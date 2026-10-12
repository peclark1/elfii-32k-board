# Prototype fabrication readiness — 32K SRAM ELF II card

Date: 2026-10-12. Baseline: feature/hyperboard-pcb-prefab-review at 7537d88f2e6fc8b3162708dac74ff012362a7f7b. Revision: engineering review, NOT production authorization.

## Decision

**PROTOTYPE-CANDIDATE electrically and in KiCad; HOLD for card-edge CAM/process sign-off before ordering.** Retain the Hyperboard-derived circuit, original 86-contact edge and existing route. Do NOT create a new timing-validation campaign as a prerequisite to having a prototype built. Run functional timing, coexistence and repeatability tests *on the prototype* after controlled installation. No order, manufacturer submission or connector alteration is authorized by this document.

The key external question is whether a vendor can fabricate the *historical* 0.1016 mm copper-to-edge finger setback without deleting or damaging the contacts during beveling. The published default processes do not substantiate this geometry; a vendor-specific CAM disposition is essential.

## Source and electrical adaptation review

Reference: owner-provided AVI Hyperboard Rev 2 schematic (2026-03-17), prior traced circuit in docs/design/hyperboard-ram-circuit-trace.md, and separately the AVI ELF II motherboard SRAM schematic. Independent schematic/netlist and routed-pad checks exist in CI.

| Function | Implemented adaptation | Assessment |
| --- | --- | --- |
| Address capture | U1 74HC573 loads high address on TPA; MA7..MA0 enter D0..D7 and leave Q0..Q7 as A15..A8. Low MA0..MA7 directly drive U2 A0..A7. | Retained Hyperboard architecture and bit order. |
| SRAM/data | U2 CY62256-70PC, D0..D7 bidirectional to ELF II bus, /OE from /MRD and /WE from /MWR. | Direct Hyperboard paths; read/write qualification is primarily by /CS. |
| Page decode | U3 74HC151 S0..S2=A12..A14, I0..I7 from eight +5V DIP positions with 8x22k pull-downs, inverted output /Z drives U2 /CS. | Matches source logic, with deliberate LS151-to-HC151 reliability substitution. |
| Logic-level adaptation | Original 74LS151 with 22k-to-GND could fail its published worst-case TTL LOW-current limit; HC151 inputs have very low leakage. | Appropriate and materially justified change. Verify fitted DIP-16 part is HC151, NOT LS151. Source notes: docs/design/page-select-ttl-input-margin.md. |
| 32K half | JP1 LOW connects mux /E to A15, HIGH connects /E to complemented A15 from one U4 CD4011 NAND gate (inputs joined). | Preserves source ROM/RAM half-selection behavior without ROM. Install exactly one shunt. |
| Motherboard RAM | ELF bus J1-69 routed solely to optional JP2-1; JP2-2 ground; shunt OPEN by default. | Slot-5 function known from project tests. Never directly connect J1-69 to SRAM /CS; it is not the chip select. |
| Unused bus contact | J1-82 electrically unconnected. | Safe to leave NC in PCB prototype; document unknown function, do not turn it into a mandatory measurement before *fabricating* an unconnected contact. |
| Omitted Hyperboard functions | ROM, BOOT, UART, tape, I/O ports, CDP1853 decoder, and other non-SRAM logic. | Intentional scope reduction. |

Existing logical truth-table, KiCad ERC, exported pad-netlist, native routed connectivity and independent filled-board KiCad 9 DRC passed on baseline SHA 7537d88 (runs 38282628031 and 38282628013). This is evidence of *design consistency*, not a proven operating prototype.

## Measured PCB manufacturing profile (existing native source)

- Full original stepped outline, 177.800 x 127.127 mm extrema; two copper layers, FR-4, nominal 1.6 mm, 1 oz outside copper proposed.
- Edge J1: 86 copper pads (43 per face), 2.540 mm pitch, 1.397 x 8.890 mm each; finger copper terminates 0.1016 mm before the leading outline; no connector geometry edit is permitted without a reviewed change.
- 437 routed track segments: 402 at 0.20 mm, 35 signal segments at 0.15 mm (about 42.94 mm total, maximum 4.82 mm long). 35 plated vias 0.60 mm land/0.30 mm nominal drill; 0.15 mm nominal radial ring.
- F.Cu and B.Cu GND fills intentionally stop short of exposed finger tongue; selective solid GND pad connections at C2-2 and U4-2 pass filled-board DRC.
- +5V: 34 segments, all 0.20 mm wide, approx. 239.58 mm cumulative; the longest straight shared section about 39.1 mm. Both +5V fingers joined via a plated through-path; one supply via is outside the tongue. Four 100 nF IC-local bypasses C1..C4 and one 10u bulk C5. Local +5V path to U1/U2/U3/U4: 5.38/5.76/6.38/12.06 mm.
- Deliberately preserve source-board silkscreen warning until release review and CAM approval. KiCad's special scoped connector copper-to-edge rule is *not* a manufacturer's approval.

0.15 mm traces and 0.60/0.30 vias are normal candidates for a capable prototype board house; the fab must still explicitly accept actual spacing, drill tolerance, finish, and mask for this specific order.

## Card-edge options, ranked

