# Sky130 1.8 V buffered DAC

**Use LTspice 26.** On macOS, launch `LTspice 26.app` from Applications and use **File → Open** to open [DAC6_Sky130_Top.asc](DAC6_Sky130_Top.asc). The older `LTspice.app` (17.2.4) reports a missing core symbol with this folder layout. Keep this folder together and click **Run**. Click **OUT** for the buffered voltage or **TAP** for the selected ladder voltage. The run sweeps all 64 codes, then tests full-range steps and enable. The supply ramps up at the start of the simulation.

The logic and analogue circuitry share one supply. The resistor string runs from ground to that supply, so the output scales with it. At 1.8 V, the ideal step is **28.125 mV** and the highest code is **1.771875 V**. A PMOS and NMOS input pair let the unity-gain buffer sense taps near both rails.

## Change the test

Right-click the `.param` lines at the bottom of the top sheet.

| Parameter | What it changes | Default |
| --- | --- | --- |
| `VDD_V` | Supply, logic high and upper DAC reference | 1.8 V |
| `IREF`, `TEMP_C` | Buffer bias current and temperature | 1 µA, 25 °C |
| `RL`, `CL` | Output load resistance and capacitance | 100 kΩ, 20 pF |
| `CCOMP` | Nominal Miller compensation capacitance | 45 pF |
| `RCOMP_L` | Length of the compensation resistor, in µm | 2.2 |

To change process corner, edit `.include models/sky130_tt.lib` and replace `tt` with `ss`, `ff`, `sf`, or `fs`. For a test that disables the buffer path during code changes, change `enable.txt` to `enable_masked.txt` on the `VEN` source. EN connects the buffer input to ground while low.

## Top-level results

All 64 codes were monotonic and within ±½ LSB in these LTspice 26.1.1 runs on macOS. Settling excludes the initial power-up ramp.

| Test | Code 0 | Code 63 | Largest settled error | Worst settling |
| --- | ---: | ---: | ---: | ---: |
| TT, 1.8 V, 25 °C | 3.26 mV | 1.77068 V | 3.26 mV | 9.15 µs |
| SF, 1.71 V, −20 °C | 3.05 mV | 1.67998 V | 3.30 mV | 12.45 µs |
| SS, 1.71 V, 110 °C | 3.98 mV | 1.68133 V | 3.98 mV | 14.06 µs |

## Compensation

The table is from LTspice 26.1.1 buffer runs with **100 kΩ ∥ 20 pF**. Phase margin is the nominal minimum across seven input voltages. Settling is the slower direction of the full-range step into the ideal ±½ LSB band.

| CCOMP | Nominal phase margin | Nominal settling | SF at 1.71 V, −20 °C |
| ---: | ---: | ---: | ---: |
| 20 pF | 51.9° | 3.11 µs | |
| 30 pF | 62.4° | 4.57 µs | 8.08 µs |
| **45 pF** | **71.5°** | **7.31 µs** | **12.27 µs** |
| 60 pF | 76.8° | 10.04 µs | 16.44 µs |

At 1.71 V and 110 °C (SS), 30 pF gave 59.7° and 45 pF gave 69.0°. The larger capacitor slows the loop and improves margin. **45 pF** gives margin above 60° in the sampled cases and settles faster than 60 pF. These are pre-layout results.

## Folders

- `blocks/` contains the child schematics and symbols. Right-click **XCORE** to see the DAC circuit.
- `models/` contains the Sky130 device libraries and LTspice adapters.
- `stimulus/` contains the time patterns for the six data inputs and enable.
