# KiCad hardware design — revision A3

Open `elfii-32k-board.kicad_pro` in KiCad.

The schematic now contains the 62256 32 KiB SRAM, 74HCT273 upper-address latch, conventional multi-unit gates for the 74HCT04, 74HCT86 and 74HCT32, two configuration jumpers, two pull-down resistors, and five decoupling capacitors.

The board is full-size, using the original-style AVI Hyperboard Rev 2 edge/shoulder geometry with a numbered 86-pad edge-connector footprint. **The PCB has initial through-hole component placement and named pads but is not routed.**

Project-local libraries: `ELFII_Expansion.pretty`, `ELFII_Expansion.kicad_sym`, `ELFII_32K.kicad_sym`. The first-pass component footprints in the PCB are simplified through-hole geometries and require replacement/reconciliation against canonical library footprints before manufacturing.

## Current validation

- Actual KiCad 9 schematic **ERC: zero errors and zero warnings** (run 38192326858).
- Netlist export, required pin connections, schematic-to-PCB pad mapping, original edge-contact safety checks, 32-case logic tests and 50-mil schematic grid alignment passed.
- KiCad PDF export and PCB Gerber *parse/export* succeeded; exports are **not fabrication files**.
- PCB **DRC: 100 findings, plus 87 unconnected items** because the board remains unrouted. 86 DRC findings concern intentional finger-to-board-edge clearance; 14 concern library-footprint mismatch.
- Timing, motherboard RAM collision, Giant Board memory map, edge gold/bevel and actual early-board contact 69/82 usage **have not been electrically verified**.

Review [ERC cleanup results](../../docs/design/erc-cleanup-a3.md), [gate-symbol connections](../../docs/design/gate-symbols-a3.md), and [bench measurements](../../docs/design/early-elfii-bus-bench-validation.md).

**Do not manufacture or insert this card yet.**
