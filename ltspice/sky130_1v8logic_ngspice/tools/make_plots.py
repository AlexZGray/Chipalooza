#!/usr/bin/env python3
"""Supplementary graphs from a CACE run of dac6_1v8 (reads runs/RUN_*/parameters/*/run_*).

Usage: python3 make_plots.py <runs/RUN_...> <output folder>"""
import glob, os, sys, math
import numpy as np, yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
C = ["#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17", "#6a4ce2", "#ec4647"]
GREY, INK, INK2 = "#b8b8b8", "#191919", "#666666"
CORNERS = ["tt", "ss", "ff", "sf", "fs"]
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#cccccc", "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": "#e6e6e6",
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                     "lines.linewidth": 2, "legend.frameon": False, "figure.dpi": 130})

def runs(param):
    out = []
    for d in sorted(glob.glob(f"{RUN}/parameters/{param}/run_*")):
        cond = yaml.safe_load(open(f"{d}/conditions.yaml"))
        data = glob.glob(f"{d}/*.data")
        if data:
            out.append((cond, np.loadtxt(data[0], ndmin=2)))
    return out

def save(fig, name):
    fig.tight_layout(); fig.savefig(f"{OUT}/{name}.png"); plt.close(fig); print("wrote", name)

def static(a, vdd):
    """a: columns time, code, vout, vtap, idd, istring of the staircase run."""
    last = {}
    for i, c in enumerate(a[:, 1]):
        if abs(c - round(c)) < 1e-3:
            last[int(round(c))] = i
    a = a[[last[k] for k in sorted(last)]]
    lsb = vdd / 64; v = a[:, 2]; k = np.arange(len(v))
    inl = (v - v[0] - k * (v[-1] - v[0]) / 63) / lsb
    return dict(v=v, tap=a[:, 3], err=(v - k * lsb) / lsb, inl=inl, dnl=np.diff(v) / lsb - 1,
                idd=(a[:, 4] + a[:, 5]) * 1e6)

# 1. PVT envelopes of absolute error, INL and DNL
pvt = [r for r in runs("static_pvt") if r[1].shape[1] == 6]
if pvt:
    S = [(c, static(a, float(c["Vvdd"]))) for c, a in pvt]
    nom = next(s for c, s in S if c["corner"] == "tt" and float(c["Vvdd"]) == 1.8 and float(c["temperature"]) == 25)
    fig, axs = plt.subplots(3, 1, figsize=(8, 9), sharex=True)
    for ax, key, lab in zip(axs, ["err", "inl", "dnl"], ["Absolute error (LSB)", "INL, endpoint (LSB)", "DNL (LSB)"]):
        Y = np.array([s[key] for _, s in S]); x = np.arange(Y.shape[1]) + (0.5 if key == "dnl" else 0)
        ax.fill_between(x, Y.min(0), Y.max(0), color=C[0], alpha=0.18, lw=0, label=f"range over {len(S)} PVT runs")
        ax.plot(x, nom[key], color=C[0], label="TT, 1.8 V, 25 °C")
        for lim in (-0.5, 0.5): ax.axhline(lim, color=C[7], lw=1, ls="--")
        ax.set_ylabel(lab); ax.set_ylim(-0.6, 0.6)
    axs[0].legend(loc="upper left", bbox_to_anchor=(0.0, 0.9), ncol=2); axs[-1].set_xlabel("Code")
    axs[0].set_title("Static accuracy over 5 corners × 3 supplies × 3 temperatures (dashed: ±0.5 LSB limit)", fontsize=10, color=INK)
    save(fig, "pvt_static_envelope")

    # worst |INL| per corner and temperature
    temps = sorted({float(c["temperature"]) for c, _ in S})
    fig, ax = plt.subplots(figsize=(8, 3.6)); w = 0.8 / len(temps)
    for j, t in enumerate(temps):
        vals = [max(max(abs(s["inl"]).max(), abs(s["err"]).max()) for c, s in S if c["corner"] == k and float(c["temperature"]) == t) for k in CORNERS]
        ax.bar(np.arange(5) + (j - 1) * w, vals, w * 0.92, color=C[j], label=f"{t:g} °C")
    ax.set_xticks(range(5), [k.upper() for k in CORNERS]); ax.set_ylabel("Worst |error| or |INL| (LSB)")
    ax.axhline(0.5, color=C[7], lw=1, ls="--"); ax.legend(ncol=3, loc="upper right"); ax.set_ylim(0, 0.68)
    ax.set_title("Worst static error per corner, over the three supply voltages", fontsize=10, color=INK)
    save(fig, "pvt_worst_error")

    # supply current vs code
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for i, k in enumerate(CORNERS):
        s = next(s for c, s in S if c["corner"] == k and float(c["Vvdd"]) == 1.89 and float(c["temperature"]) == 110)
        ax.plot(s["idd"], color=C[i], label=k.upper())
    ax.plot(nom["idd"], color=INK2, ls=":", label="TT, 1.8 V, 25 °C")
    ax.set_xlabel("Code"); ax.set_ylabel("Supply current incl. string (µA)"); ax.legend(ncol=6, loc="lower left")
    ax.set_title("Supply current at the end of each staircase step, 1.89 V and 110 °C per corner", fontsize=10, color=INK)
    save(fig, "supply_current")

    # buffer offset
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for i, k in enumerate(CORNERS):
        s = next(s for c, s in S if c["corner"] == k and float(c["Vvdd"]) == 1.8 and float(c["temperature"]) == 25)
        ax.plot((s["v"] - s["tap"]) * 1e3, color=C[i], label=k.upper())
    ax.set_xlabel("Code"); ax.set_ylabel("VOUT − VTAP (mV)"); ax.legend(ncol=5)
    ax.set_title("Buffer offset per code, 1.8 V, 25 °C (1 LSB = 28.1 mV)", fontsize=10, color=INK)
    save(fig, "buffer_offset_corners")

