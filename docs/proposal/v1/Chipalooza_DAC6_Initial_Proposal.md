# Buffered six bit resistor string DAC

We propose a reusable voltage output digital to analogue converter in Sky130 CMOS, combining a six bit resistor string, CMOS tap selection and an integrated output buffer. The block is intended for programmable sensor thresholds, calibration voltages and low frequency analogue set points within a system on chip.

The proposed operating point is a 3.3 V analogue supply, 1.8 V digital controls and externally supplied 0.3 V and 3.0 V references. The output will provide 64 monotonic levels into a specified high impedance load. The principal targets are ±0.5 LSB absolute transfer error and settling within 20 µs under the conditions defined below.


## 1 Functional description


A continuous string of 64 matched resistor sections divides the reference span. A six stage tree of complementary NMOS and PMOS transmission gates selects one tap according to D5 to D0. Level shifters provide the 3.3 V gate drives from the 1.8 V control interface. A unity gain amplifier isolates the string from the output load.

Figure 1  Proposed IP architecture. EN_MON and the harness bias interface are planned additions to the functional demonstrator.

EN high connects the selected tap to the buffer. EN low connects the buffer input to VREFL, giving a defined low end output while the buffer and string remain powered. There is no tri-state output or power-down mode. An integrated precision reference, serial interface and low glitch waveform synthesis are outside the proposed scope.

Videal = VREFL + (D / 64) × (VREFH − VREFL)

D is an unsigned code from 0 to 63. At the nominal references, 1 LSB is 42.1875 mV; the ideal output is 0.300000 V at code 0 and 2.9578125 V at code 63. The upper reference itself is not selected. A nominal 64 kΩ string draws 42.1875 µA from VREFH into VREFL; the lower reference source must be able to sink this current.


## Initial evidence and design status


The hierarchical LTspice demonstrator has passed all 64 codes, monotonicity, enable/reset and selected large-step and major-carry tests. At nominal supplies and LTspice’s 27 °C default, it shows 0.107 LSB maximum settled error and approximately 6.2 µs worst settling among the tested stress transitions into 100 kΩ and 20 pF. Deliberate heavy-load and unbuffered-tap loading failures were also verified.

These are architecture-level results using identical resistors, generic CMOS and a supplied MCP6001 teaching macromodel. They do not establish Sky130 performance. The submitted IP will replace the macromodel with a transistor-level amplifier and use foundry devices, extracted parasitics and mismatch verification.


## 2 Interfaces and harness resource request


We request three standard dedicated analogue pads for the two references and buffered output. The digital data and enable use the harness control interface. EN_MON is a 1.8 V copy of the IP enable input, exported through one digital test channel as a timing reference. No custom pad is proposed.

| Port | Domain and direction | Function and proposed access |

| --- | --- | --- |

| D5 to D0 | 6 digital inputs 1.8 V | Unsigned parallel input code; D5 is the most significant bit. Harness control inputs. |

| EN | 1 digital input 1.8 V | Active high conversion enable. Low resets the buffer input to VREFL. Harness control input. |

| EN_MON | 1 digital test output 1.8 V | Buffered copy of EN at the IP boundary. Selected harness test route for timing measurements. |

| VREFH | Analogue input | Nominal 3.0 V upper reference. Dedicated standard analogue pad. |

| VREFL | Analogue input | Nominal 0.3 V lower reference. Dedicated standard analogue pad; external source must sink ladder current. |

| VOUT | Analogue output | Buffered DAC output. Dedicated standard analogue pad; specified load to VSSA. |

| IBIAS | Analogue bias input | One harness bandgap referenced current source, nominal 1 µA into the block, for local amplifier bias mirrors. No dedicated signal pad. |

| VDDA and VDDD | Supply inputs | 3.3 V analogue and 1.8 V digital supplies from the slot. |

| VSSA and VSSD | Supply returns | Analogue and digital grounds, connected according to the approved wrapper. |



