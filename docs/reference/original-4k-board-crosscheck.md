# Netronics 4K memory board — original schematic cross-check

This review is derived from **ELF II - 4K Memory Board Schematic.pdf**, page 2 (the sheet titled *SCHEMATIC 4Kx8 MEMORY BD*). Page 3 depicts expansion power supply alternatives; page 4 depicts an optional original-256-byte-memory wiring modification. Do **not** confuse these three sheets.

## Confirmed original electrical functions

| Expansion connector contact | Original period schematic text | Our 32K board |
| --- | --- | --- |
| 24 | MWR | /MWR control input |
| 28 | TPA | Address latch timing input |
| 30 | MRD | /MRD control input |
| 36, 40, 44, 48, 52, 56, 60, 64 | MA7 to MA0 | Multiplexed address inputs |
| 34, 38, 42, 46, 50, 54, 58, 62 | D7 to D0 | SRAM data inputs/outputs |
| **69** | **“MOTHER BD. MEMORIES OFF”**, *if used* | **No connection**; do not tie to ground |

The original board also uses TPA (through a gate marked **74C07**) with memory address latch circuitry. This independently supports the design approach of buffering the **high address byte**, but the exact latch edge and propagation margins still need CDP1802 and 74HCT datasheet review.

The original uses a large 2102 memory array, jumpers and a more elaborate bank select decoder. Our 62256 design is *not* a direct electrical clone and must be validated independently.

## Contact 69 conflict

- The Hyperboard Rev 2 Gerber assigns its P3 pad 69 to a GND net.
- The historical Netronics 4K memory board instead identifies this pad as **motherboard memory disable**, with the note `IF USED`.
- These may reflect variant wiring or an alternate use of the connector. There is **no basis to assume** contact 69 is safe as a ground return on the early original ELF II.
- The Rev A2 design correctly keeps J1-69 unconnected in both schematic and PCB. Our J1 symbol label now reads `MEMORY_OFF?` to flag the unresolved historical usage.
- On the user's original motherboard, verify the actual pin 69 connection unpowered, including whether it reaches a RAM-enable or inhibit circuit. Then decide whether active memory-disable support is useful.
- J1-82 likewise remains unconnected pending physical verification.

## Practical coexistence implications

- If J1-69 can disable original motherboard RAM non-destructively on this revision, a future optional jumper/buffer could make the 32K card easier to use at address `0000`. **Do not design or populate this connection until electrical polarity, current drive, and what else it affects are confirmed.**
- If the motherboard 2101 RAM remains enabled, overlapping read cycles may drive the data bus simultaneously, corrupting data or stressing IC outputs. Having the new RAM's selection truth table pass does not prove safe coexistence.
- Giant Board installed means its ROM and RAM decoding must be checked separately for overlaps with `0000–7FFF` and `8000–FFFF`.

## Recommended unpowered measurements on the early original ELF II

1. Identify pin 69 on the correct contact face and check continuity to ground with power disconnected; **do not energize or jumper it** as a test.
2. Check continuity between pin 69 and motherboard memory decode / RAM enable pins using original schematic references.
3. Determine whether pin 82 is actually bonded to connector ground (or different on this revision).
4. Verify edge connector orientation, including contact 1/2 and the component-side viewing convention.
5. Record photos and measured results in the project log before modifying or routing any related nets.

This note records *period-source evidence*, not the result of those pending bench measurements.
