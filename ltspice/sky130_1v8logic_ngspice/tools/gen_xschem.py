#!/usr/bin/env python3
"""Generate xschem schematics and symbols for the 1.8 V DAC from a flat SPICE subcircuit
library (the netlist of the LTspice schematics in ../../sky130_1v8logic).

Usage: python3 gen_xschem.py circuit.lib ../xschem

Each .subckt becomes <name>.sch and <name>.sym. Sky130 adapter cells from
Sky130_Adapters.lib are replaced by the PDK xschem symbols:
  SKY_N1 / SKY_P1 -> sky130_fd_pr/nfet_01v8.sym / pfet_01v8.sym (nf=1, mult=N)
  SKY_R1K         -> sky130_fd_pr/res_high_po_0p69.sym, L=7.33, mult=4 (four legs in parallel)
  SKY_R           -> sky130_fd_pr/res_high_po_0p69.sym, L=<l>
  SKY_C           -> sky130_fd_pr/cap_mim_m3_1.sym, W=L=<side>
Nets are connected with lab_pin labels placed on the symbol pins, so no wires are drawn.
"""
import re, sys, os, math

TOP_NAME = "dac6_1v8"           # CACE project / DUT name
CORE = "DAC6_Sky130_Core"
PARAMS = {"RCOMP_L": 2.2, "CC_SIDE": round(173 * math.sqrt(45 / 60), 3)}   # values from the LTspice top sheet

HDR = "v {xschem version=3.4.4 file_version=1.2\n}\n"

# PDK symbol pin positions (from xschem_sky130/sky130_fd_pr/*.sym)
NFET = {"D": (20, -30), "G": (-20, 0), "S": (20, 30), "B": (20, 0)}
PFET = {"D": (20, 30), "G": (-20, 0), "S": (20, -30), "B": (20, 0)}
RES = {"P": (0, -30), "M": (0, 30), "B": (-20, 0)}
CAP = {"c0": (0, -30), "c1": (0, 30)}

def parse(path):
    subs, cur = {}, None
    for ln in open(path):
        t = ln.split()
        if not t or t[0].startswith("*"):
            continue
        if t[0].lower() == ".subckt":
            cur = t[1]; subs[cur] = {"pins": t[2:], "inst": []}
        elif t[0].lower() == ".ends":
            cur = None
        elif cur and t[0][0] in "Xx":
            args = [a for a in t[1:] if "=" not in a]
            prm = dict(a.split("=", 1) for a in t[1:] if "=" in a)
            subs[cur]["inst"].append((t[0], args[:-1], args[-1], prm))
    return subs

def val(v):
    m = re.fullmatch(r"\{(\w+)\}", v)
    return PARAMS[m.group(1)] if m else float(v)

def fmt(x):
    return ("%.6g" % x)

def pin_dirs(name, pins):
    d = {}
    for p in pins:
        if p in ("VDD", "VDDA", "VSS"):
            d[p] = "inout"
        elif re.fullmatch(r"(Y|Z|OUT|VOUT|VTAP|TAP|G2|BP)", p) or (name == "DAC_Control" and re.fullmatch(r"S\dB?|E|EB", p)):
            d[p] = "out"
        else:
            d[p] = "in"
    if name == "Sky_Bias":
        d["BP"] = "out"; d["IBIAS"] = "inout"
    if name in ("Sky_InputP", "Sky_Output"):
        d["BP"] = "in"
    if name == "Sky_Output":
        d["G2"] = "in"
    if name in ("Sky_InputN", "Sky_OTA", "DAC_Buffer", CORE):
        d["IBIAS"] = "inout"
    if name == "DAC_Bank8":
        d["LO"] = d["HI"] = "inout"
    if name in ("DAC_String64", CORE):
        d["VREFL"] = d["VREFH"] = "inout"
    return d

def write_sym(path, name, pins, dirs):
    """Box symbol: inputs on the left, outputs/inouts on the right, pins in SPICE order."""
    left = [p for p in pins if dirs[p] == "in"]
    right = [p for p in pins if dirs[p] != "in"]
    n = max(len(left), len(right), 1)
    h = 20 * n + 20
    w = max(140, 9 * max(len(name), 8) + 40)
    pos = {}
    for i, p in enumerate(left):
        pos[p] = (-w / 2 - 20, -h / 2 + 20 + 20 * i)
    for i, p in enumerate(right):
        pos[p] = (w / 2 + 20, -h / 2 + 20 + 20 * i)
    o = [HDR, "G {}\n",
         'K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}\n',
         "V {}\nS {}\nE {}\n"]
    x0, y0, x1, y1 = -w / 2, -h / 2, w / 2, h / 2
    o.append(f"P 4 5 {x0} {y0} {x1} {y0} {x1} {y1} {x0} {y1} {x0} {y0} {{}}\n")
    for p in pins:          # SPICE order = order of B 5 records
        x, y = pos[p]
        o.append(f"B 5 {x-2.5} {y-2.5} {x+2.5} {y+2.5} {{name={p} dir={dirs[p]}}}\n")
        if x < 0:
            o.append(f"L 4 {x} {y} {x0} {y} {{}}\nT {{{p}}} {x0+5} {y-6} 0 0 0.2 0.2 {{}}\n")
        else:
            o.append(f"L 4 {x1} {y} {x} {y} {{}}\nT {{{p}}} {x1-5} {y-6} 0 1 0.2 0.2 {{}}\n")
    o.append(f"T {{@symname}} 0 {y0-25} 0 0 0.25 0.25 {{hcenter=true}}\nT {{@name}} 0 {y1+5} 0 0 0.2 0.2 {{hcenter=true}}\n")
    open(path, "w").write("".join(o))
    return pos

