# KiCad starter

- `elfii-32k-board.kicad_pro` — project container.
- `elfii-32k-board.kicad_sch` — empty schematic page with project title; **no nets or components yet**.
- PCB file **now exists**, with the full measured Hyperboard Rev 2 outline and the 86-contact connector footprint. Contact numbers 1–86 were extracted from front/back copper-Gerber metadata; schematic nets, SRAM components and tracks have not yet been implemented.

The schematic skeleton was authored as KiCad text format but could not be opened or checked with KiCad CLI in this environment. Please verify that it opens in your installed KiCad before wiring components.

The reusable connector symbol and connector footprint are included in project-local KiCad libraries (`ELFII_Expansion.kicad_sym` and `ELFII_Expansion.pretty`). Next, confirm original bus signal assignment and implement the memory schematic described in `docs/design/schematic-plan.md`.

## Current electrical schematic

The `.kicad_sch` file now contains an **initial pin-numbered, connected schematic draft**, built around a 74HCT273, 62256, 74HCT04, 74HCT86, 74HCT32, power bypassing and configuration jumpers. Two units of P3 represent the 86-contact bus.

The project-local `ELFII_32K.kicad_sym` and `ELFII_Expansion.kicad_sym` libraries are registered in `sym-lib-table`.

This environment has **no KiCad CLI**, so the committed sheet is syntax/structure checked but has **not been opened in Eeschema or run through ERC**. Some generic symbols are project-specific instead of stock KiCad library symbols. Confirm pin placements, labels, footprints and electrical types in the graphical editor before design release.

The PCB currently holds the outline and edge connector only; component placement/routing is NOT done.
