# Sky130 buffered 6-bit DAC

Open [DAC6_Sky130_Top.asc](DAC6_Sky130_Top.asc) in LTspice and click **Run**. Keep the whole `sky130_dac6` folder together. Click **OUT** to plot the buffered output or **TAP** to plot the selected resistor tap.

## Change the test

In the top sheet, right-click the `.param` lines at the bottom and edit the values you want to change. Click **Run** again to see the result.

| Parameter | What it changes | Default |
| --- | --- | --- |
| `AVDD` | Analogue supply voltage | 3.3 V |
| `DVDD` | Digital supply voltage and input logic high level | 1.8 V |
| `IREF` | Buffer bias current | `1u` (1 µA) |
| `TEMP_C` | Simulation temperature | 25 °C |
| `REF_L`, `REF_H` | Low and high DAC reference voltages | 0.3 V, 3.0 V |
| `RL`, `CL` | Output load resistance and capacitance | `100k` (100 kΩ), `20p` (20 pF) |

For example, change `RL=100k` to `RL=10k` to try a heavier load.

To change the process corner, edit `.include models/sky130_tt.lib`. Replace `tt` with `ss`, `ff`, `sf`, or `fs`. Leave the separate adapter include in place.

To disable the DAC while the input code changes, right-click the `VEN` source and change `enable.txt` to `enable_masked.txt` in the file path.

## Folders

- `blocks/` contains the DAC child schematics and their symbols. Right-click **XCORE** in the top sheet to see the circuit inside.
- `models/` contains the Sky130 device libraries and their LTspice adapters.
- `stimulus/` contains the input waveforms for the six data bits and the enable signal.