1. **Preferred inquiry: PCBWay engineering-reviewed custom connector finishing** on the current exact Gerbers. Ask about selective hard gold over nickel (e.g. 10 microinch Au / 120 microinch Ni quote starting point), with *no conventional bevel* or a custom shallow/deburred lead-in that does not touch finger copper. Only proceed if they supply an acceptable drawing explaining insertion-edge treatment and tolerances, and confirm 1.6 mm mating thickness. Do not assume their standard gold-finger service will accept it.
2. **Fallback: un-beveled ENIG engineering prototype**, *only if PCBWay/another manufacturer explicitly accepts this construction and the real slot can tolerate a square insertion edge*. This is for a small number of careful test insertions, not a promised durable finished card.
3. **Alternative custom gold-plating/finger rework** where a vendor provides a controlled process drawing (e.g. plating after forming or sacrificial plating rails). If they require trimming contact copper, shifting the leading edge, increasing the copper setback or other geometry changes, STOP and obtain separate owner approval after assessing the historic connector wipe/fit.
4. **JLCPCB normal 30-degree bevel: not pre-approved.** Published advice requires about 0.6 mm setback for 1.6 mm board and warns of CAM optimization. A conventional 45-degree PCBWay bevel is listed at about 0.50 mm chamfer depth and 30 degree at about 0.95 mm: both are much deeper than 0.1016 mm. No silent automatic correction allowed.

Sources:
- PCBWay gold-finger process and bevel dimensions: https://www.pcbway.com/pcb_prototype/PCB_Gold_fingers.html
- PCBWay quote settings, selective hard gold, no-bevel option: https://www.pcbway.com/HighQualityOrderOnline.aspx
- PCBWay electroplating manufacturing-rail consideration: https://www.pcbway.com/blog/Engineering_Technical/Understanding_PCB_Manufacturing__Hard_Gold_Plating.html
- JLCPCB updated policy: https://jlcpcb.com/help/article/jlcpcb-gold-fingers
- JLCPCB specific 1.6 mm example: https://jlcpcb.com/quote/pcbOrderFaq/Gold%20Fingers

## Power and decoupling disposition

The previously recorded 0.20 mm rail is not a demonstrated electrical defect at these CMOS loads. A conservative isolated 153 mm, 0.20 mm, 35um copper run is approximately 0.38 ohm; a 55 mA SRAM-only load implies about 21 mV of illustrative DC drop on that length, not a true whole-board worst case. The main PCB has parallel GND copper pours, and native DRC/graph continuity passes. C4's 12 mm positive bypass path is less attractive than C1..C3, but there is no measured malfunction justifying ripping up the complete route. The base current/droop report remains useful as characterization, **not an ordering prerequisite**. Initial prototype tests should include supply at the SRAM with representative read/write activity, only then change copper if a fault is observed.

## Process specification for vendor quotation

Two-layer FR4, **1.6 mm nominal finished thickness**, 1 oz finished copper (confirm vendor choice), green solder mask both sides with 86 complete openings over both finger faces and no ink on wipe surfaces, white top legend, plated through holes / 0.30 mm via drills, electrical test, routed stepped outline as supplied. Quote **selective hard gold on the 86 fingers** (ask thickness options) and a defined non-damaging edge finish; ENIG-only alternate must be separately identified. No V-scoring along the finger edge; supply written production CAM proof before proceeding. Board quantity: quote five prototype units and any minimum/tooling surcharge. Do not treat vendor's auto preview as acceptance.

**Cost:** No binding or adequately parameterized public price is available for 177.8 x 127.127 mm with custom finger treatment. Request an itemized written quote for 5 boards, setup/film/plating surcharges, freight and tax. Do not substitute the $5 promotional small-board price.

## Exact pre-order decisions / measurements

Required **before ordering**:
1. Written manufacturer CAM approval: unchanged card-finger outline/pads or explicit dimensioned exception submitted for user approval; inspect bevel/no-bevel, plating, mask, tolerances, copper and vias, and any sacrificial plating rails.
2. Owner accepts supplier's confirmed contact durability/lead-in process and quoted *total price*. If manufacturer requests any geometry change, separately approve only after actual connector-fit assessment.
3. Set build configuration: 1.6 mm finished edge tolerance suitable for the original Netronics slot, 1 oz copper, green/white, selective hard-gold preference; identify populated or unpopulated quantities and selected SRAM/logic DIP packages.
4. Verify versioned review Gerber/Excellon/BOM artifact belongs to a known SHA with passing ERC/DRC and matches the reviewed CAM. Remove/replace the explicit NOT-FOR-FAB PCB silkscreen/release hold in a **separate, revalidated revision** before production.

**Not required before making prototype PCB:** extra 1802/TPA scope campaigns, theoretical power/ground impedance optimization, reworking a 12 mm bypass trace without a fault, proving J1-82's unknown function while NC, or fully exercising software/ROM/Giant Board combinations. These belong in controlled bring-up, not a pre-fabrication research gate.

## Post-fabrication bring-up

Verify continuity/no shorts and fitted shunts (JP2 OPEN; only one JP1 half position), insert in a known-compatible slot with power OFF, power through a current-limited setup, check +5V at U2, start with one selected 4K page and no conflicting motherboard/other expansion-RAM region, run write/read patterns across page boundaries, test LOW/HIGH separately, verify disabled pages do not drive D[0..7], and then conduct longer RAM tests and coexistence testing. Diagnose timing only if the prototype presents a repeatable issue.

## Evidence and pending state

Design files unchanged by this report. Source validation: https://github.com/peclark1/elfii-32k-board/actions/runs/38282628013 and https://github.com/peclark1/elfii-32k-board/actions/runs/38282628031 . Review builds (Gerber/drill/PDF/BOM) remain **NOT FOR PRODUCTION** until vendor CAM is approved and separate tagged release created. See docs/manufacturing/PCBWAY_CAM_REQUEST.md and hardware/bom/elfii-32k-prototype-bom.csv.
