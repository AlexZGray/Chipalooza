# Sky130 1.8 V DAC for LTspice 17

Extract the ZIP and keep the folder together. Open [DAC6_Sky130_Top.asc](DAC6_Sky130_Top.asc) in LTspice 17.2.4 on macOS, then click **Run**. Click **OUT** to plot the buffered voltage or **TAP** for the selected resistor tap.

The child schematics and symbols sit beside the top sheet so LTspice 17 can find them. The model files use resistor expressions compatible with LTspice 17. The circuit and test sequence are the same as in the LTspice 26 version.

## Change the test

Edit the `.param` lines on the top sheet. `VDD_V` sets the supply and the upper DAC reference. `RL` and `CL` set the output load. `IREF` and `TEMP_C` set the bias and temperature. `CCOMP` sets the compensation capacitor and defaults to 45 pF.

The `models` folder contains the Sky130 libraries. The `stimulus` folder contains the input and enable waveforms.

## Verified run

The top sheet completed in LTspice 17.2.4 on macOS in about five minutes, including model loading. At 1.8 V with the default load, output increased at every code, from 3.26 mV to 1.77068 V. The largest nominal DC error was 3.26 mV, and the longest settling time after startup was 9.15 µs to within ±½ LSB of the settled value.
