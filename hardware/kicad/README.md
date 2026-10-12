# ELF II 32K SRAM KiCad design — Hyperboard-derived revision

**Work in progress; not a fabrication or installation release.**

## Current source files

- `elfii-32k-board.kicad_sch`: active electrical design, rebuilt from the
  AVI Hyperboard Rev 2 SRAM/address/page-select circuit.
- `ELFII_32K.kicad_sym`: project-specific schematic symbols.
- `elfii-32k-board.kicad_pcb`: **previous A5 copper routing study**.
  Its track netlist is from the obsolete custom 74HCT273/XOR/OR circuit.
  **Do not assume that this PCB matches the current schematic.**
- `ELFII_Expansion.pretty` and `ELFII_Expansion.kicad_sym`: the
  measured genuine full-size two-sided 86-contact ELF II card edge,
  preserved unchanged.
- `SCHEMATIC_REBUILD_IN_PROGRESS`: intentional protection against
  using the old PCB as though its pads/traces matched the new schematic.

## New PCB placement and routing workflow

The `KiCad design checks` GitHub Action exports the current schematic
netlist and invokes `scripts/build_pcb_candidate.py` to generate a
**new, separate through-hole PCB candidate**. The generator retains the
original connector and board outline but replaces all old-architecture
parts, traces and vias. It tests the source-to-pad pin map and runs actual
KiCad 9 DRC. The new design has U1 74HC573, U2 62256, U3 74HC151,
U4 CD4011, an eight-way page DIP, jumpers and bypass capacitors.

The `Hyperboard SRAM routing trial (preview only)` Action additionally
exports this *new* candidate to Specctra DSN, attempts Freerouting 2.5,
imports any produced session into a **separate** KiCad PCB, reruns pin
and mechanical checks, compares native DRC findings and uploads front/back
SVGs and all evidence as an Action artifact. It does not overwrite source
copper. Download the latest `hyperboard-route-preview` artifact
from the corresponding GitHub Actions run.

## Electrical safety and release holds

- Source schematic can pass ERC and strict memory pin/net tests without
  proving 1802 timing or compatibility with original onboard 2101 RAM.
- Physical connector **J1-69 remains NC on generated routing candidates**,
  deliberately differing from the optional disable-jumper schematic until
  early-original-Netronics behavior is bench verified. J1-82 remains NC.
- The card-edge copper-to-outline findings are intentional but must be
  resolved with board manufacturing requirements (plating, bevel and
  mating-contact geometry), not silently waived for fabrication.
- A routed board still requires source/schematic reconciliation, zero
  unexplained DRC violations, visual layout review, bench validation, and
  a deliberate fabrication signoff.

See `docs/design/hyperboard-ram-rebuild.md`,
`docs/design/hyperboard-ram-circuit-trace.md` and
`docs/design/page-select-ttl-input-margin.md` for electrical provenance.
