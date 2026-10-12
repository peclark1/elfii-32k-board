# Hyperboard Rev 2 SRAM circuit trace

Primary electrical reference: `AVIELF2HYPERBOARD-KiCad-Rev2.pdf`, Rev 2.0 dated 2026-03-17. Cross-check: `AVIELF2v1-Sch.pdf` (AVI ELF II motherboard).

This note records the source schematic as drawn before adapting it to the standalone 32K card. The important correction from the earlier design is that the Hyperboard connector net named `RAM_CE` is **not** the CY62256 chip-select net.

## Circuit inventory

| Ref | Part | Relevant source pins / nets | SRAM role | Standalone disposition |
| --- | --- | --- | --- | --- |
| P3 | ELF II 86-contact edge connector | 24 `/MWR`; 28 `TPA`; 30 `/MRD`; 34/38/42/46/50/54/58/62 = D7..D0; 36/40/44/48/52/56/60/64 = multiplexed A7..A0; 69 = source net `RAM_CE` | Brings the 1802 multiplexed address, data and memory controls to the card | Keep existing verified mechanical geometry. J1-69 → JP2-1, JP2-2 grounded, shunt normally open; Slot-5 disable behavior established; J1-82 stays NC. |
| A8 | 74HC573 | D0 p2<-MA7, D1 p3<-MA6, D2 p4<-MA5, D3 p5<-MA4, D4 p6<-MA3, D5 p7<-MA2, D6 p8<-MA1, D7 p9<-MA0; Q0 p19=A15, Q1 p18=A14, Q2 p17=A13, Q3 p16=A12, Q4 p15=A11, Q5 p14=A10, Q6 p13=A9, Q7 p12=A8; LE/Load p11=TPA; /OE p1=GND; VCC p20, GND p10 | Captures the high address byte while the 1802 MA bus is in its high-address phase | **Keep exactly.** This replaces the experimental 74HCT273/inverter arrangement. |
| A11 | CY62256-70PC | A0..A7 p10,9,8,7,6,5,4,3 <- MA0..MA7; A8..A14 p25,24,21,23,2,26,1 <- latched A8..A14; Q0..Q7 p11,12,13,15,16,17,18,19 <-> D0..D7; /OE p22=/MRD; /WE p27=/MWR; /CS p20 from U1 /Z; VCC p28, GND p14 | 32K x 8 SRAM | **Keep exactly.** |
| SW1 | 8-position DIP | left/common side tied +5V; positions labelled 0000,1000,...7000; right side drives U1 I0..I7 | Enables individual 4K pages within the selected 32K half | **Keep concept and pin ordering.** |
| RN3 | 22K bussed resistor network | one 22K pull-down on each SW1/U1 data-input node; common to GND | Makes an open page switch a definite logic 0 | **Keep.** |
| U1 | 74LS151 | I0 p4=0000, I1 p3=1000, I2 p2=2000, I3 p1=3000, I4 p15=4000, I5 p14=5000, I6 p13=6000, I7 p12=7000; S0 p11=A12, S1 p10=A13, S2 p9=A14; /E p7 is half-select qualification; Z p5 unused; /Z p6 -> CY62256 /CS p20; VCC p16, GND p8 | Selects the DIP state for the current 4K page. When the selected switch is ON, the selected input is 1 and /Z goes low, selecting SRAM. | **Keep.** This is the Hyperboard RAM chip-select mechanism. |
| J8 | 2x2 memory-map jumper | RAM side uses p1=A15 and p2=U1 /E. Other side participates in complementary ROM selection. Source legend shows horizontal orientation = RAM low 32K / ROM high 32K; vertical orientation = ROM low 32K / RAM high 32K. | Chooses whether U1 is enabled for A15=0 or A15=1 | **Simplify.** On the standalone card use a 1x3 LOW/HIGH jumper: common -> U1 /E; LOW endpoint -> A15; HIGH endpoint -> /A15. Do not copy the ROM leg. |
| A7D | CD4011 NAND gate | both inputs are driven from the RAM/ROM A15-select path; output supplies the complementary half-select used by J8 | Provides the inverted A15 sense for the alternate 32K half | **Keep the function.** Use one 4011 gate as the source-derived inverter and tie unused 4011 inputs to a defined level. |
| A13A | 74HC74 | D p2 is drawn from an A15-labelled net, C p3=BUS_CLK, Q p5 is also labelled A15, /Q p6 labelled /A15 | Part of the Hyperboard memory/boot selection block | **Do not copy.** The Rev 2 drawing reuses the A15 net name on both the D-side source and Q output, so copying this block would add source ambiguity without benefit. The standalone card already has a valid latched A15 at A8 Q0. |
| A13B, J6, J7 | 74HC74 + BOOT jumpers | BOOT/RUN state logic | Hyperboard autoboot / ROM Hi-Z behavior | **Omit.** |
| A10 | 28C256 | ROM address/data, /OE=/MRD, /CS from ROM selection | ROM | **Omit.** |
| A9 | 74HC244 | shared buffering elsewhere on Hyperboard | Not required for the SRAM path traced above | **Omit.** |
| A1/A2 | CDP1853 | I/O decode | Not in the SRAM address/data/control path | **Omit.** |

