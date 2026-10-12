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
| **69** | **“MOTHER BD. MEMORIES OFF”**, *if used* | **JP2-1 via MB_RAM_DISABLE net; JP2-2 to GND (closed shunt reproduces known-working Hyperboard in slot 5)** |

The original board also uses TPA (through a gate marked **74C07**) with memory address latch circuitry. This independently supports the design approach of buffering the **high address byte**, but the exact latch edge and propagation margins still need CDP1802 and 74HCT datasheet review.

The original uses a large 2102 memory array, jumpers and a more elaborate bank select decoder. Our 62256 design is *not* a direct electrical clone and must be validated independently.

## Contact 69 — known-working Slot-5 inhibit

- The Hyperboard Rev 2 manufacturing Gerber assigns its P3 pad 69 to GND.
- The historical Netronics 4K memory board identifies the corresponding
  original contact 69 as **`MOTHER BD. MEMORIES OFF`** (`IF USED`).
- **Established prior project behavior (user-confirmed):** the Hyperboard
  installed in expansion **slot 5** disables motherboard RAM on the user's
  original Netronics ELF II. That resolves the previous blanket uncertainty
  about this function on that specific machine/slot configuration.
- The standalone card uses the same original RAM-disable input via an
  intentional jumper: J1-69 -> JP2-1, JP2-2 -> GND. **A closed JP2 shunt**
  reproduces the Hyperboard's grounded contact 69; with JP2 open,
  original motherboard RAM is not disabled by this card.
- The previous routed `experiment/hyperboard-route-ceee8d6e` preview
  left J1-69 open and is superseded for this function. The revised PCB
  routing and tests must confirm the actual copper path to JP2.
- Contact 82 remains NC until separately identified. A positive Slot-5
  result does not prove behavior with alternate motherboard revisions
  or differently configured expansion slots.

## Practical coexistence implications

- J1-69's grounded Slot-5 memory-disable action has already been established by the known-working Hyperboard; use JP2 to make that ground connection only when needed, particularly with low RAM mapped at `0000`.
- If the motherboard 2101 RAM remains enabled, overlapping read cycles may drive the data bus simultaneously, corrupting data or stressing IC outputs. Having the new RAM's selection truth table pass does not prove safe coexistence.
- Giant Board installed means its ROM and RAM decoding must be checked separately for overlaps with `0000–7FFF` and `8000–FFFF`.

## Recommended unpowered measurements on the early original ELF II

1. For any different motherboard or slot, identify pin 69 on the correct contact face and compare it against the already established Slot-5 behavior; do not use an unknown contact as a general ground return.
2. Check continuity between pin 69 and motherboard memory decode / RAM enable pins using original schematic references.
3. Determine whether pin 82 is actually bonded to connector ground (or different on this revision).
4. Verify edge connector orientation, including contact 1/2 and the component-side viewing convention.
5. Record photos and measured results in the project log before modifying or routing any related nets.

The original schematic/Gerber facts above are **source-derived**; the Slot-5 functional result is **user-confirmed previous bench work**, not an inference from the schematic alone.
