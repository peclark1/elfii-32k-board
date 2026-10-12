# 32K SRAM card — physical and electrical pre-fabrication review
Review date: 2026-10-12

**Status: engineering review only. Not approved to fabricate, purchase or install.**

Branch `feature/hyperboard-pcb-prefab-review` is derived from the
coordinator-accepted `experiment/hyperboard-route-b57bb49a` at
`cd902d8b0b1cb3dfee6a36365e016e25e7ea1fd4`.
`main` remains unchanged at this review milestone.

## What was inspected: the actual native routed .kicad_pcb

The corrected starting preview (not the earlier first-pass route) had:

| Physical characteristic | Observed value |
| --- | --- |
| Copper | two layers: F.Cu, B.Cu |
| Tracks | 438 segments; 396 at 0.20 mm and 42 at 0.15 mm |
| Plated vias | 35, each 0.60 mm diameter / 0.30 mm drill |
| Zones | none in the accepted preview |
| GND wiring | 51 routed segments, approximately 401.1 mm total |
| +5 V wiring | 35 routed segments, approximately 234.7 mm total; two 0.15 mm neckdowns |
| Edge pads | 86, two sided, Gerber-derived; 14 original Edge.Cuts segments |
| J1-69 | routed to JP2-1, with JP2-2 to GND; no permanent tie |
| J1-82 | unconnected (function not independently verified) |

The first 426-segment/27-via trial and historical NC J1-69 notes are
**superseded** and must not be used as descriptions of this revised layout.

## Corrections implemented on the review branch

1. **Moved the dangerous +5 V via out of the card-finger region.** A
   +5 V F.Cu/B.Cu tie via at (174.793, 150.627) was in the exposed
   finger Y interval (approximately 144.2974 to 153.1874).
   Removed it and its four connecting stubs, reconnecting both sides
   through a new via at (175.3, 142.2793), safely above the finger
   tongue (defined PCB body transition at Y=144.272).
2. **Created a ground-return system.** Added F.Cu and B.Cu GND zones,
   with 0.30 mm clearance and thermal parameters and a conservative
   Y=141.5 southern boundary to exclude the entire finger tongue.
   Existing routed GND tracks stay until their effectiveness can be
   independently checked against filled pours in KiCad.
3. **Fixed stale regression logic.** The original motherboard-RAM-disable
   behavior in Slot 5 is established prior evidence. The safety guard
   requires J1-69 → JP2-1; JP2-2 → GND, removable jumper normally open;
   J1-82 remains NC. A second check traverses the actual F/B trace and
   via graph to verify continuity from J1-69 to JP2-1.
4. **Established a dedicated native CI gate.** The workflow validates
   schematic ERC, original mechanical geometry, pin/net mapping,
   physical copper safety, temporary zone refill and project-local
   full-board KiCad 9 DRC. It uploads inspection SVGs and test reports,
   not manufacturing outputs. See Actions for this branch.

## Electrical/physical questions that are *not* cleared by DRC

- **Power distribution:** the original 0.20 mm power and ground tracks
  are uncomfortably narrow for a long common supply backbone; +5 V
  includes two 0.15 mm neckdowns near the upper IC region.
  The new ground zones improve returns *if* their filled copper has
  reliable thermal/pad connectivity and reasonable continuity.
  They do not automatically solve +5 V trace-current/voltage-drop
  and transient-return concerns. Check copper weight, supply budget
  and actual filled-zone geometry before authorizing fabrication.
- **Decoupling:** C1, C2, C3, C4 serve U1–U4; pad-center distance to
  each respective VCC pad is about 5.4, 5.8, 6.4 and 11.6 mm.
  C4/U4 is the weakest local placement; measure actual loop length,
  return paths and socket clearances rather than assuming its physical
  proximity is adequate. C5 is bulk support, not an IC-local bypass.
- **Route quality:** several 100+ mm address/control traces cross the
  full-length connector-to-IC distance; all routing widths and neckdown
  clearances must be checked against the actual board house capability.
  The 0.15 mm segments are especially fabrication-sensitive; inspect
  any short microsegments and mask/sliver clearances in copper SVGs.
- **Edge contact specification:** the native board records 1.6 mm
  thickness and original two-sided 86-finger Gerber geometry, but this
  is not a manufacturer's approval. Specify selective hard gold (or an
  explicitly accepted alternative), bevel angle and depth, finger
  length/contact wipe, mask exclusion, tolerance on board thickness,
  substrate, and edge routing. Finger copper from historical Gerbers
  ends roughly 0.10 mm short of the board edge. Verify feasibility
  of that detail with the fabricator.
- **Assembly clearance:** no physical slot/card-cage test or populated
  component-height/courtyard check has been completed. Validate the
  switches, resistor array, DIP sockets, jumpers, bottom-side
  copper/parts and envelope with a 1:1 board template.
- **Logic and compatibility:** the schematic follows the Hyperboard RAM
  path (U1 high-address 74HC573, U2 CY62256, U3 74HC151 page selector,
  U4 CD4011 A15 complement). ERC, pad-net consistency and clean KiCad
  DRC cannot prove TPA latch setup/hold, /CS propagation, /MRD→/OE,
  /MWR→/WE overlap, read data release, write timing, or interactions with
  ROM and Giant Board memory-mapping. Bench verification on the original
  early Netronics machine is still mandatory before installation.
- **J1-82:** deliberately NC; do not guess its function from newer AVI
  documentation. J1-69 RAM-disable in Slot 5 is settled and is **not**
  being reopened absent conflicting bench evidence.

## Release gate

A successful native KiCad ERC/DRC and matching nets are necessary but
not sufficient. This board stays on a **non-authoritative feature branch**.
Do not generate a production order, fabricate or install while timing,
actual memory coexistence, power-width review, mechanical envelope,
J1-82, and the manufacturer's card-edge process remain open.