# 2. Monte Carlo
mc = [r for r in runs("static_mc") if r[1].shape[1] == 6]
if mc:
    M = [static(a, float(c["Vvdd"])) for c, a in mc]
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.6))
    for s in M: axs[0].plot(s["inl"], color=C[0], lw=1, alpha=0.35)
    axs[0].set_xlabel("Code"); axs[0].set_ylabel("INL (LSB)"); axs[0].set_title(f"INL, {len(M)} mismatch samples", fontsize=10)
    for lim in (-0.5, 0.5): axs[0].axhline(lim, color=C[7], lw=1, ls="--")
    axs[0].set_ylim(-0.6, 0.6)
    worst_inl = [abs(s["inl"]).max() for s in M]; worst_dnl = [abs(s["dnl"]).max() for s in M]
    worst_err = [abs(s["err"]).max() for s in M]
    bins = np.linspace(0, 0.5, 26)
    axs[1].hist(worst_inl, bins, color=C[0], alpha=0.8, label="max |INL|", edgecolor="white", lw=1)
    axs[1].hist(worst_dnl, bins, color=C[1], alpha=0.7, label="max |DNL|", edgecolor="white", lw=1)
    axs[1].hist(worst_err, bins, color=C[2], alpha=0.6, label="max |abs. error|", edgecolor="white", lw=1)
    axs[1].set_xlabel("Per-sample worst value (LSB)"); axs[1].set_ylabel("Samples"); axs[1].legend()
    axs[1].set_title("Worst value per Monte Carlo sample", fontsize=10)
    save(fig, "mc_static")
    off = [(s["v"][32] - s["tap"][32]) * 1e3 for s in M]
    np.savetxt(f"{OUT}/mc_summary.txt", np.c_[worst_inl, worst_dnl, worst_err, off],
               header="max|INL| max|DNL| max|err| (LSB), buffer offset at code 32 (mV)", fmt="%.4f")

