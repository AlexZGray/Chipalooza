# DAC proposal submission details

Prepared 12 November 2026. This administrative template accompanies the public technical proposal and contains placeholders only. Fill personal and institutional details in a private submission copy. The proposal has not been submitted.

## Team and contact placeholders

- Team name: **[TEAM NAME]**
- ICARUS team number: **[TEAM NUMBER OR NOT YET ASSIGNED]**
- Primary contact: **[CONTACT NAME AND EMAIL]**
- Designers: **[DESIGNER NAMES]**
- Institution, if required in correspondence: **[INSTITUTION]**

Personal and institutional information belongs in the correspondence and separate attachments, not the main technical proposal.

## Files to send

1. **Chipalooza_DAC6_Initial_Proposal.pdf** — the main technical document, suitable for eventual public project documentation.
2. **Chipalooza_DAC6_Provisional_Equipment.pdf** — separate test-equipment attachment. Its equipment/access assumptions are provisional, as requested; specific models are not invented.
3. **Each designer’s actual CV, as an individual attachment.** CVs have not been created or inferred from names/placeholders. Include every participating designer.

Editable Word versions are provided for both prepared attachments. Send the final PDFs after filling in the administrative fields. Download the repository or the individual files for local editing. Send the equipment list and actual CVs as separate email attachments.

## Submission destination and date

- Email: **chipalooza@opencircuitdesign.com**
- Official deadline: **23 November 2026**
- Suggested team target: **21 November 2026**
- Suggested subject: **Chipalooza Challenge 4 proposal — Buffered six bit resistor string DAC — [TEAM NAME]**

No cutoff time or timezone was specified on the official pages checked. Do not rely on a last-minute interpretation. Keep the sent package and acknowledgement.

## Technical source link

Public repository: [AlexZGray/Chipalooza](https://github.com/AlexZGray/Chipalooza)

Runnable reference: [LTspice DAC files](https://github.com/AlexZGray/Chipalooza/tree/main/simulations/ltspice/dac6)

The existing demonstrator is an architecture aid, not the final Sky130 sign-off design. The proposal explicitly adds an EN_MON test output and a nominal 1 µA harness bias interface for the transistor amplifier; neither is claimed to exist in the published LTspice demonstrator.

## Final team review

- Fill the team/contact placeholders; include the ICARUS number if assigned.
- Attach the actual designer CVs separately.
- Confirm the proposed accuracy, supply/temperature envelope, load and update/reset protocol as the team’s design targets. The buffer’s input range and stability are the main feasibility risks.
- Discuss the three dedicated analogue pads, EN_MON digital test route and nominal 1 µA bias source/compliance with the organiser. The request is within the published numerical resource limits but the precise allocation and wrapper mapping are not yet agreed.
- Retain the provisional equipment assumption for this initial version or replace it with confirmed models/access details before sending. Before measurement, record calibration and actual availability.
- Confirm a standard open-source license for original IP and compatible third-party dependencies. Apache 2.0 is proposed in the technical document. Publishing this proposal does not change the repository license or the LTspice design sources.
- Review the final PDFs after any edits and confirm that personal information has not entered the main proposal.

## Official references

- [Challenge 4 rules](https://opencircuitdesign.com/chipalooza/rules-4.html)
- [Submission instructions](https://opencircuitdesign.com/chipalooza/get-involved.html)
- [Challenge 4 schedule](https://opencircuitdesign.com/chipalooza/schedule-4.html)
