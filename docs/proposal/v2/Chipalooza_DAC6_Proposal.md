# Chipalooza Challenge #4 Proposal: Buffered 6-Bit Resistor-String DAC

**Team name:** [TEAM NAME] · **ICARUS team number:** [TO BE ASSIGNED]

Attachments sent separately: list of test equipment, designer CVs.

## 1. Type of IP block

A voltage-output, 6-bit resistor-string DAC with an integrated unity-gain output buffer, in Sky130. It is intended for low-frequency set points inside an SoC: programmable comparator thresholds, trim and calibration voltages, and bias set points.

## 2. Functional description

- **Resistor string:** 64 matched unit resistors between the external references VREFH and VREFL. The resistor string is inherently monotonic.
- **Tap selector:** a 6-level binary tree of CMOS transmission gates, with one level per data bit, so no decoder is needed. The selected tap is $VTAP = VREFL + D × \frac{VREFH − VREFL}{64}$, for D = 0 to 63.
- **Level shifters:** seven cross-coupled level shifters convert D5–D0 and EN from 1.8 V logic into complementary 0 / 3.3 V switch drives.
- **Output buffer:** a Sky130 transistor-level op-amp in unity-gain feedback. It isolates the high-impedance string (up to about 16 kΩ at mid-code) from the load.
- **Enable:** with EN high, the selected tap drives the buffer. With EN low, the buffer input switches to VREFL, giving a defined low output. The string and buffer remain powered.

Codes may be changed while EN is high. Brief glitches at multi-bit transitions are expected.

## 3. I/O list and harness resources

| Pin | Type | Harness resource | Notes |
|---|---|---|---|
| D5–D0 | Digital in, 1.8 V | 6 control inputs | D5 = MSB |
| EN | Digital in, 1.8 V | 1 control input | May map to the per-block harness enable |
| VREFH | Analog in | Shared analog line | Sources the string current, about 42 µA |
| VREFL | Analog in | Shared analog line | Must sink the string current |
| VTAP | Analog test out | Shared analog line | Unbuffered tap voltage; test use only, needs a ≥10 MΩ meter |
| VOUT | Analog out | 1 dedicated pad (requested) | Buffered output; must not be shared |
| IBIAS | Bias in | 1 mirrored current, 1 µA | Bias for the buffer |
| VDDA / VDDD / VSS | Power | Per-slot switch | 3.3 V analog, 1.8 V digital |

**Total:** 7 of 24 control inputs, 0 status outputs, 3 of 4 shared analog lines, 1 dedicated pad, and 1 bias current. The voltage drop across a shared-line switch at 42 µA is about 0.2 mV (about 0.005 LSB), so placing the references on shared lines costs essentially no accuracy. VTAP lets us measure string linearity and buffer offset (VOUT − VTAP) separately. It is also a usable unbuffered fallback output.

## 4. Target specification

Conditions: VREFL = 0.300 V, VREFH = 3.000 V, load 100 kΩ ∥ 20 pF (including pad, package, and fixture), over the operating range below unless noted. 1 LSB = 42.1875 mV. Errors are referred to the measured reference voltages.

| Parameter | Min | Typ | Max | Unit |
|---|---|---|---|---|
| VDDA | 3.135 | 3.3 | 3.465 | V |
| VDDD | 1.71 | 1.8 | 1.89 | V |
| Temperature | −20 | 25 | 110 | °C |
| IBIAS | 0.8 | 1.0 | 1.2 | µA |
| Resolution | | 6 | | bit |
| Output range (code 0 to 63) | | 0.300 to 2.958 | | V |
| Absolute error, every code | −0.5 | | +0.5 | LSB |
| DNL | −0.5 | | +0.5 | LSB |
| INL (endpoint fit) | −0.5 | | +0.5 | LSB |
| Monotonicity | Guaranteed | | | |
| Settling after a code change, to ±0.5 LSB | | 10 | 20 | µs |
| Reference current | | 42.2 | 60 | µA |
| IDDA (excluding reference current) | | 0.3 | 1.0 | mA |
| IDDD (static) | | 5 | 50 | µA |

