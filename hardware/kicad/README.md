# KiCad starter

- `elfii-32k-board.kicad_pro` — project container.
- `elfii-32k-board.kicad_sch` — empty schematic page with project title; **no nets or components yet**.
- PCB file **now exists**, with the full measured Hyperboard Rev 2 outline and the 86-contact connector footprint. Contact numbers 1–86 were extracted from front/back copper-Gerber metadata; schematic nets, SRAM components and tracks have not yet been implemented.

The schematic skeleton was authored as KiCad text format but could not be opened or checked with KiCad CLI in this environment. Please verify that it opens in your installed KiCad before wiring components.

The reusable connector symbol and connector footprint are included in project-local KiCad libraries (`ELFII_Expansion.kicad_sym` and `ELFII_Expansion.pretty`). Next, confirm original bus signal assignment and implement the memory schematic described in `docs/design/schematic-plan.md`.
