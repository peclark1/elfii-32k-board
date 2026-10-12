# First PCB placement — Rev A1 review

Status: **unrouted electrical draft**. Schematic ERC, PCB DRC, bus timing and hardware compatibility have NOT been passed.

## Full-size mechanics preserved
- AVI Hyperboard Rev 2 measured outline: nominal 177.8 × 127.127 mm, 1.6 mm FR4.
- 86-contact edge connector with exact copper-Gerber-derived pitch and pad geometry.
- No shrinking of board, per project decision.

## Initial DIP/parts placement (KiCad coordinates, mm)
| Ref | Device | Centre X | Centre Y |
| --- | --- | ---: | ---: |
| U1 | 74HCT273 address latch | 92 | 67 |
| U2 | 62256 32KiB SRAM | 153 | 72 |
| U3 | 74HCT04 | 68 | 111 |
| U4 | 74HCT86 | 100 | 111 |
| U5 | 74HCT32 | 132 | 111 |
| JP1 | LOW/HIGH bank select | 190 | 80 |
| JP2 | card enable | 190 | 107 |
| R1 | enable pulldown, 10k | 176 | 123 |
| R2 | region pulldown, 10k | 176 | 132 |
| C1–C5 | per-chip 100nF bypass capacitors | adjacent to U1–U5 | — |

The general grouping is period-styled: latch left of RAM, glue logic and configuration beneath/to the right, substantial unpopulated space above for period-inspired labeling and service notes.

## Electrical consistency
- Components are included as actual KiCad through-hole footprints with numbered pads and provisional nets assigned.
- Each component carries its corresponding schematic UUID path to assist KiCad footprint synchronization.
- 86-contact connector is not re-created; existing full-size original-derived geometry retained.
- All traces and vias are intentionally absent.
- Automated checks test the region-select truth table and KiCad's exported schematic pin/net connectivity, then compare physical pad net assignment to that netlist.
- KiCad 7.0.11 can export netlist and Gerbers; it does not provide `sch erc` or `pcb drc` commands in the CLI shipped by Ubuntu 24.04. **Actual ERC and DRC must still be run using KiCad's GUI or a newer KiCad CLI.**

## Before starting routing
1. Open the branch in KiCad and inspect pad geometry, pin-one orientations and silkscreen readability.
2. Confirm original ELF II socket engagement (contact fingers, bevel, finish, stackup, thickness).
3. Confirm the 1802 TPA sampling timing and zero overlap of low RAM with the original 2101s.
4. Check desired ROM/monitor configuration with the Giant Board.
5. Run full ERC; then place power bypasses as close to IC power pins as possible.
6. Route first power/ground, then MA/DATA, then latched A8–A15, followed by read/write/select signals.
7. Perform full DRC, verify reversible motherboard compatibility and electrical bench test.
8. Only after signoff produce manufacturing Gerbers for a prototype; currently exported Gerbers are solely for parsing checks, **not fabrication**.
