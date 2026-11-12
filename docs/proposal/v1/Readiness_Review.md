# Buffered DAC project and proposal review

**Recommendation: proceed with the buffered 6-bit resistor-string DAC as a suitable Chipalooza Challenge 4 proposal.** It is a useful low-frequency SoC building block and a credible mixed analogue/digital project for a team comfortable with circuits but new to transistor-level IC design. Organiser acceptance and slot allocation remain their decisions.

The selected scope combines resistor matching, transmission-gate switching, voltage-domain interfaces and amplifier design. Six bits and a high-impedance load keep the accuracy/drive demands moderate. The output buffer makes the work more substantial and useful than a bare resistor string. No claim of a new topology or absence of existing DAC IP is necessary.

## Assessment of the attached slide

The slide correctly identifies the necessary proposal contents. Its table is labelled **Challenge 3** and must not set the Sky130 supply or pad budget. The current Challenge 4 rules specify 1.8 V digital and 3.3 V analogue supplies, up to 24 digital controls, 12 digital test outputs, four shared analogue lines and three dedicated pads. The proposal requests seven controls, one digital test output, zero shared analogue lines, three dedicated analogue pads and one bias current source.

| Requirement | Where addressed |
|---|---|
| Type and useful application of IP | Main proposal, page 1 |
| Functional description and code transfer | Main proposal, pages 1 and 2 |
| I/O and test ports | Main proposal, page 2; includes EN_MON and bias access |
| Typical/minimum/maximum targets | Main proposal, pages 3 and 4 |
| Absolute external constraints | Main proposal, page 3; clearly provisional, subject to PDK limits |
| Measurement plan and uncertainty | Main proposal, page 5 |
| Open-source verification, layout and deliverables | Main proposal, page 6 |
| Equipment | Separate provisional equipment attachment |
| Designer CVs | Actual individual CVs still to be attached separately |
| Team name and ICARUS number | Separate administrative placeholders, as requested |

Personal and institutional details are excluded from the main proposal. Team/contact placeholders are confined to the administrative companion and equipment attachment.

## Technical judgement

The main analogue risk is the buffer. At minimum VDDA, the required input range approaches the upper rail, so a routine differential pair may not support the whole range. Input topology, offset, compensation and capacitive-load stability require early Sky130 work. The proposal calls this out rather than treating the MCP6001 teaching macro as an IC design.

The static error budget is internally consistent: up to 0.2 LSB zero-code error, 0.1 LSB span error and 0.2 LSB endpoint INL conservatively sum to 0.5 LSB overall. The absolute transfer limit is also tested directly. The limits are proposed targets, not achieved foundry performance or a statistical yield guarantee.

The intended application tolerates a brief reset to the low reference during updates. The guaranteed settling target therefore uses EN rising after a stable code. A buffered copy of EN provides a measurement reference through a harness digital test route. Calibration/routing must be agreed before final timing claims. Live-update glitches are characterised but are not subject to an invented low-glitch performance guarantee.

The 0.3 V lower reference needs a source that can absorb the string current. The equipment attachment therefore includes a source/sink-capable SMU or equivalent reference fixture, rather than assuming any bench supply can provide it. The 20 pF output load explicitly includes pad, package, fixture and probe. The 1 kΩ overload remains a simulation stress case; silicon measurements use the validated load range.

The nominal 1 µA bias request helps avoid adding a precision reference generator to the project. Its direction, compliance and actual harness implementation need interface agreement. This and EN_MON are planned additions, explicitly distinguished from the current LTspice files.

## Readiness

The technical proposal is complete for team review. Populate the requested placeholders and attach real CVs before sending. Equipment is assumed available for this provisional version, in accordance with the user’s instruction; model/access details are not represented as confirmed facts.

The proposal package is published in the project repository. No submission email has been sent and no CV has been fabricated. Use the current official submission instructions and 23 November 2026 deadline.