def write_sch(path, name, sub, sympos):
    o = [HDR, "G {}\nK {}\nV {}\nS {}\nE {}\n"]
    o.append(f"T {{{name}: generated from the LTspice schematic by tools/gen_xschem.py}} -900 -560 0 0 0.4 0.4 {{}}\n")
    dirs = pin_dirs(name, sub["pins"])
    sym = {"in": "devices/ipin.sym", "out": "devices/opin.sym", "inout": "devices/iopin.sym"}
    for i, p in enumerate(sub["pins"]):
        o.append(f"C {{{sym[dirs[p]]}}} -900 {-500 + 30 * i} 0 0 {{name=p{i+1} lab={p}}}\n")
    nlab = 0
    def lab(x, y, net):
        nonlocal nlab
        nlab += 1
        o.append(f"C {{devices/lab_pin.sym}} {x} {y} 0 0 {{name=l{nlab} sig_type=std_logic lab={net}}}\n")
    cols = 6
    for k, (iname, nets, cell, prm) in enumerate(sub["inst"]):
        X = -500 + 320 * (k % cols); Y = -400 + 220 * (k // cols)
        base = re.sub(r"^X_?", "", iname)
        if cell in ("SKY_N1", "SKY_P1"):
            W, L, M = val(prm["w"]), val(prm["l"]), int(val(prm.get("mult", "1")))
            symf, pinmap = ("nfet_01v8", NFET) if cell == "SKY_N1" else ("pfet_01v8", PFET)
            attrs = (f"name={base} W={fmt(W)} L={fmt(L)} nf=1 mult={M} "
                     f"ad={fmt(W*0.29)} pd={fmt(2*(W+0.29))} as={fmt(W*0.29)} ps={fmt(2*(W+0.29))} "
                     f"nrd={fmt(0.29/W)} nrs={fmt(0.29/W)} sa=0 sb=0 sd=0 model={symf} spiceprefix=X")
            o.append(f"C {{sky130_fd_pr/{symf}.sym}} {X} {Y} 0 0 {{{attrs}}}\n")
            for pn, net in zip("DGSB", nets):
                lab(X + pinmap[pn][0], Y + pinmap[pn][1], net)
        elif cell in ("SKY_R1K", "SKY_R"):
            L, M = (7.33, 4) if cell == "SKY_R1K" else (val(prm["l"]), 1)
            o.append(f"C {{sky130_fd_pr/res_high_po_0p69.sym}} {X} {Y} 0 0 "
                     f"{{name={base} L={fmt(L)} model=res_high_po_0p69 spiceprefix=X mult={M}}}\n")
            for pn, net in zip("MPB", nets):   # xschem pin order of res_high_po_0p69.sym is M, P, B
                lab(X + RES[pn][0], Y + RES[pn][1], net)
        elif cell == "SKY_C":
            Wc, Lc = val(prm["w"]), val(prm["l"])
            o.append(f"C {{sky130_fd_pr/cap_mim_m3_1.sym}} {X} {Y} 0 0 "
                     f"{{name={base} model=cap_mim_m3_1 W={fmt(Wc)} L={fmt(Lc)} MF=1 spiceprefix=X}}\n")
            for pn, net in zip(("c0", "c1"), nets):
                lab(X + CAP[pn][0], Y + CAP[pn][1], net)
        else:
            o.append(f"C {{{cell}.sym}} {X} {Y} 0 0 {{name=x{base}}}\n")
            for pn, net in zip(SUBS[cell]["pins"], nets):
                px, py = sympos[cell][pn]
                lab(X + px, Y + py, net)
    open(path, "w").write("".join(o))

if __name__ == "__main__":
    SUBS = parse(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    # The CACE DUT is the core with a lower-case project name
    SUBS[TOP_NAME] = SUBS.pop(CORE)
    for s in SUBS.values():
        s["inst"] = [(i, n, TOP_NAME if c == CORE else c, p) for i, n, c, p in s["inst"]]
    sympos = {}
    for name, s in SUBS.items():
        d = pin_dirs(CORE if name == TOP_NAME else name, s["pins"])
        sympos[name] = write_sym(f"{out}/{name}.sym", name, s["pins"], d)
    for name, s in SUBS.items():
        write_sch(f"{out}/{name}.sch", CORE if name == TOP_NAME else name, s, sympos)
    print("wrote", len(SUBS), "cells to", out)
