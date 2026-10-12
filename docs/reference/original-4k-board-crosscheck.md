# Netronics 4K memory board — original schematic cross-check

This review is derived from **ELF II - 4K Memory Board Schematic.pdf**, page 2 (the sheet titled *SCHEMATIC 4Kx8 MEMORY BD*). Page 3 depicts expansion power supply alternatives; page 4 depicts an optional original-256-byte-memory wiring modification. Do **not** confuse these three sheets.

> **Current correction (2026-10-12):** The original Slot-5 motherboard
> RAM-disable behavior through J1-69 is settled prior bench evidence.
> The revised PCB physically routes J1-69 to JP2-1 and JP2-2 to GND,
> with the shunt normally OPEN. J1-82 remains unresolved.
> Rev A2 claims about physically unconnected J1-69 are historical.

## Confirmed original electrical functions

| Expansion connector contact | Original period schematic text | Our 32K board |
| --- | --- | --- |
| 24 | MWR | /MWR control input |
| 28 | TPA | Address latch timing input |
| 30 | MRD | /MRD control input |
| 36, 40, 44, 48, 52, 56, 60, 64 | MA7 to MA0 | Multiplexed address inputs |
| 34, 38, 42, 46, 50, 54, 58, 62 | D7 to D0 | SRAM data inputs/outputs |
| **69** | **“MOTHER BD. MEMORIES OFF”**, *if used* | **J1-69 → JP2-1 / optional JP2-2 GND**; no permanent ground strap |

The original board also uses TPA (through a gate marked **74C07**) with memory address latch circuitry. This independently supports the design approach of buffering the **high address byte**, but the exact latch edge and propagation margins still need CDP1802 and 74HCT datasheet review.

The original uses a large 2102 memory array, jumpers and a more elaborate bank select decoder. Our 62256 design is *not* a direct electrical clone and must be validated independently.

## Contact 69 conflict

- The Hyperboard Rev 2 Gerber assigns its P3 pad 69 to a GND net.
- The historical Netronics 4K memory board instead identifies this pad as **motherboard memory disable**, with the note `IF USED`.
- Contact 69 is a motherboard-RAM-disable input on the tested original Slot-5 configuration, **not** a general GND return.
- **Historical only:** Rev A2 had J1-69 disconnected pending evidence; the accepted new PCB now routes J1-69 to the optional removable JP2 shunt. The connector symbol retains the period label `MEMORY_OFF?`.
- Prior Slot-5 work already establishes motherboard RAM disable. Do not reopen that settled test without conflicting evidence; other memory overlap and timing questions remain.
- J1-82 likewise remains unconnected pending physical verification.

## Practical coexistence implications

- The current design implements the established Slot-5 motherboard-RAM-disable input through normally OPEN, removable JP2. Installed card coexistence and timing still require release verification.
- If the motherboard 2101 RAM remains enabled, overlapping read cycles may drive the data bus simultaneously, corrupting data or stressing IC outputs. Having the new RAM's selection truth table pass does not prove safe coexistence.
- Giant Board installed means its ROM and RAM decoding must be checked separately for overlaps with `0000–7FFF` and `8000–FFFF`.

## Remaining unpowered checks (J1-69 itself is settled)

1. Determine whether pin 82 is grounded or assigned another function on this board; do not energize it.
2. Verify edge connector orientation, including contact 1/2 and the component-side viewing convention.
3. Check mechanical Slot-5 fit, finger plating/engagement and current-return contact arrangements.
4. Record the installed Giant Board/memory map and preserve known Slot-5 RAM-disable evidence.

This note preserves *period-source evidence* and the later accepted Slot-5 J1-69 result; it does not replace timing, mapping and J1-82 checks.
