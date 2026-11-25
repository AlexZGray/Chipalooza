#!/usr/bin/env python3
"""Write the CACE testbench templates (xschem .sch) for dac6_1v8.

Usage: python3 gen_testbenches.py ../cace/templates

Every testbench places the DUT symbol (or the buffer amplifier symbol), the supplies and
the load as xschem symbols. The stimulus that depends on CACE conditions is in code blocks.
CACE replaces CACE{name} with condition values and evaluates CACE[expression]."""
import os, sys

HDR = "v {xschem version=3.4.4 file_version=1.2\n}\nG {}\nK {}\nV {}\nS {}\nE {}\n"
def esc(s):
    """Escape braces for an xschem attribute string."""
    return s.replace("{", "\\{").replace("}", "\\}")

class Sch:
    def __init__(self, title):
        self.o = [HDR, f"T {{{title}}} -700 -760 0 0 0.6 0.6 {{}}\n",
                  "T {VREFH has its own source at the VDDA voltage so the string current can be read} -700 420 0 0 0.3 0.3 {}\n"]
        self.n = 0
    def c(self, sym, x, y, attrs):
        self.o.append(f"C {{{sym}}} {x} {y} 0 0 {{{attrs}}}\n")
    def lab(self, x, y, net):
        self.n += 1
        if net == "GND":
            self.c("devices/gnd.sym", x, y, f"name=lg{self.n} lab=GND")
        else:
            self.c("devices/lab_pin.sym", x, y, f"name=lp{self.n} sig_type=std_logic lab={net}")
    def two(self, sym, x, y, attrs, p, m):
        """Two-pin device with pins at (x, y-30) and (x, y+30)."""
        self.c(sym, x, y, attrs); self.lab(x, y - 30, p); self.lab(x, y + 30, m)
    def code(self, x, y, name, text):
        self.c("devices/code_shown.sym", x, y, f'name={name} only_toplevel=false value="{esc(text)}"')
    def save(self, path):
        open(path, "w").write("".join(self.o))

def sym_pins(path):
    pins = []
    for ln in open(path):
        if ln.startswith("B 5"):
            t = ln.split()
            x = (float(t[2]) + float(t[4])) / 2; y = (float(t[3]) + float(t[5])) / 2
            name = ln.split("name=")[1].split()[0].rstrip("}")
            pins.append((name, x, y))
    return pins

SETUP = """* CACE testbench {tb} for dac6_1v8
* CACE{{filename}}_CACE{{N}}: corner CACE{{corner}}, CACE{{temperature}} C
.lib CACE{{PDK_ROOT}}/CACE{{PDK}}/libs.tech/combined/sky130.lib.spice CACE{{corner}}
.include CACE{{DUT_path}}
.option TEMP=CACE{{temperature}}
.option SEED=CACE[CACE{{seed=12345}} + CACE{{iterations=0}}]
.option warn=1
"""

DWELL_SLOW, DWELL = 30, 12      # µs per code: codes 0-3 settle slowly near the ground rail

def bitsrc_staircase():
    """Digital inputs for a slow code staircase 0, 1, ..., 63 (one code change every DWELL
    microseconds, DWELL_SLOW for codes 0 to 3). The bits are decoded from the voltage on
    node code. The script samples each code just before the next change."""
    t, pts = 0.0, ["0 0"]
    for k in range(64):
        t += DWELL_SLOW if k <= 3 else DWELL
        if k < 63:
            pts.append(f"{t:g}u {k} {t + 0.01:g}u {k + 1}")
    lines = ["* Six data bits decoded from the staircase voltage on node code",
             f"VCODE code GND PWL({' '.join(pts)})"]
    for n in range(6):
        a, b = 2 ** n, 2 ** (n + 1)
        lines.append(f"Bd{n} d{n} GND V={{CACE{{Vvdd}}*(floor((v(code)+0.5)/{a})-2*floor((v(code)+0.5)/{b}))}}")
    return "\n".join(lines) + "\n", t

def bitsrc_static():
    return "\n".join(f"Vd{n} d{n} GND DC CACE[CACE{{b[{n}]}} * CACE{{Vvdd}}]" for n in range(6)) + "\n"

def bitsrc_step():
    out = ["* Code steps from b to its complement (63 - b) at tstep"]
    for n in range(6):
        lo = f"CACE[CACE{{b[{n}]}} * CACE{{Vvdd}}]"
        hi = f"CACE[(1 - CACE{{b[{n}]}}) * CACE{{Vvdd}}]"
        out.append(f"Vd{n} d{n} GND PWL(0 {lo} 2u {lo} 2.001u {hi})")
    return "\n".join(out) + "\n"

def dut_tb(title, dutsym, vdd_value="DC CACE{Vvdd}", ena="DC CACE[CACE{ena} * CACE{Vvdd}]"):
    s = Sch(title)
    for name, x, y in sym_pins(dutsym):
        net = {"VSS": "GND", "VDDA": "vdd", "VOUT": "out", "VTAP": "tap"}.get(name, name.lower())
        s.lab(x, y, net)
    s.c("dac6_1v8.sym", 0, 0, "name=XDUT")
    s.two("devices/vsource.sym", -500, 300, f'name=Vvdd value="{esc(vdd_value)}" savecurrent=false', "vdd", "GND")
    s.two("devices/vsource.sym", -380, 300, f'name=Vrefh value="{esc("DC CACE{Vvdd}")}" savecurrent=false', "vrefh", "GND")
    s.two("devices/vsource.sym", -260, 300, 'name=Vrefl value="DC 0" savecurrent=false', "vrefl", "GND")
    s.two("devices/isource.sym", -140, 300, f'name=Ibias value="{esc("DC CACE{Ibias}")}"', "vdd", "ibias")
    s.two("devices/vsource.sym", -20, 300, f'name=Ven value="{esc(ena)}" savecurrent=false', "en", "GND")
    s.two("devices/res.sym", 300, 300, f"name=Rload value=CACE\\{{Rload\\}} m=1", "out", "GND")
    s.two("devices/capa.sym", 420, 300, f"name=Cload value=CACE\\{{Cload\\}} m=1", "out", "GND")
    return s