Resource totals are seven digital control inputs, one digital test output, zero shared analogue lines, three dedicated analogue pads and one bias current source. No harness voltage reference or second current source is assumed. This is within the published Challenge 4 numerical resource budget; final allocation, pad types and wrapper mapping remain subject to organiser agreement [1].

The 1 µA bias value and a proposed ±20% design envelope are interface requests, not a claim about the final harness reference accuracy or compliance. The mirror input voltage, source polarity and supply sequencing will be checked against the published reference interface before schematic freeze. Bias test equipment may replace this source during standalone verification.

EN_MON needs an observable digital test route with known delay. We will establish the route and calibration with the harness team before finalising timing measurements. No additional dedicated timing pad is requested. Internal string and amplifier nodes are simulation probes, not additional silicon test pins.


## Control protocol


For a specified update, hold EN low for at least 5 µs, change D5 to D0, keep the complete code stable for at least 5 µs, then assert EN and hold the code stable until settling is complete. The reset interval is acceptable for the intended threshold and calibration use. Live code changes are permitted for characterisation, but no glitch-free transition or automatic break-before-make behaviour is guaranteed.


## 3 Operating conditions and external limits


The following is the proposed post-layout operating envelope. Typical values are design aims at TT, 25 °C and nominal supplies, not measured silicon data. Minima and maxima define acceptance conditions where applicable. A dash means that no separate value is specified.

| Quantity and condition | Min | Typ | Max |

| --- | --- | --- | --- |

| Analogue supply VDDA, V | 3.135 | 3.3 | 3.465 |

| Digital supply VDDD, V | 1.71 | 1.8 | 1.89 |

| Operating temperature, °C | −40 | 25 | 110 |

| IBIAS sourced into the core, µA | 0.8 | 1.0 | 1.2 |

| VREFL for specified transfer tests, V | — | 0.300 | — |

| VREFH for specified transfer tests, V | — | 3.000 | — |

| Digital low input, V | 0 | — | 0.3 VDDD |

| Digital high input, V | 0.7 VDDD | — | VDDD |

| Resistive output load to VSSA, kΩ | 100 | 100 | Open |

| Total capacitive load at amplifier output, pF | 0 | 20 | 20 |

| EN low before a code change, µs | 5 | — | — |

| Complete code stable before EN rises, µs | 5 | — | — |



Performance is specified at the nominal reference voltages shown; wider reference programmability is not an initial acceptance requirement. Transfer errors are calculated from the measured reference values, so external reference accuracy is excluded. References must be stable during each measurement. The load capacitance budget includes the pad, package, board, test fixture and probe, not only an added capacitor.


## Conservative absolute constraints


The proposed external supply bounds are 0 to 3.6 V on VDDA and 0 to 1.95 V on VDDD. Reference and bias terminals must remain between VSSA and VDDA; digital control terminals must remain between VSSD and VDDD. IBIAS must be current limited to 2 µA. VOUT must not be externally driven or shorted; the specified minimum resistive load is 100 kΩ.

These are provisional absolute-use constraints, not qualified damage or reliability ratings. All selected transistor, pad and inter-domain stresses must also meet the PDK limits, which take precedence [4]. No above-rail signal, powered-off input, ESD level or output-short capability is claimed. Standard foundry pads will provide the approved protection structure.

Keep EN and all data inputs low during supply transitions. Apply external references and bias only after both rails are valid; remove these drives before powering down. The permitted rail ramp and sequencing behaviour will be verified in the transistor-level design and documented with the final wrapper.


## 4 Proposed performance targets


Limits below apply over the proposed operating envelope with the specified references and load, unless a row narrows its conditions. One LSB is the measured reference span divided by 64, nominally 42.1875 mV. The limits are proposed development targets to be agreed at proposal review, not demonstrated Sky130 specifications.

| Characteristic and condition | Min | Typ | Max |

| --- | --- | --- | --- |

