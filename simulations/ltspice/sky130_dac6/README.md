# Sky130 buffered 6-bit resistor-string DAC

A **pre-layout transistor design** using pinned SkyWater foundry BSIM models, physical poly-resistor models and a physical MIM-capacitor model. The integrated amplifier contains 23 MOS instance groups. All on-chip switches, level shifters, inverters and analogue components use Sky130 devices.

**Start here:** open **[DAC6_Sky130_Top.asc](DAC6_Sky130_Top.asc)** in LTspice and select **Run**. The complete folder must stay together. No PDK installation, global symbol installation or Python package is needed to run the schematics. Verified with LTspice 26.1.1.

Read the **[design calculations, buffer margin and measured results](docs/Design_Report.md)**. Model provenance, compatibility changes and licensing are in **[NOTICE.md](NOTICE.md)**.

## Examples

| Sheet | Purpose |
|---|---|
| [DAC6_Sky130_Top.asc](DAC6_Sky130_Top.asc) | All 64 codes, major carries, large steps and reset; updates while enabled provide an additional stress test |
| [DAC6_Sky130_Core.asc](DAC6_Sky130_Core.asc), [.asy](DAC6_Sky130_Core.asy) | Reusable DUT with the v2 proposal's external ports; run it from a parent testbench |
| [DAC6_Sky130_Integration.asc](DAC6_Sky130_Integration.asc) | The complete simulation using one reusable core instance |
| [DAC6_Sky130_Tap_Probe.asc](DAC6_Sky130_Tap_Probe.asc) | Nominal 64-code test with an external 10 MΩ / 10 pF VTAP probe |
| [DAC6_Sky130_Protocol.asc](DAC6_Sky130_Protocol.asc) | All codes with EN low before changing data and at least 5 µs data setup before enable |
| [DAC6_Sky130_Min_Supply.asc](DAC6_Sky130_Min_Supply.asc) | SS, 110 °C, VDDA 3.135 V, VDDD 1.71 V, 0.8 µA bias |
| [DAC6_Sky130_Protocol_Min.asc](DAC6_Sky130_Protocol_Min.asc) | The same low-supply condition with the host protocol |
| [DAC6_Sky130_Hot_Fast.asc](DAC6_Sky130_Hot_Fast.asc) | FF, 110 °C, high supplies and 1.2 µA bias |
| [DAC6_Sky130_Cold_Skew.asc](DAC6_Sky130_Cold_Skew.asc) | SF, −40 °C, high analogue supply, low digital supply and low bias |
| [DAC6_Sky130_Overload.asc](DAC6_Sky130_Overload.asc) | Intentional 1 kΩ overload; the output is expected to fail its voltage target |
| [Buffer_Step.asc](Buffer_Step.asc) | Standalone physical buffer, full-scale steps into 100 kΩ / 20 pF |
| [Buffer_Range.asc](Buffer_Range.asc) | Slow excursion to both rails, showing where tracking fails |
| [Buffer_DC.asc](Buffer_DC.asc), [Buffer_DC_Low.asc](Buffer_DC_Low.asc) | DC sweeps starting at the middle operating point |
| [Buffer_AC.asc](Buffer_AC.asc), [Buffer_AC_Worst.asc](Buffer_AC_Worst.asc) | Loop gain at nominal and a combined MOS/RC corner |

Right-click a block to open its child schematic. The default waveform profile plots the tap, buffer input, output and digital controls. Plot `-V(out)/V(fb)` in the AC examples to obtain loop gain, including its phase. `V(out)` alone in that test is the response to the feedback injection source.

## Change conditions

Edit the parameters on a top-level sheet. Device-wrapper dimensions are numbers in micrometres, for example `w=7 l=8`; the adapters perform the SI conversion. `TEMP_C` controls both `.temp` and `PDK_TEMP`; keep these linked because the portable resistor expressions use the latter. Resistor temperature coefficients retain the native model's 27 °C default nominal temperature; MOS cards retain their own nominal temperature.

Change the `.include models/sky130_tt.lib` directive to select `tt`, `ff`, `ss`, `fs` or `sf`. The supplied corner examples select their own model file. Their PWL files also use the corresponding digital voltage; changing `DVDD` alone does not rescale a file-based stimulus. The `stimulus/1p71` and `stimulus/1p89` folders provide the two endpoint levels.

The amplifier's `mult` values represent parallel **7 µm unit fingers**, with the displayed length. Keep that geometry when laying out the design; replacing a finger bank by one very wide transistor can select a different model bin and changes matching and parasitics.

## Reproduce the checks

After running the main sheet, a standard-library-only checker verifies its measured behaviour:

```sh
python3 verify_results.py
```

Run the four normal/corner examples, the overload and the two protocol examples, then check the complete LTspice transient set:

```sh
python3 verify_results.py --all --protocol
```

After also running Integration and Tap_Probe, append `--integration` to check them and compare the reusable core's output against the architecture sheet.

The [reference measurements](results/reference_ltspice.json) and [code-by-code data](results/reference_Top_codes.csv) are committed. Checkers write separate `latest*` files.

The Top and Integration sheets were also run from a fresh package extracted into a folder with spaces in its name. [The portability check](results/reference_portability.json) records their passing measurements and hashes of the 132 runnable input files.

For the **540-point LTspice stability matrix**, open and run the 25 `validation/LT_AC_*.cir` files. Each has one AC analysis and a parameter step. The matrix uses LTspice's alternate solver (`solver=alt`). Install the optional Python dependencies and check the resulting RAW files:

```sh
python3 -m pip install -r validation/requirements.txt
python3 validation/analyse_lt_ac.py
```

The matrix models retain the original foundry cards for the geometries used by the buffer. This speeds parameter stepping. The full DAC uses the complete selected-family libraries. To rebuild the matrix files after changing the model set:

```sh
python3 tools/make_ac_matrices.py
```

Additional cross-checks use ngspice, including 85 slow range tests, 120 midpoint AC tests, 60 midpoint RC-corner tests and independent 100-seed amplifier/string mismatch screens:

```sh
python3 validation/run_checks.py --suite all
python3 validation/check_rc_settling.py
```

The mismatch screen resets the circuit after setting each seed, then samples amplifier codes after 80 µs in a 100 µs dwell. This keeps parameter randomisation reproducible and separates static matching from the dedicated timing tests.

Use `--ngspice /path/to/ngspice` if it is not on the search path. `--runs` changes the mismatch sample count. The ngspice AC screen intentionally uses the middle input; the LTspice matrix covers all three selected input levels. Generated simulations stay in `validation/.work`.

## Scope

The [core interface](interface.json) follows proposal v2: D5–D0 and EN, three shared analogue signals VREFH/VREFL/VTAP, one requested dedicated VOUT pad, and a 1 µA bias. It allocates no digital status output. EN_MON is an internal inspection node. In the testbenches, `TAP` and `OUT` denote VTAP and VOUT. The optional masked-update examples supplement the enabled code-change tests; masking is not required.

The supplies, external references, external harness bias, input patterns, board decoupling and specified output load are test fixtures. They are intentionally ideal. The shared-reference harness switches are outside the model; their voltage drop is unverified. The on-chip circuit contains no generic MOS model, ideal switch or op-amp macromodel.

This is an implementation for pre-layout design and review. Pad/ESD behaviour, extracted interconnect and well parasitics, actual harness supply/bias models, power sequencing, combined statistical yield and physical slot fit still require qualification. The [report](docs/Design_Report.md) distinguishes measured results from provisional design allowances.