def main(out):
    here = os.path.dirname(os.path.abspath(__file__))
    dutsym = os.path.join(here, "..", "xschem", "dac6_1v8.sym")
    os.makedirs(out, exist_ok=True)

    # 1. Slow staircase through all 64 codes (static transfer function)
    stim, tstop = bitsrc_staircase()
    s = dut_tb("CACE testbench static_staircase: all 64 codes, settled", dutsym)
    s.code(-700, -600, "SETUP", SETUP.format(tb="static_staircase") + stim)
    s.code(600, -600, "CONTROL", f""".control
set wr_singlescale
set num_threads=1
tran 100n {tstop:g}u
let idd = -i(Vvdd)
let istring = -i(Vrefh)
wrdata CACE{{filename}}_CACE{{N}}.data v(code) v(out) v(tap) idd istring
quit
.endc
""")
    s.save(f"{out}/static_staircase.sch")

    # 2. DC operating point at one code
    s = dut_tb("CACE testbench dc_op: one code, DC", dutsym)
    s.code(-700, -600, "SETUP", SETUP.format(tb="dc_op") + bitsrc_static())
    s.code(600, -600, "CONTROL", """.control
set wr_singlescale
set num_threads=1
op
let idd = -i(Vvdd)
let istring = -i(Vrefh)
wrdata CACE{filename}_CACE{N}.data v(out) idd istring
quit
.endc
""")
    s.save(f"{out}/dc_op.sch")

    # 3. Code step transient
    s = dut_tb("CACE testbench tran_step: code b to 63 - b at 2 us", dutsym)
    s.code(-700, -600, "SETUP", SETUP.format(tb="tran_step") + bitsrc_step())
    s.code(600, -600, "CONTROL", """.control
set wr_singlescale
set num_threads=1
tran 5n CACE{Tstop}
let idd = -i(Vvdd)
wrdata CACE{filename}_CACE{N}.data v(out) idd
quit
.endc
""")
    s.save(f"{out}/tran_step.sch")

    # 4. Supply rejection with the references held at their DC value
    s = dut_tb("CACE testbench psrr: AC on VDDA only, references fixed", dutsym,
               vdd_value="DC CACE{Vvdd} AC 1")
    s.code(-700, -600, "SETUP", SETUP.format(tb="psrr") + bitsrc_static())
    s.code(600, -600, "CONTROL", """.control
set wr_singlescale
set num_threads=1
ac dec 10 1 100Meg
let psrr = -db(v(out))
wrdata CACE{filename}_CACE{N}.data psrr
quit
.endc
""")
    s.save(f"{out}/psrr.sch")

    # 5. Open-loop gain of the buffer amplifier (loop broken with a large L and C)
    s = Sch("CACE testbench ac_loop: buffer loop gain, loop broken at INM")
    otasym = os.path.join(out, "buffer_ota.sym")
    for name, x, y in sym_pins(otasym):
        net = {"VSS": "GND", "VDD": "vdd", "INP": "inp", "INM": "inm", "OUT": "out", "IBIAS": "ibias"}[name]
        s.lab(x, y, net)
    s.c("buffer_ota.sym", 0, 0, "name=XOTA")
    s.two("devices/vsource.sym", -500, 300, f'name=Vvdd value="{esc("DC CACE{Vvdd}")}" savecurrent=false', "vdd", "GND")
    s.two("devices/isource.sym", -380, 300, f'name=Ibias value="{esc("DC CACE{Ibias}")}"', "vdd", "ibias")
    s.two("devices/vsource.sym", -260, 300, f'name=Vin value="{esc("DC CACE{Vin}")}" savecurrent=false', "inp", "GND")
    s.two("devices/ind.sym", 300, -300, "name=Lbreak value=1T m=1", "out", "inm")
    s.two("devices/capa.sym", 420, -300, "name=Cbreak value=1T m=1", "inm", "acin")
    s.two("devices/vsource.sym", 540, -300, 'name=Vac value="DC 0 AC 1" savecurrent=false', "acin", "GND")
    s.two("devices/res.sym", 300, 300, "name=Rload value=CACE\\{Rload\\} m=1", "out", "GND")
    s.two("devices/capa.sym", 420, 300, "name=Cload value=CACE\\{Cload\\} m=1", "out", "GND")
    s.code(-700, -600, "SETUP", SETUP.format(tb="ac_loop"))
    s.code(700, -600, "CONTROL", """.control
set wr_singlescale
set num_threads=1
ac dec 40 0.1 1G
let lg = -v(out)/v(inm)
let lg_db = db(lg)
let lg_ph = 180/pi*cph(lg)
wrdata CACE{filename}_CACE{N}.data lg_db lg_ph
quit
.endc
""")
    s.save(f"{out}/ac_loop.sch")

if __name__ == "__main__":
    main(sys.argv[1])
