#!/usr/bin/env python3
"""Check the three supplied LTspice transient examples; standard library only.

Run all three .asc testbenches first. Reference measurements are never overwritten.
"""

import argparse
import bisect
import csv
import json
import math
import re
import struct
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
LSB = 2.7 / 64
RUNS = ("DAC6_Top", "DAC6_Heavy_Load", "DAC6_Tap_Load")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def raw(path):
    """Read selected traces from normal or FastAccess real binary RAW files."""
    blob = path.read_bytes()
    encoding = "utf-16-le" if blob[:2] in (b"T\0", b"\xff\xfe") else "utf-8-sig"
    marker_encoding = "utf-16-le" if encoding == "utf-16-le" else "utf-8"
    marker = "Binary:\n".encode(marker_encoding)
    if marker not in blob:
        marker = "Binary:\r\n".encode(marker_encoding)
    require(marker in blob, f"{path.name}: expected a binary LTspice RAW file")
    end = blob.index(marker)
    header = blob[:end].decode(encoding)
    payload = memoryview(blob)[end + len(marker):]
    require("Transient Analysis" in header, f"{path.name}: expected transient analysis")
    count = int(re.search(r"No\. Variables:\s*(\d+)", header).group(1))
    points = int(re.search(r"No\. Points:\s*(\d+)", header).group(1))
    names = re.findall(r"^\s*\d+\s+(\S+)\s+\S+", header, re.M)
    flags = re.search(r"^Flags:\s*(.*)", header, re.M).group(1).lower().split()
    require("real" in flags and "complex" not in flags, "Expected real transient data")
    require(len(names) == count and points > 1, "Incomplete RAW header")
    size = 8 if "double" in flags else 4
    row_bytes = 8 + (count - 1) * size
    require(len(payload) == points * row_bytes, f"{path.name}: incomplete RAW data")
    wanted = {
        "time", "v(out)", "v(tap)", "v(dac_in)", "v(en)",
        "v(e)", "v(eb)", "i(vhigh)",
    }
    wanted.update(f"v(d{i})" for i in range(6))
    wanted.update(f"v(s{i}{suffix})" for i in range(6) for suffix in ("", "b"))
    result = {}
    for column, name in enumerate(names):
        name = name.lower()
        if name not in wanted:
            continue
        fmt = struct.Struct("<d" if column == 0 or size == 8 else "<f")
        start = 0 if column == 0 else 8 + (column - 1) * size
        stride = row_bytes
        if "fastaccess" in flags:
            start = 0 if column == 0 else points * (8 + (column - 1) * size)
            stride = fmt.size
        values = [fmt.unpack_from(payload, start + k * stride)[0] for k in range(points)]
        require(all(math.isfinite(v) for v in values), f"Non-finite values in {name}")
        result[name] = values
    require(wanted <= result.keys(), f"Missing traces: {sorted(wanted - result.keys())}")
    times = result["time"]
    require(abs(times[-1] - 0.008) < 1e-10, f"{path.name}: simulation must finish at 8 ms")
    require(all(a <= b for a, b in zip(times, times[1:])), "Expected an unstepped run")
    return result


def mean_window(run, signal, start, stop):
    first = bisect.bisect_left(run["time"], start)
    last = bisect.bisect_right(run["time"], stop)
    require(last > first, f"No samples in {start:g}..{stop:g} s")
    return sum(run[signal][first:last]) / (last - first)


