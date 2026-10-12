# 86-contact edge connector — first KiCad implementation

**Status: MECHANICAL PROTOTYPE ONLY. Not electrical-ready or fabrication-ready.**

The board includes `ELFII_Expansion:ELFII_Edge_86_Rev2_Unverified` at the geometry extracted from the user's AVI Hyperboard Rev 2 Gerbers.

## Geometry as implemented
- 43 contact openings per face, 86 total.
- Pitch 2.540 mm; span 106.680 mm center to center.
- Each rectangle: 1.397 × 8.890 mm from the **solder-mask file**.
- First column center: X=66.9036 mm; final: X=173.5836 mm.
- Contact center Y=148.7424 mm, on the Hyperboard-derived outline ending at Y=153.289 mm.
- Board thickness 1.6 mm, as specified by supplied .gbrjob.
- The same coordinates are assigned on front and back copper/mask layers.

## IMPORTANT validation flags
- Pads use provisional text IDs `F01...F43` and `B01...B43`. These **are not the original bus pin numbers** and are not safe to use in electrical schematics.
- Footprint rectangles reflect mask openings. Recheck actual copper pad size, end clearance, side clearances, copper layer, paste absence, and solder mask data, and compare to the Gerber copper.
- Check exact original connector numbering and component vs solder side against the original Netronics schematic.
- Confirm board-outline fit and edge chamfer/bevel requirements with a physical template.
- Surface finish and card edge plating remain unspecified in the supplied files. Obtain fab house edge-connector finish/process guidance.
- Review physical orientation for accidental face reversal.
- This board has **no routing, electrical nets, SRAM, or logic components yet**.
- KiCad CLI is not installed in the current runtime; no ERC/DRC has been run.

## Next electrical stage
Only after the pad mapping is verified, create symbol(s), assign real pin numbers and check via independent schematic reference, then connect the latch, SRAM and decoder. Preserve design gates in schematic-plan.md.