# 3. Step waveforms
wf = runs("step_waveform")
if wf:
    lsb = 1.8 / 64
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8))
    names = {0: "0 → 63", 63: "63 → 0", 31: "31 → 32", 32: "32 → 31"}
    for i, (c, a) in enumerate(sorted(wf, key=lambda r: [0, 63, 31, 32].index(int(r[0]["b"])))):
        t = (a[:, 0] - 2e-6) * 1e6; v = a[:, 1]; b = int(c["b"])
        ax = axs[0] if b in (0, 63) else axs[1]
        if b in (0, 63):
            ax.plot(t, v, color=C[i], label=names[b])
        else:
            ax.plot(t, (v - v[-1]) * 1e3, color=C[i], label=names[b])
    axs[0].set_xlabel("Time after code change (µs)"); axs[0].set_ylabel("VOUT (V)"); axs[0].legend(); axs[0].set_xlim(-1, 20)
    axs[0].set_title("Full-scale steps, TT, 25 °C, 100 kΩ ∥ 20 pF", fontsize=10)
    for lim in (-0.5 * lsb * 1e3, 0.5 * lsb * 1e3): axs[1].axhline(lim, color=C[7], lw=1, ls="--")
    axs[1].set_xlabel("Time after code change (µs)"); axs[1].set_ylabel("VOUT − final value (mV)"); axs[1].legend()
    axs[1].set_xlim(-1, 20); axs[1].set_title("Midscale steps (dashed: ±0.5 LSB)", fontsize=10)
    save(fig, "step_waveforms")

# 4. Settling over PVT
st = runs("settling")
if st:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cace", "scripts"))
    import settling as S_
    rows = []
    for c, a in st:
        r = S_.postprocess({"time": list(a[:, 0]), "vout": list(a[:, 1])}, c)
        rows.append((c["corner"], float(c["temperature"]), int(c["b"]), r["settling_time"][0] * 1e6))
    fig, ax = plt.subplots(figsize=(9, 3.8))
    labels = []; x = 0
    for k in CORNERS:
        for t in sorted({r[1] for r in rows}):
            labels.append(f"{k.upper()}\n{t:g} °C")
            for j, b in enumerate([0, 63, 31, 32]):
                val = next(r[3] for r in rows if r[0] == k and r[1] == t and r[2] == b)
                ax.bar(x + (j - 1.5) * 0.2, val, 0.18, color=C[j], label=["0 → 63", "63 → 0", "31 → 32", "32 → 31"][j] if x == 0 else None)
            x += 1
    ax.set_ylim(0, 24); ax.axhline(20, color=C[7], lw=1, ls="--"); ax.set_xticks(range(len(labels)), labels, fontsize=7)
    ax.set_ylabel("Settling to ±0.5 LSB (µs)"); ax.legend(ncol=4, loc="upper left")
    ax.set_title("Settling time per corner and temperature, 1.8 V (dashed: 20 µs limit)", fontsize=10)
    save(fig, "settling_pvt")

# 5. Loop gain Bode plot at TT
lg = runs("loop_gain")
if lg:
    tt = sorted([r for r in lg if r[0]["corner"] == "tt" and float(r[0]["temperature"]) == 25], key=lambda r: float(r[0]["Vin"]))
    fig, axs = plt.subplots(2, 1, figsize=(8, 5.5), sharex=True)
    for i, (c, a) in enumerate(tt):
        f, g, p = a[:, 0], a[:, 1], a[:, 2]
        p = p - 360 * round(p[0] / 360)
        axs[0].semilogx(f, g, color=C[i], label=f"Vin = {float(c['Vin']):g} V")
        axs[1].semilogx(f, p, color=C[i])
    axs[0].axhline(0, color=INK2, lw=0.8); axs[1].axhline(-180, color=INK2, lw=0.8)
    axs[0].set_ylabel("Loop gain (dB)"); axs[1].set_ylabel("Phase (°)"); axs[1].set_xlabel("Frequency (Hz)")
    axs[0].legend(); axs[0].set_title("Buffer loop gain, TT, 25 °C, 100 kΩ ∥ 20 pF", fontsize=10)
    axs[1].set_ylim(-270, 10)
    save(fig, "loop_gain_tt")

# 6. PSRR
ps = runs("psrr")
if ps:
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for i, k in enumerate(CORNERS):
        c, a = next(r for r in ps if r[0]["corner"] == k)
        ax.semilogx(a[:, 0], a[:, 1], color=C[i], label=k.upper())
    ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("PSRR (dB)"); ax.legend(ncol=5, loc="upper right")
    ax.set_title("VDDA rejection at code 32, references held fixed, 25 °C", fontsize=10)
    save(fig, "psrr_corners")
