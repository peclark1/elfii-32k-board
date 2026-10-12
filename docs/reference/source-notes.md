# Reference material

Source documents supplied by the project owner, consulted for initial architecture:

1. **Netronics ELF II Assembly Manual**, original early-revision scan. Page 13: ELF II bus definition; pages 14–16: control, memory and TV circuits.
2. **ELF II — A Personal Microcomputer for $100**, Popular Electronics. Figure 6: bus connector map; Figure 1: 2101 memory and address arrangement.
3. **ELF II — 4K Memory Board Schematic**, original Netronics documentation. Page 1 placement/parts; page 2 selection and schematic; page 4 suggested original RAM isolation.
4. **ELF II — Memory and ADC Board**, schematic found via COSMAC ELF files. Shows 62256 + 27256 and 74LS273 high address latch. **Its shared /CE and mapping are not independently verified**; use only as reference.
5. **16K-Board-Pix-Schematic.zip**, COSMAC ELF group files: period-style 2114 array and expansion design, for comparison.
6. **AVIELF2v1-Sch.pdf** and **AVIELF2HYPERBOARD-KiCad-Rev2.pdf**: modern expansion-compatible implementation references.

References are **not** copied into this repository pending copyright/license review. Use the owner's local copies.

## Corrections to generated concept art
- The 22-pin vertical pinout was fabricated; actual ELF II connector is 86 contacts.
- The high address A8–A15 must be latched on TPA, not A0–A7 as drawn.
- The displayed 74LS138 decoding and logic gate wiring are not a valid checked circuit.
- PCB image traces and pin labels are artistic, not manufacturing data.

## Next research work
Record precise evidence for latch sampling edge; compare motherboard, Netronics 4K and AVI schematics; verify memory-map decode and connector geometry.
