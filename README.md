# Chipalooza

A **buffered 6-bit resistor-string DAC** for Chipalooza Challenge #4 in Sky130 CMOS.

## Run the Sky130 design

1. Clone the repository or download and extract its ZIP archive.
2. Install [LTspice](https://www.analog.com/ltspice).
3. Open **[DAC6_Sky130_Top.asc](simulations/ltspice/sky130_dac6/DAC6_Sky130_Top.asc)** and choose **Run**.

Keep the complete `simulations/ltspice/sky130_dac6` folder together. Models, local symbols, child schematics, plot settings and stimuli are included. No separate PDK installation is needed. The examples were tested with LTspice 26.1.1.

**[Setup, examples and reproducible checks →](simulations/ltspice/sky130_dac6/README.md)**

**[Circuit stages, hand calculations, buffer margin and results →](simulations/ltspice/sky130_dac6/docs/Design_Report.md)**

This version uses actual pinned Sky130 BSIM models for the amplifier, transmission gates, level shifters and digital inverters. The string and compensation components use foundry poly-resistor and MIM-capacitor models. It is a **pre-layout implementation**; extracted layout and harness qualification remain necessary before tapeout.

## Initial proposal

**[Proposal documents and editable versions →](docs/proposal/README.md)**

The latest simplified proposal (v2), original proposal package (v1), and provisional equipment attachment remain available. Team details are placeholders. Proposal targets are distinguished from measured pre-layout results in the current design report.

## Earlier teaching example

The original [generic CMOS/MCP6001 demonstrator](simulations/ltspice/dac6/README.md) is retained for comparison. Its results describe that earlier model set. Use the Sky130 folder above for the current transistor design.

Generated waveforms, logs and working simulation files are excluded from Git. Committed reference measurements can be compared with freshly generated `latest*` results.