| Resolution, bits | 6 | 6 | 6 |

| Absolute transfer error, LSB; every code after settling | −0.5 | 0 | +0.5 |

| Differential nonlinearity, LSB; every adjacent step | −0.5 | 0 | +0.5 |

| Endpoint integral nonlinearity, LSB; every code | −0.2 | 0 | +0.2 |

| Zero-code error, LSB | −0.2 | 0 | +0.2 |

| Full-span gain error, LSB | −0.1 | 0 | +0.1 |

| Monotonicity across all 64 codes | Required | Required | Required |

| Settling from EN rising to ideal output ±0.5 LSB, µs; code stable before enable | — | 10 | 20 |

| Reset settling after EN falls, µs; output to VREFL ±0.5 LSB | — | 10 | 20 |

| Load regulation magnitude, mV; 100 kΩ to 1 MΩ at code 63 | — | 1 | 5 |

| Reference current magnitude, µA; either reference, steady state | — | 42.2 | 100 |

| Analogue supply current IDDA, mA; all static codes, including reset, excluding reference current | — | 0.30 | 1.0 |

| Digital supply current IDDD, µA; static controls | — | 5 | 50 |



Absolute error is VOUT minus the ideal voltage derived from the measured references, with no offset or gain correction. Zero-code error is VOUT at code 0 minus VREFL. Gain error is the measured code 0 to 63 span minus 63 ideal LSBs. The conservative allocations are 0.2 LSB for zero-code error, 0.1 LSB for gain error and 0.2 LSB for endpoint INL, summing to the overall 0.5 LSB limit. The combined absolute error will also be checked directly.

DNL is an adjacent output step divided by ideal LSB, minus one. Endpoint INL is deviation from the straight line through the measured code 0 and code 63 outputs, expressed in ideal LSBs. A monotonic result requires every measured adjacent output step to be positive within measurement uncertainty.

Settling starts at the 50% point of EN at the IP boundary and ends when VOUT enters and remains within the stated band. The bias, references and supplies are already stable. EN_MON route delay will be measured or bounded and included in the uncertainty. Live-update glitches, output noise and operation beyond the stated load will be characterised and reported; no separate numerical acceptance limits are proposed for them.


## 5 Silicon measurement plan


We will characterise packaged devices at nominal supplies and approximately 25 °C, then repeat the transfer and current measurements at supply extremes and −40, 25, 70 and 110 °C. Sample count depends on returned devices; every measured device, temperature, supply and fixture configuration will be recorded. Process corners are verified by simulation, not inferred from a small silicon sample.

| Test | Measurement method | Acceptance or report |

| --- | --- | --- |

| Function and reset | Drive all 64 codes through the harness using the specified EN sequence. Apply two known references and observe VOUT. | Correct selected level; EN low returns to the low-reference output. |

| Transfer accuracy and linearity | Measure VREFH, VREFL and VOUT with a calibrated DMM. Use at least 1 ms settling plus the DMM integration time per code; repeat ascending and descending. | Absolute error, zero-code error, gain error, DNL, INL and monotonicity against page 4 limits. |

| Settling and reset | Capture VOUT and EN_MON simultaneously using a high-impedance low-capacitance probe. Test codes 0, 1, 31, 32 and 63 after reset, plus both output extremes. | Enable and reset settling ≤20 µs, after correcting or bounding the digital test-route delay. |

| Glitches and noise | Hold EN high for 31↔32 and 0↔63 live updates. Capture peak excursion and transient error area. Measure code 32 output noise with a stated bandwidth and instrument floor. | Report results and conditions; no low-glitch or noise limit is claimed. |

| Loading and drive | Repeat static tests with 1 MΩ and 100 kΩ loads and the full 0–20 pF capacitance budget. Use larger capacitance and 1 kΩ only as simulation stress cases. | Load change at code 63 ≤5 mV. Accuracy and settling at the specified load; simulation stress cases reported separately. |