**Absolute limits:**
- VDDA: 0 to 3.6 V. VDDD: 0 to 1.95 V.
- References and VOUT: between VSS and VDDA, with VREFL < VREFH.
- Digital inputs: between VSS and VDDD.
- VOUT must not be driven or shorted.
- IBIAS: ≤ 2 µA.

The Sky130 device and pad ratings take precedence over these limits.

## 5. Simulation to date

An LTSpice model of the architecture (64-resistor string, the transmission-gate tree, the level shifters, and enable selector) was run. These use generic Level-1 CMOS models, not Sky130 models. The buffer is the MCP6001 teaching macromodel.

| Result | Value | What it shows |
|---|---|---|
| All 64 codes, monotonic | Pass; minimum step 42.187 mV | The tree and level-shifter logic select correctly |
| Worst absolute error | 0.107 LSB (4.5 mV) | Almost all of this is the macromodel's built-in 4.5 mV offset. It sets the scale of the buffer-offset budget |
| DNL / INL | ≈ 0 | Expected with ideal, identical resistors. Silicon DNL/INL will depend on how well the Sky130 poly resistors match. |
| Worst settling (tested transitions, including 31↔32 and 0↔63) | 6.2 µs | With a 1 MHz amplifier, the 20 µs target leaves margin |
| 100 kΩ load placed directly on the tap | 267 mV error (≈ 6 LSB) | The buffer is necessary |
| 1 kΩ output load | Code 63 clips to 2.54 V | Shows the output-drive limit. A 1 kΩ load is outside the specified load range |

These results validate the architecture and control logic only. The next step is to port the design to Xschem and ngspice with Sky130 devices, and to design the transistor-level buffer. The buffer is the main design task: it must accept inputs from 0.3 to 3.0 V on a 3.135 V supply and stay stable into 20 pF.

## 6. Basis for the chosen values

Several values are starting points, to be confirmed or revised against Sky130 simulation before the schematic review:

- **0.3 V and 3.0 V references:** chosen to keep the buffer 0.3 V away from each rail at nominal supply. At VDDA = 3.135 V, the top code leaves only about 0.18 V of headroom for the buffer output. If the buffer cannot meet spec there, we will lower VREFH (for example to 2.7–2.8 V), or specify the top codes at nominal supply only.
- **1 kΩ unit resistor (64 kΩ total):** sets a 42 µA reference current. This is a starting balance between reference current, resistor area, and settling. A higher resistance (for example 256 kΩ, about 10 µA) remains an option.
- **±0.5 LSB accuracy and 20 µs settling:** standard targets for a 6-bit DAC, set with margin above the LTspice results. They are not derived from a specific application requirement.
- **100 kΩ ∥ 20 pF load:** represents a typical on-chip or bench input. 20 pF is our estimate of the pad, package, and fixture capacitance.
- **Supply tolerance (±5%) and temperature range:** assumed until the harness documentation is published.
- **IDDA estimate and 1 µA bias:** the IDDA figure comes from first hand calculations for a two-stage op-amp. The 1 µA bias follows the harness guidance.
- **Transistor sizes in the LTspice model:** illustrative only, not the final Sky130 sizing.

## 7. Test plan outline

| Test | Method | Pass criterion |
|---|---|---|
| Function | Step through all 64 codes over SPI; toggle EN | Correct level for each code; EN low gives VREFL |
| Transfer, DNL, INL | Precision DMM on VOUT, VREFH, and VREFL; sweep codes up and down; allow ≥ 1 ms per code | Absolute error, DNL, and INL within spec; monotonic |
| Buffer vs. string | Measure VTAP (≥ 10 MΩ input) and VOUT at each code | Separates resistor mismatch from buffer offset |
| Settling and glitches | Oscilloscope on VOUT; code steps 0↔63 and 31↔32, triggered on the output step | Settling ≤ 20 µs; glitch amplitude reported |
| Load | Repeat transfer at 100 kΩ and 1 MΩ, with 20 pF total | Within spec |
| Supply and reference current | SMU on VDDA, VDDD, VREFH, and VREFL; sweep IBIAS over its range | Within spec; stable across the IBIAS range |
| Temperature and supply | Repeat transfer and current tests at the supply and temperature extremes available | Report against spec |

The references are driven by a source/measure unit. A plain bench supply cannot sink the VREFL current.
