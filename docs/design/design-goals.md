# Design goals and constraints

## Core functions
- 32 KiB usable volatile RAM with one DIP-28 62256-compatible SRAM.
- Plug into the original Netronics ELF II 86-contact expansion bus without reinterpreting its pin numbers.
- Low-half (0000–7FFF) / high-half (8000–FFFF) region selection; explicit disabled state.
- Valid memory read/write enable logic: /OE asserted only on selected reads, /WE only on selected writes, /CE only in enabled region and valid memory cycles.
- Correct CDP1802 multiplexed addresses: MA0–MA7 initially carry A8–A15, captured on TPA; later MA0–MA7 represent A0–A7.
- Through-hole construction, socketed SRAM and logic; individual 100 nF bypass capacitors by each IC.
- Design for normal 5 V operation and documented current draw.

## Mechanical and historical goals
- Period-inspired green PCB, white silkscreen, edge fingers, DIP components and restrained legend.
- **Decision (2026-10-11): retain the full Hyperboard Rev 2 PCB outline** (nominal 177.8 mm × 127.127 mm), including connector tongue and shoulders, rather than shortening the card after placement. This is our period-style mechanical baseline; an original 16K board's exact dimensions remain to be independently verified.
- Reuse the measured Hyperboard Rev 2 edge geometry, and verify connector pin numbering, insertion depth, and component clearances against the original ELF II hardware BEFORE fabrication.
- No modifications to motherboard unless a separately documented, reversible RAM isolation option proves necessary.

## Verification gates
1. Transcribe original ELF II bus pinout with two independent references.
2. Establish memory map and conflict avoidance against motherboard 2101 and Giant Board.
3. Design and review address latch, decoder, /CE /OE /WE truth table.
4. KiCad ERC and independent schematic review.
5. PCB DRC, edge geometry measurement and manufacturing rules.
6. Bench checkout with current-limited supply; logic analyzer RAM cycles.
7. RAM walking-bit and full 32 KiB patterns, including repeated checksum runs.

## Non-goals (first revision)
- EEPROM/EPROM, ADC, serial, or additional Giant Board functions.
- An electrically unverified direct copy of the illustrative mockup.
