# Hyperboard-derived RAM rebuild — source of truth

## Decision

The current A5 schematic/PCB is retained in Git history for comparison, but the electrical design is being restarted from the proven AVI Hyperboard Rev 2 RAM architecture rather than continuing the custom 74HCT273/XOR/OR decode.

Primary source: `AVIELF2HYPERBOARD-KiCad-Rev2.pdf` (Rev 2.0, 2026-03-17).

## Core circuit copied from the Hyperboard

### ELF II expansion bus
Use the existing verified 86-contact edge connector geometry and these Hyperboard signal contacts:
- TPA: P3-28
- /MRD: P3-30
- /MWR: P3-24
- D7..D0: P3-34,38,42,46,50,54,58,62
- MA7..MA0: P3-36,40,44,48,52,56,60,64
- optional motherboard memory-disable contact: P3-69
- +5 V / GND from existing documented power contacts.

### High-address latch — Hyperboard A8, 74HC573
Copy the Hyperboard pin mapping exactly:
- pin 2 D0 <- MA7, Q0 pin 19 -> A15
- pin 3 D1 <- MA6, Q1 pin 18 -> A14
- pin 4 D2 <- MA5, Q2 pin 17 -> A13
- pin 5 D3 <- MA4, Q3 pin 16 -> A12
- pin 6 D4 <- MA3, Q4 pin 15 -> A11
- pin 7 D5 <- MA2, Q5 pin 14 -> A10
- pin 8 D6 <- MA1, Q6 pin 13 -> A9
- pin 9 D7 <- MA0, Q7 pin 12 -> A8
- pin 11 Load <- TPA
- pin 1 /OE -> GND
- pin 20 VCC -> +5 V; pin 10 -> GND.

This replaces the experimental 74HCT273 clock/inverter arrangement.

### SRAM — Hyperboard A11, CY62256-70PC / compatible 62256
Copy the Hyperboard connections:
- SRAM A0..A7 <- MA0..MA7 directly.
- SRAM A8..A14 <- latched A8..A14.
- SRAM D0..D7 <-> bus D0..D7.
- /OE pin 22 <- /MRD.
- /WE pin 27 <- /MWR.
- /CS pin 20 <- RAM_CE.
- pin 28 +5 V, pin 14 GND.

A15 is not an SRAM address input; it is available for 32K-half / memory-map control.

### 4K page map — Hyperboard U1/SW1 concept
The Hyperboard uses a 74LS151 with A12/A13/A14 as its select inputs and an 8-position map switch labelled 0000,1000,...7000. Each switch input has a 22K pull-down. This lets RAM participation be selected in 4K pages rather than forcing all 32K to respond.

For our dedicated card this is valuable on an original ELF II:
- leave the 0000 page off while the motherboard RAM remains active, or
- optionally use the documented memory-disable bus contact and enable the entire low 32K.

Do **not** copy the Hyperboard ROM/autoboot circuitry merely to obtain RAM. J6/J8 and the 74HC74/4011 logic serve RAM/ROM/boot mode selection on the combined Hyperboard and will be treated separately if a high/low-32K selector is desired.

## Rebuild sequence

1. Replace the current schematic with a clean P3 -> 74HC573 -> 62256 drawing.
2. Add the 74LS151 + 8-position 4K RAM map exactly as the source circuit.
3. Add optional motherboard-RAM-disable jumper on P3-69, default open.
4. Decide whether a dedicated high/low 32K selector is useful; if so, copy only the relevant Hyperboard J8/A15 gating after tracing it exactly.
5. Run KiCad ERC and a pin-by-pin regression against this source map.
6. Only after the schematic is accepted, discard/reroute the PCB from the new netlist.

The existing routed PCB is therefore a historical/proof-of-routability reference, not the basis of the rebuild.