## Exact memory path

The 1802 expansion bus carries a multiplexed `MA0..MA7` bus. During the high-address phase, A8 captures it on `TPA` with the bit ordering used by both AVI designs: MA7 becomes A15, MA6 becomes A14, ..., MA0 becomes A8. After that phase the same bus carries the low byte and feeds SRAM A0..A7 directly.

Therefore a memory cycle is visually:

`P3 MA[0..7] -> A8 74HC573 -> A[8..15]`

and in parallel after TPA:

`P3 MA[0..7] -> A11 A[0..7]`

with `A8..A14` from the latch feeding the upper seven address pins of the 62256.

Data is direct and bidirectional:

`P3 D[0..7] <-> A11 Q[0..7]`

The SRAM controls are likewise direct except chip select:

- `/MRD -> A11 /OE`
- `/MWR -> A11 /WE`
- `U1 /Z -> A11 /CS`

## RAM chip select and 32K-half selection

The source 74LS151 is the crucial RAM-select device.

`A12,A13,A14` select one of eight 4K-page switch inputs. Each page input is normally pulled low by RN3; closing that page's SW1 section connects it to +5V. With U1 enabled, an ON page therefore produces low on U1 `/Z`, which directly selects the CY62256.

U1 `/E` is active low and supplies the A15 qualification. Hyperboard J8 routes either the A15 sense or its complement into that enable path, while the other half of J8 simultaneously maps the ROM to the opposite 32K half. The standalone board does not need the ROM half of this circuit, so the equivalent RAM-only control is:

- LOW 32K: `U1 /E = A15` (enabled when A15=0)
- HIGH 32K: `U1 /E = /A15` (enabled when A15=1)

A 1x3 LOW/HIGH jumper is clearer than copying the Hyperboard's 2x2 RAM+ROM jumper.

## Important RAM_CE correction

The Hyperboard schematic labels P3 contact 69 `RAM_CE`, but that net is separately shown tied to GND. The Rev 2 copper Gerber therefore reports pad 69 as GND. This is consistent: the connector signal is a motherboard/onboard-RAM control, not A11 pin 20.

**Do not connect P3-69 to CY62256 /CS.** The CY62256 /CS comes from U1 pin 6 (/Z).

On the standalone board P3-69 should only be offered through an optional, normally-open motherboard-RAM-disable jumper to GND, and it is **already known from Slot-5 testing to disable motherboard RAM**. Do not permanently bond J1-69 to GND.

## Cross-check against the AVI ELF II motherboard

The AVI ELF II motherboard independently confirms the core architecture:

- it uses a 74HC573 with the same reversed high-byte capture (MA7->A15 ... MA0->A8);
- the 573 Load input is TPA and /OE is grounded;
- the CY62256 uses direct low address, direct D0..D7, `/MRD -> /OE`, and `/MWR -> /WE`.

Its 8-position RAM DIP is **not** the same chip-select mechanism as the Hyperboard. On the motherboard, seven switch sections connect latched system A8..A14 to the SRAM's seven upper address inputs (with 22K pull-downs), effectively controlling address mapping/mirroring. The SRAM `/CE` is controlled separately by the motherboard's `RAM_CE` logic through an inverter.

For a plug-in expansion card that must become electrically inactive in unselected regions, the Hyperboard's 74LS151 page-select architecture is the appropriate reference. It explicitly controls SRAM /CS and can leave selected 4K pages disabled rather than merely aliasing SRAM addresses.

## Standalone adaptation chosen

The rebuild will therefore use:

- 74HC573 high-address latch;
- CY62256-70PC/compatible 62256;
- 74HC151 pin-compatible 4K-page selector (intentional TTL LOW-current adaptation of source 74LS151);
- 8-position DIP + 8 x 22K pull-down network;
- one CD4011 gate to create /A15, with unused inputs tied;
- one 1x3 LOW/HIGH 32K-half jumper;
- optional normally-open P3-69-to-GND motherboard-RAM-disable jumper;
- one 0.1uF bypass capacitor per IC plus local bulk capacitance.

ROM, UART, cassette, I/O decoders, CDP1853 logic, boot flip-flops and data buffering that exist for other Hyperboard functions are intentionally omitted.
