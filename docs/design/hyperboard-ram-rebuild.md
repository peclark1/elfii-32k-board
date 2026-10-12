# Hyperboard-derived RAM rebuild — source of truth

## Decision

The A5 schematic/PCB is retained in Git history as a routing study, but the electrical design is being rebuilt from the AVI Hyperboard Rev 2 RAM architecture.

Primary source: `AVIELF2HYPERBOARD-KiCad-Rev2.pdf` (Rev 2.0, 2026-03-17).

The pin-by-pin trace and source cross-check are recorded in [hyperboard-ram-circuit-trace.md](hyperboard-ram-circuit-trace.md). That document supersedes earlier notes that incorrectly treated the Hyperboard connector net `RAM_CE` as the CY62256 chip-select.

## Standalone architecture

### ELF II expansion bus

Keep the existing verified 86-contact edge connector geometry. Required source contacts are:

- TPA: P3-28
- /MRD: P3-30
- /MWR: P3-24
- D7..D0: P3-34,38,42,46,50,54,58,62
- MA7..MA0: P3-36,40,44,48,52,56,60,64
- optional motherboard-RAM-disable contact: P3-69, **default open and still early-Netronics-unverified**
- +5 V / GND from the already documented power contacts.

### High-address latch — Hyperboard A8, 74HC573

Copy the Hyperboard mapping exactly:

- pin 2 D0 <- MA7; Q0 pin 19 -> A15
- pin 3 D1 <- MA6; Q1 pin 18 -> A14
- pin 4 D2 <- MA5; Q2 pin 17 -> A13
- pin 5 D3 <- MA4; Q3 pin 16 -> A12
- pin 6 D4 <- MA3; Q4 pin 15 -> A11
- pin 7 D5 <- MA2; Q5 pin 14 -> A10
- pin 8 D6 <- MA1; Q6 pin 13 -> A9
- pin 9 D7 <- MA0; Q7 pin 12 -> A8
- pin 11 Load <- TPA
- pin 1 /OE -> GND
- pin 20 VCC -> +5 V; pin 10 -> GND.

### SRAM — Hyperboard A11, CY62256-70PC

- A0..A7 <- MA0..MA7 directly.
- A8..A14 <- latched A8..A14.
- D0..D7 <-> bus D0..D7.
- /OE pin 22 <- /MRD.
- /WE pin 27 <- /MWR.
- /CS pin 20 <- **74LS151 U1 /Z pin 6**.
- pin 28 +5 V; pin 14 GND.

A15 is not a 62256 address input. It qualifies the LS151 enable so the RAM occupies only the selected 32K half.

### 4K page select — Hyperboard U1/SW1/RN3

Copy the source page selector:

- U1 = 74LS151.
- S0/S1/S2 = A12/A13/A14.
- I0..I7 = 0000,1000,...7000 page-enable switch states.
- SW1 connects an enabled page to +5 V.
- RN3 provides one 22K pull-down per page.
- U1 Z pin 5 is unused.
- U1 /Z pin 6 directly drives SRAM /CS.

### 32K-half select

The Hyperboard's 2x2 J8 simultaneously maps RAM and ROM. The standalone card needs only the RAM half, so simplify this shared circuit to:

- a 1x3 LOW/HIGH jumper with common -> U1 /E;
- LOW endpoint -> A15;
- HIGH endpoint -> /A15;
- one source-derived CD4011 NAND gate with both inputs tied to A15 to produce /A15.

This is electrically equivalent to the RAM side of Hyperboard J8 without copying ROM/autoboot plumbing. Unused 4011 inputs must be tied to a defined level.

### P3-69 / RAM_CE

The Hyperboard labels P3-69 `RAM_CE` and ties that connector net to GND. The copper Gerber therefore correctly reports pad 69 as GND.

That connector signal is **not** the Hyperboard SRAM /CS. On this standalone board it is only an optional motherboard-RAM-disable function. Provide a normally-open jumper from P3-69 to GND and retain the existing warning that early-Netronics behavior must be bench verified before use.

## Omitted Hyperboard functions

Do not copy the 28C256 ROM, UART, cassette circuitry, CDP1853 I/O decoding, autoboot flip-flops, ROM Hi-Z logic, or unrelated 74HC244 buffering.

The source A13A 74HC74 belongs to the shared memory/boot block and is not required for the standalone RAM path. The Rev 2 drawing also reuses the A15 net name around that flip-flop in a way that is not useful to reproduce. The standalone design uses the already-latched A15 from the 74HC573 directly.

## Rebuild sequence

1. Replace the old custom 74HCT273/XOR/OR schematic with P3 -> 74HC573 -> CY62256.
2. Add the exact 74LS151 + 8-position 4K page selector.
3. Add the RAM-only LOW/HIGH half selector and source-derived 4011 inverter.
4. Add optional P3-69 motherboard-RAM-disable jumper, default open.
5. Add explicit power, one 0.1uF bypass per IC, local bulk capacitance, and defined unused inputs.
6. Run real KiCad 9 ERC.
7. Export a KiCad netlist and enforce the source pin map in automated regression tests.
8. Only after the schematic passes, replace the old PCB netlist/placement and reroute.

The previous routed PCB remains proof that a two-layer implementation is feasible; it is not a constraint on the new electrical design.
