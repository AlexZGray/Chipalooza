#!/usr/bin/env python3
"""Check that the xschem netlist of the generated schematics has the same devices, nets and sizes
as the reference SPICE library. Usage: compare_netlists.py circuit.lib xschem_netlist.spice"""
import re, sys
MAP = {"SKY_N1": "nfet_01v8", "SKY_P1": "pfet_01v8", "SKY_R1K": "res_high_po_0p69",
       "SKY_R": "res_high_po_0p69", "SKY_C": "cap_mim_m3_1", "DAC6_Sky130_Core": "dac6_1v8"}
PAR = {"RCOMP_L": "2.2", "CC_SIDE": "149.822"}

def lines(path):
    buf = []
    for ln in open(path):
        ln = ln.rstrip("\n")
        if ln.startswith("+") and buf:
            buf[-1] += " " + ln[1:]
        else:
            buf.append(ln)
    return buf

def norm(x):
    x = PAR.get(x.strip("{}"), x)
    try: return "%.5g" % float(x)
    except ValueError: return x

def parse(path, ref):
    subs, cur = {}, None
    for ln in lines(path):
        ln = re.sub(r"^\*\*\.subckt", ".subckt", ln)
        t = ln.split()
        if not t: continue
        if t[0].lower() == ".subckt":
            cur = MAP.get(t[1], t[1]); subs[cur] = {"pins": t[2:], "dev": []}; continue
        if t[0].lower() in (".ends", "**.ends"):
            cur = None; continue
        if cur is None or t[0][0] not in "Xx": continue
        args = [a for a in t[1:] if "=" not in a]
        prm = {k.lower(): v for k, v in (a.split("=", 1) for a in t[1:] if "=" in a)}
        cell = args[-1].replace("sky130_fd_pr__", ""); nets = args[:-1]
        name = re.sub(r"^[Xx]_?X?", "", t[0]).upper()
        if ref:
            c0 = cell; cell = MAP.get(cell, cell)
            if c0 in ("SKY_N1", "SKY_P1"):
                key = (norm(prm["w"]), norm(prm["l"]), norm(prm.get("mult", "1")))
            elif c0 == "SKY_R1K": key = ("7.33", "4")
            elif c0 == "SKY_R": key = (norm(prm["l"]), "1")
            elif c0 == "SKY_C": key = (norm(prm["w"]), norm(prm["l"]))
            else: key = ()
        else:
            if cell in ("nfet_01v8", "pfet_01v8"):
                key = (norm(prm["w"]), norm(prm["l"]), norm(prm["mult"]))
                assert prm["m"] == prm["mult"] and prm["nf"] == "1"
            elif cell.startswith("res_"): key = (norm(prm["l"]), norm(prm["mult"]))
            elif cell.startswith("cap_"): key = (norm(prm["w"]), norm(prm["l"]))
            else: key = ()
        subs[cur]["dev"].append((name, cell, tuple(nets), key))
    return subs

a, b = parse(sys.argv[1], True), parse(sys.argv[2], False)
bad = 0
for k in a:
    if k not in b: print("missing cell", k); bad += 1; continue
    if a[k]["pins"] != b[k]["pins"]: print("pin order differs", k, a[k]["pins"], b[k]["pins"]); bad += 1
    sa, sb = sorted(a[k]["dev"]), sorted(b[k]["dev"])
    if sa != sb:
        bad += 1; print("cell", k, "differs")
        for x in set(sa) ^ set(sb): print("   ", x)
print("cells compared:", len(a), "devices:", sum(len(v["dev"]) for v in a.values()), "mismatches:", bad)
sys.exit(1 if bad else 0)
