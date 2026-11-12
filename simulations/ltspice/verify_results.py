#!/usr/bin/env python3
"""Check the supplied LTspice transient examples using only Python's standard library."""

import argparse
import bisect
import json
import math
import re
import struct
import sys
from pathlib import Path

RUNS = ("Mux4_Complete", "Mux4_Testbench", "Mux4_Heavy_Load")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_run(path, prefix):
    """Read selected traces from real binary RAW files, including FastAccess."""
    blob = path.read_bytes()
    encoding = "utf-16-le" if blob[:2] in (b"T\0", b"\xff\xfe") else "utf-8-sig"
    marker = "Binary:\n".encode("utf-16-le" if encoding == "utf-16-le" else "utf-8")
    # Also accept headers written with Windows CRLF line endings.
    if marker not in blob:
        marker = "Binary:\r\n".encode("utf-16-le" if encoding == "utf-16-le" else "utf-8")
    require(marker in blob, f"{path.name}: expected binary RAW output from a transient run")
    end = blob.index(marker)
    header = blob[:end].decode(encoding)
    payload = memoryview(blob)[end + len(marker):]
    flags = re.search(r"^Flags:\s*(.*)$", header, re.M).group(1).lower().split()
    require("real" in flags and "complex" not in flags, f"{path.name}: expected a real transient run")
    require("Transient Analysis" in header, f"{path.name}: expected transient analysis")
    count = int(re.search(r"No\. Variables:\s*(\d+)", header).group(1))
    points = int(re.search(r"No\. Points:\s*(\d+)", header).group(1))
    names = re.findall(r"^\s*\d+\s+(\S+)\s+\S+", header, re.M)
    require(len(names) == count and points > 1, f"{path.name}: incomplete RAW header")
    indices = {name.lower(): i for i, name in enumerate(names)}
    needed = ["time", "v(out)", "v(en)", "v(s0)", "v(s1)"]
    needed += [f"v(in{i})" for i in range(4)]
    needed += [f"v({prefix}d{i}{suffix})" for i in range(4) for suffix in ("", "b")]
    require(all(name in indices for name in needed), f"{path.name}: missing mux traces; use the supplied .save directive")
    require(f"v({prefix}xdecoder:s1b)" in indices, f"{path.name}: internal voltages were not saved")
    require(any(name.startswith("id(") and ":mn" in name for name in indices), f"{path.name}: MOSFET drain currents were not saved")
    scalar_bytes = 8 if "double" in flags else 4
    scalar = struct.Struct("<d" if scalar_bytes == 8 else "<f")
    row_bytes = 8 + (count - 1) * scalar_bytes
    require(len(payload) >= points * row_bytes, f"{path.name}: incomplete simulation data")
    result = {}
    for name in needed:
        column = indices[name]
        fmt = struct.Struct("<d") if column == 0 else scalar
        if "fastaccess" in flags:
            start = 0 if column == 0 else points * (8 + (column - 1) * scalar_bytes)
            stride = fmt.size
        else:
            start = 0 if column == 0 else 8 + (column - 1) * scalar_bytes
            stride = row_bytes
        result[name] = [fmt.unpack_from(payload, start + k * stride)[0] for k in range(points)]
        require(all(math.isfinite(v) for v in result[name]), f"{path.name}: non-finite {name}")
    times = result["time"]
    require(all(a <= b for a, b in zip(times, times[1:])), f"{path.name}: expected one unstepped transient run")
    require(abs(times[-1] - 0.008) < 1e-9, f"{path.name}: simulation must finish at 8 ms")
    return result


def check_run(data, prefix, heavy):
    times = data["time"]
    stable = [(k, min(int(t / 0.001), 7) % 4) for k, t in enumerate(times)
              if 50e-6 < t % 0.001 < 970e-6 and t < 0.00785]
    require(stable, "No settled samples found")
    decoder_error = 0.0
    channel_rows = []
    for k, channel in stable:
        address = 2 * int(data["v(s1)"][k] > 2.5) + int(data["v(s0)"][k] > 2.5)
        require(address == channel and data["v(en)"][k] > 4.99, "Unexpected address/enable stimulus")
        for i in range(4):
            decoder_error = max(decoder_error,
                abs(data[f"v({prefix}d{i})"][k] - (5 if i == channel else 0)),
                abs(data[f"v({prefix}d{i}b)"][k] - (0 if i == channel else 5)))
    require(decoder_error < 0.01, "Decoder selection does not match the truth table")
    for channel in range(4):
        ks = [k for k, selected in stable if selected == channel]
        require(ks, f"IN{channel} was not exercised")
        error = max(abs(data["v(out)"][k] - data[f"v(in{channel})"][k]) for k in ks)
        gain = sum(data["v(out)"][k] / data[f"v(in{channel})"][k] for k in ks) / len(ks)
        require(error < (0.12 if heavy else 0.0012), f"IN{channel}: settled output error exceeded the test limit")
        if heavy:
            require(0.96 < gain < 0.99, f"IN{channel}: heavy-load attenuation was not observed")
        channel_rows.append({"input": channel, "max_settled_error_mV": error * 1000, "mean_gain": gain})
    off = [k for k, t in enumerate(times) if 2e-6 < t < 18e-6
           or any(i * 0.001 - 7e-6 < t < i * 0.001 - 2e-6 for i in range(1, 8))
           or 0.00793 < t < 0.008]
    require(off, "No disabled samples found")
    off_error = max(max(abs(data[f"v({prefix}d{i})"][k]),
                       abs(data[f"v({prefix}d{i}b)"][k] - 5)) for k in off for i in range(4))
    require(off_error < 0.01, "A channel remained enabled during a disabled interval")
    require(abs(data["v(out)"][-1]) < 0.001, "The external load did not discharge OUT after disable")
    return {"points": len(times), "duration_s": times[-1], "decoder_max_error_V": decoder_error,
            "disabled_decoder_max_error_V": off_error, "channels": channel_rows}


def interpolate(data, time):
    times, values = data["time"], data["v(out)"]
    k = bisect.bisect_left(times, time)
    if times[k] == time:
        return values[k]
    return values[k - 1] + (values[k] - values[k - 1]) * (time - times[k - 1]) / (times[k] - times[k - 1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent,
                        help="Folder containing the three completed RAW files (defaults to this script's folder)")
    args = parser.parse_args()
    try:
        summary, runs = {}, {}
        for name in RUNS:
            prefix = "xmux:" if name == "Mux4_Testbench" else ""
            runs[name] = read_run(args.directory / (name + ".raw"), prefix)
            summary[name] = check_run(runs[name], prefix, name == "Mux4_Heavy_Load")
        difference = max(abs(interpolate(runs["Mux4_Complete"], (slot + phase) * 0.001)
                             - interpolate(runs["Mux4_Testbench"], (slot + phase) * 0.001))
                         for slot in range(8) for phase in (0.2, 0.5, 0.8))
        require(difference < 1e-5, "Reusable mux and full assembly differ by more than 10 uV")
        summary["complete_vs_reusable_symbol_max_difference_V"] = difference
        summary["status"] = "pass"
        print(json.dumps(summary, indent=2))
        return 0
    except (OSError, ValueError, AttributeError, struct.error) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        print("Run Mux4_Complete.asc, Mux4_Testbench.asc and Mux4_Heavy_Load.asc first.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
