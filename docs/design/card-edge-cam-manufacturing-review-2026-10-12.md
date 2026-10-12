# Card-edge CAM and manufacturability review — engineering questions only

Date: 2026-10-12  
Status: **NO fabrication, no purchase/order, no install, no merge authorization.**
The original 86-contact two-sided geometry and board outline **must be
preserved** unless a separately reviewed change is approved.

## Native geometry that must not silently change

The current routed KiCad board preserves the original Hyperboard Rev 2
historical manufacturing geometry:

| Feature | Native PCB |
| --- | --- |
| Outline | 177.800 x 127.127 mm extreme-coordinate span; 14 stepped/chamfered Edge.Cuts segments |
| Board thickness | 1.6 mm nominal in KiCad; tolerance not established |
| Edge contacts | 86 rectangular copper pads, 43 each face |
| Pitch | 2.540 mm |
| Contact width / length | 1.397 x 8.890 mm |
| Finger-center range | X=66.9036 to 173.5836 mm |
| Leading card edge | Y=153.2890 mm |
| Copper end toward edge | Y=153.1874 mm |
| **Copper-to-edge setback** | **0.1016 mm** (historical geometry, NOT approved bevel clearance) |
| J1-69 | Physical copper to optional JP2-1; JP2-2 GND; no permanent shunt |
| J1-82 | Physically NC, deliberately unassigned |
| Supply via | +5V 0.60/0.30 mm via at (175.3,142.2793), not in finger tongue |

Source geometry: `docs/reference/hyperboard-rev2-gerber-geometry.md`;
hard-locked by `tests/test_mechanical_geometry.py`. The CI manufacturing
feature report is emitted from the *actual* PCB source.

## Published fabricator guidance creates a significant question

JLCPCB's published card-edge FAQ describes a 1.6 mm board with a 30-degree
bevel requiring at least approximately **0.6 mm** between the card edge and
the start of a gold finger, or parts of the copper may be cut away or the
manufacturer may alter the CAM image. This should **not** be treated as a
universal specification: fabricators and bevel processes differ. However
our historic copper-to-edge setback is only **0.1016 mm**, considerably
less than that example clearance.

- JLCPCB original gold-finger FAQ:
  https://jlcpcb.com/quote/pcbOrderFaq/Gold%20Fingers
- JLCPCB updated gold-finger process guidance (2026-09-18):
  https://jlcpcb.com/help/article/jlcpcb-gold-fingers
- PCBWay published advanced capability table:
  https://www.pcbway.com/advanced-pcb-capabilities.html

This is a **real manufacturing ambiguity**, not an error to solve by
blindly moving all 86 contacts inward. Moving them changes the contact
wipe distance and may defeat fit in the old Netronics socket. Equally,
the manufacturer must not bevel through active finger copper or
silently change it without consent. An approved process and any requested
CAM edits must be reviewed together with the **actual mating socket**.

## Copper features in the current engineering route

- 437 copper segments total.
- 402 segments at **0.20 mm**.
- 35 segments at **0.15 mm**, about **42.94 mm** of copper,
  longest ~4.82 mm (after five longer runs were widened).
- 35 plated vias, **0.60 mm land / 0.30 mm nominal drill**:
  nominal radial ring 0.15 mm before processing tolerances.
- F.Cu and B.Cu ground fills stop at Y=141.5 mm, away from
  the finger insertion tongue. The two GND tie exceptions
  C2-2/U4-2 are intentionally solid to avoid starved thermals.
- No PCB production file has been released.

PCBWay's public *advanced* capability page advertises small track and
spacing features, but this is **not an acceptance of our design, copper
weight, drill tolerance, annular ring, solder-mask bridges, or pricing**.
Obtain a specific quotation/CAM disposition with the actual board data
**before any manufacturing authorization**.

## Questions to send a candidate fabricator (not a build order)

1. **Card edge geometry:** Can the process retain the exact 86-contact
   two-sided 1.397 x 8.890 mm pads, 2.540 mm pitch and the current
   0.1016 mm copper-to-edge setback, including reliable plating and
   beveling? If not, ask for *dimensioned* proposed CAM modifications
   and their effect on connector wipe. **Do not authorize automatic edits.**
2. **Bevel:** What bevel angle, depth, residual-edge thickness,
   copper setback and tolerances are actually achievable for a
   1.6 mm nominal 43+43-contact card? Does it require moving
   finger copper, changing overall length, or additional plating rails?
3. **Finish:** Is selective **hard gold over nickel** available on only the
   contact fingers? If ENIG is substituted, what is its wear-life/cycle
   limitation for repeated vintage card-cage insertion? Does the
   selected process need sacrificial plating connections or a panel rail?
4. **Card thickness/outline:** What is guaranteed finished thickness at
   the mating edge and contour tolerance? Can the stepped tongue,
   edge shoulders and 1.27 mm board-corner chamfers be routed as supplied?
5. **Fabrication rules:** Confirm 0.15/0.20 mm traces, actual minimum
   copper spacing, 0.60/0.30 vias, drill-to-copper spacing, finished
   annular rings, chosen copper weight, solder-mask registration and
   any minimum allowable pad-to-board-edge spacing elsewhere.
6. **Solder mask:** All 86 fingers must be properly open on their
   respective faces, with no ink/contact-surface interference.
7. **Assembly/electrical holds:** Manufacturer CAM approval does *not*
   establish board-to-Netronics-slot fit, component height, or safe
   electrical operation. Those require separate owner-side bench work.

## Acceptance gate

Archive the manufacturer's *specific* written answers, a reviewed CAM
overlay showing the original connector and any proposed changes, the
actual socket dimensions or physical fit test, and the intended finish
and bevel before proceeding. If the vendor cannot meet the historic
connector requirements, stop and return proposed changes for explicit
engineering and owner approval. This document authorizes inquiry only,
not uploading production Gerbers for an order.