def analyse(directory=BASE):
    """Validate waveforms and write latest metrics, without changing references."""
    directory = Path(directory)
    missing = [name + ".raw" for name in RUNS if not (directory / (name + ".raw")).exists()]
    require(not missing, "Missing simulations: " + ", ".join(missing) +
            ". Open and run all three DAC6_*.asc testbenches in LTspice first.")
    runs = {name: raw(directory / (name + ".raw")) for name in RUNS}
    run = runs["DAC6_Top"]
    times = run["time"]
    codes = json.loads((directory / "stimulus.json").read_text())["codes"]
    rows = []
    rail_error = 0.0
    for code in range(64):
        start, stop = code * 1e-4 + 60e-6, code * 1e-4 + 90e-6
        ideal = 0.3 + code * LSB
        output = mean_window(run, "v(out)", start, stop)
        tap = mean_window(run, "v(tap)", start, stop)
        rows.append({"code": code, "ideal_V": ideal, "tap_V": tap,
                     "output_V": output, "error_LSB": (output - ideal) / LSB})
        for bit in range(6):
            level = (code >> bit) & 1
            for suffix, expected in (("", level), ("b", 1 - level)):
                actual = mean_window(run, f"v(s{bit}{suffix})", start, stop)
                rail_error = max(rail_error, abs(actual - 3.3 * expected))
            actual_input = mean_window(run, f"v(d{bit})", start, stop)
            require(abs(actual_input - 1.8 * level) < 0.001, "Unexpected digital stimulus")
    max_error = max(abs(row["error_LSB"]) for row in rows)
    tap_error = max(abs(row["tap_V"] - row["ideal_V"]) / LSB for row in rows)
    steps = [rows[i + 1]["output_V"] - rows[i]["output_V"] for i in range(63)]
    dnl = [step / LSB - 1 for step in steps]
    fitted_step = (rows[-1]["output_V"] - rows[0]["output_V"]) / 63
    inl = [(row["output_V"] - rows[0]["output_V"] - row["code"] * fitted_step) / LSB
           for row in rows]
    require(min(steps) > 0, "Non-monotonic output")
    require(max_error < 0.25, f"Output accuracy failed: {max_error:g} LSB")
    require(tap_error < 0.01, f"Tap selection failed: {tap_error:g} LSB")
    require(rail_error < 0.01, f"Level shifting failed: {rail_error:g} V")

    settling = []
    for slot in (65, 66, 67, 68, 69, 70, 71, 74, 75, 76, 77, 78):
        target = 0.3 + codes[slot] * LSB
        start, stop = slot * 1e-4, (slot + 1) * 1e-4 - 1e-7
        first = bisect.bisect_left(times, start)
        last = bisect.bisect_right(times, stop)
        require(last > first, f"No samples for stress-test slot {slot}")
        outside = [k for k in range(first, last) if abs(run["v(out)"][k] - target) > 0.5 * LSB]
        elapsed = 0 if not outside else times[min(outside[-1] + 1, last - 1)] - start
        require(abs(run["v(out)"][last - 1] - target) < 0.5 * LSB, "Output did not settle")
        settling.append({"slot": slot, "code": codes[slot], "time_us": elapsed * 1e6})
    max_settling = max(row["time_us"] for row in settling)
    require(max_settling < 20, f"Settling exceeds 20 us: {max_settling:g}")
    disabled = mean_window(run, "v(out)", 0.00725, 0.00735)
    require(abs(disabled - 0.3) < 0.25 * LSB, "Disabled output did not reset")
    require(mean_window(run, "v(e)", 0.00725, 0.00735) < 0.01 and
            mean_window(run, "v(eb)", 0.00725, 0.00735) > 3.29, "Enable controls failed")
    heavy = mean_window(runs["DAC6_Heavy_Load"], "v(out)", 0.00634, 0.00639)
    require(0.3 + 63 * LSB - heavy > 0.25, "Heavy-load failure was not demonstrated")
    tap_loading_errors = [
        abs(mean_window(runs["DAC6_Tap_Load"], "v(tap)", i * 1e-4 + 60e-6,
                        i * 1e-4 + 90e-6) - (0.3 + i * LSB)) for i in range(64)
    ]
    require(max(tap_loading_errors) > 0.15, "Direct-tap loading failure was not demonstrated")
    current = abs(mean_window(run, "i(vhigh)", 0.00325, 0.00329))
    require(abs(current - 2.7 / 64000) < 1e-7, "Unexpected string current")
    result = {
        "status": "PASS",
        "LSB_mV": LSB * 1e3,
        "code0_V": rows[0]["output_V"],
        "code63_V": rows[-1]["output_V"],
        "max_output_error_LSB": max_error,
        "max_tap_error_LSB": tap_error,
        "max_abs_DNL_LSB": max(map(abs, dnl)),
        "max_abs_endpoint_INL_LSB": max(map(abs, inl)),
        "min_step_mV": min(steps) * 1e3,
        "level_shift_max_rail_error_V": rail_error,
        "largest_measured_settling_us": max_settling,
        "settling_band": "ideal output +/-0.5 LSB; includes model offset",
        "settling_tests": settling,
        "disabled_output_V": disabled,
        "string_current_uA": current * 1e6,
        "heavy_load_code63_V": heavy,
        "max_direct_tap_loading_error_mV": max(tap_loading_errors) * 1e3,
        "checks": ["all 64 codes selected correctly", "monotonicity", "absolute accuracy",
                   "DNL and endpoint INL measured", "all six 1.8V inputs and 3.3V complements",
                   "major-carry and large-jump settling", "enable reset to VREFL",
                   "ladder current", "intentional heavy-load clipping", "intentional direct-tap loading"],
    }
    results = directory / "results"
    results.mkdir(exist_ok=True)
    (results / "latest.json").write_text(json.dumps(result, indent=2) + "\n")
    with (results / "latest_all_codes.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(result, indent=2))
    return result, runs, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=BASE,
                        help="Folder containing the three RAW files and stimulus.json")
    args = parser.parse_args()
    try:
        analyse(args.directory)
    except (OSError, ValueError, KeyError, AttributeError, IndexError, struct.error) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