| Current and references | Measure IDDA and IDDD separately for all static codes and reset. Measure the current sourced by VREFH and absorbed by VREFL. Sweep IBIAS over its specified range. | Supply and reference current limits on page 4; stable operation across the bias range. |

| Temperature and supply sensitivity | Repeat the transfer, current and representative transient tests at the operating-envelope endpoints and compare with extracted corner results. | Specified limits across the agreed envelope; publish failures and measurement uncertainty. |



The provisional equipment list is supplied separately. Reference instruments must source and sink current; a supply that cannot sink current is unsuitable by itself for VREFL. Kelvin sensing or measured pad/fixture drops will be used where practical. Reference-path error and pad/fixture loading will be included in the uncertainty budget.

The voltage-measurement uncertainty target is ≤1 mV, comfortably below half an LSB; timing uncertainty should be ≤0.5 µs. Fixture capacitance and active-probe loading will be measured or bounded so the total 20 pF condition is credible. If the harness test route cannot support a defensible timing reference, its routing must be resolved before timing sign-off.


## 6 Implementation verification and delivery


The main design work is the transistor-level buffer: it must accept 0.3–3.0 V inputs at the minimum supply, hold offset within the error budget and remain stable over the specified output capacitance. We will assess complementary input or other suitable input-range topologies, local bias mirrors, gain and compensation before committing dimensions. An MCP6001 chip or proprietary amplifier model will not be the submitted IP.

The selector and interface will use PDK devices whose gate, drain and body limits support the actual voltage stresses; nominal 3.3 V operation does not justify using 1.8 V core devices in the analogue path. Resistors will use matched unit elements, consistent orientation, dummies and routing designed to reduce gradient and contact errors. No slot area estimate is claimed before device sizing and harness dimensions are known.

Reproducible Xschem and ngspice testbenches will cover all 64 codes, TT/FF/SS/FS/SF corners where supported, supply and bias extremes, temperature, startup, mismatch and extracted parasitics. The amplifier will also receive open-loop gain, loop stability, slew and noise checks. The design target is at least 60° simulated phase margin over the specified 0–20 pF load range. Mismatch/yield assumptions and run counts will be documented rather than inferred from nominal linearity.

| Milestone | Planned deliverable |

| --- | --- |

| Proposal review Week of 23 Nov 2026 | Agree the specification, three analogue pads, EN_MON test route and 1 µA bias interface. |

| Schematic review Week of 28 Dec 2026 | Sky130 circuit and bias design; open-source functional, corner, stability and initial mismatch results. |

| Layout review Week of 1 Feb 2027 | Reusable standalone layout, DRC/LVS, extracted transfer, settling and corner verification. |

| Final review Week of 22 Feb 2027 | Harness wrapper, approved pad and reference connections, sign-off evidence and measurement scripts. |

| After fabrication | Board bring-up, measured characterisation and published results; dates depend on returned silicon. |



Final deliverables will include editable design sources, standalone and wrapped layouts, GDS/LEF and extracted netlists as applicable, reproducible verification scripts, sign-off records and measurement documentation in a public repository. We propose Apache 2.0 for original project IP, subject to team confirmation and compatible third-party source terms. The teaching macromodel is only a feasibility aid, not a dependency of the final open-source verification flow.


## References


Official requirements and schedule checked on 12 November 2026. The supplied slide’s resource table is labelled Challenge 3; this proposal uses the current Sky130 Challenge 4 rules. Repository and team details are supplied separately to keep personal information outside this public technical document.

[1] Challenge 4 rules: https://opencircuitdesign.com/chipalooza/rules-4.html

[2] Proposal submission instructions: https://opencircuitdesign.com/chipalooza/get-involved.html

[3] Challenge 4 schedule: https://opencircuitdesign.com/chipalooza/schedule-4.html

[4] Sky130 device information: https://skywater-pdk.readthedocs.io/en/main/rules/device-details.html
