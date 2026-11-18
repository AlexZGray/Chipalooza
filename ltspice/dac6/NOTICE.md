# Model attribution

`MCP6001.txt` is the teaching macromodel attributed in its header to **Peter Cheung, 24 September 2024, version 1.2**. The accompanying `MCP6001.asy` symbol and the model were copied unchanged from the existing LTspice teaching setup used for this demonstrator. The original model header and authorship are preserved.

This is a simplified teaching model, not a Microchip manufacturer macromodel or a Sky130 transistor-level amplifier. Its limitations and modeled offset are described in the [design guide](README.md#5-output-buffer).

`DAC6_Models.lib` contains illustrative Level-1 CMOS equations and is not a foundry PDK. The local hierarchy symbols and schematics are included so this reference runs without installing a global symbol library. The four-terminal CMOS transmission-gate and inverter cells reuse the earlier Chipalooza mux demonstration geometry.

This addition does not assign a new repository-wide license or replace the attribution on supplied teaching materials.
