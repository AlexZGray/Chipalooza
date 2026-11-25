# Sky130 1.8 V DAC: CACE characterization with ngspice

This folder runs the 1.8 V rail-to-rail DAC from [`../sky130_1v8logic`](../sky130_1v8logic) through [CACE](https://github.com/efabless/cace) with ngspice. Everything here is open source: xschem schematics, ngspice, the Sky130 models from SkyWater's open PDK, and Python. Only schematic (pre-layout) netlists are used, so CACE skips Magic, KLayout, Netgen and other layout steps.

The results are in [`../../docs/sky130_1v8logic_ngspice_results.md`](../../docs/sky130_1v8logic_ngspice_results.md).

## Folder layout

| Path | Contents |
| --- | --- |
| `xschem/` | xschem schematics and symbols of every block. `dac6_1v8.sch` is the DAC core (`DAC6_Sky130_Core` in LTspice) and is the CACE device under test. |
| `cace/dac6_1v8.yaml` | CACE datasheet: pins, conditions, parameters and limits. |
| `cace/templates/` | Testbench schematics. CACE fills in the `CACE{...}` values for each run. |
| `cace/scripts/` | Python post-processing: INL, DNL, errors, settling, loop gain and PSRR. |
| `cace/results/` | CACE summary tables from the runs behind the results file. |
| `reference/circuit.lib` | SPICE netlist read from the LTspice block schematics. It is the source for `xschem/`. |
| `tools/` | Scripts that build the files above and the extra graphs. |

`runs/`, `netlist/` and `docs/` are created by CACE when it runs.

## How the schematics were made

The LTspice schematics stay the design source. Two scripts carry them into xschem.

1. `tools/asc2net.py` reads `../sky130_1v8logic/blocks/*.asc` and writes `reference/circuit.lib`.
2. `tools/gen_xschem.py` turns each subcircuit into an xschem `.sch`/`.sym` pair. It places the Sky130 PDK symbols (`nfet_01v8`, `pfet_01v8`, `res_high_po_0p69`, `cap_mim_m3_1`) with the same W, L and multiplier as the LTspice adapters, and connects nets with labels.

`tools/compare_netlists.py` netlists the xschem schematics and checks every device, net, size and pin order against `reference/circuit.lib`. All 14 cells and 79 device or block instances match. If you edit the LTspice design, rerun both scripts and the check:

```bash
python3 tools/asc2net.py ../sky130_1v8logic/blocks reference/circuit.lib
python3 tools/gen_xschem.py reference/circuit.lib xschem
cd xschem && xschem -n -s -r -x -q -o /tmp/nl -N dac6_1v8.spice dac6_1v8.sch && cd ..
python3 tools/compare_netlists.py reference/circuit.lib /tmp/nl/dac6_1v8.spice
```

The testbench schematics come from `tools/gen_testbenches.py`.

## Running CACE

You need ngspice (version 42 was used), xschem, Python 3.10 or newer, and CACE (`pip install cace`).

You also need the Sky130 PDK. With a full install from [ciel](https://github.com/fossi-foundation/ciel) or volare, set `PDK_ROOT` to its folder and `PDK=sky130A`.

If a full install is not possible, `tools/make_pdk_subset.sh` builds a small `PDK_ROOT` instead. It clones two repositories: the xschem Sky130 symbols, and SkyWater's device models (`skywater-pdk-libs-sky130_fd_pr`). From the models it builds the ngspice corner libraries for the devices this design uses. The results in `docs/` were made with this subset because the CI machine could not download a full PDK. Its TT, SS and SF libraries give the same LTspice-matched results as the libraries in `../sky130_1v8logic/models`, to the microvolt.

```bash
tools/make_pdk_subset.sh ~/pdk_subset          # only if there is no full sky130A install
export PDK_ROOT=~/pdk_subset PDK=sky130A
cd cace
cace dac6_1v8.yaml -s schematic -j 2           # all parameters, about 1.5 hours on 2 cores
cace dac6_1v8.yaml -s schematic -p static_nominal   # one parameter, a few minutes
python3 ../tools/make_plots.py ../runs/RUN_<date> ../../../docs/sky130_1v8logic_ngspice
```

CACE writes `runs/RUN_<date>/summary.md` (the summary table) and a plot for each `plot:` entry under `runs/RUN_<date>/parameters/<parameter>/`.

Two xschem notes:

- `xschem/xschemrc` sets `lvs_netlist 1`. CACE asks for a `.subckt` wrapper around the top cell with `top_is_subckt`, which xschem 3.4.4 does not know. `lvs_netlist` gives the same wrapper.
- The ngspice control blocks set `num_threads=1`, so two parallel CACE jobs fit on two cores.

## Testbenches

| Template | What it does |
| --- | --- |
| `static_staircase.sch` | Steps the code 0, 1, …, 63 in a transient and holds each code until the output settles: 30 µs for codes 0 to 3, 12 µs for the rest. The script reads each code just before it changes. A DC sweep would be faster, but it sometimes reached a false operating point at code 1 (VOUT about 0.5 V); a transient at the same corner settles correctly. The `unsettled` result checks that the output moved less than 0.05 LSB in the last 2 µs of every code. |
| `dc_op.sch` | Operating point at one code, used for the EN-low test. |
| `tran_step.sch` | Switches the code from `b` to `63 - b` at 2 µs: full-scale steps (0↔63) and midscale steps (31↔32). |
| `ac_loop.sch` | Opens the buffer loop at the inverting input with a 1 TH inductor and a 1 TF capacitor. It measures the loop gain of `Sky_OTA` with the DAC load. |
| `psrr.sch` | Puts AC on VDDA while VREFH stays at its DC value. This measures the buffer's supply rejection apart from the intended ratiometric tracking. |

VREFH has its own source at the VDDA voltage in every testbench. It is the same voltage as in the design, and it lets CACE read the string current on its own.
