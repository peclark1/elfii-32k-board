# AVI Hyperboard Rev 2 P3 connector netlist extracted from copper Gerbers

Source: user-supplied `AVIELF2HYPERBOARD-Rev-2-gerbers (2).zip`, `F_Cu.gbr` and `B_Cu.gbr`, with embedded KiCad X2 attributes `%TO.P,P3,<number>,<number>*%` and `%TO.N,<net>*%`.

**This is an exact transcription of the Hyperboard Gerber exports, NOT yet an independent verification against the early original Netronics ELF II motherboard pinout.**

Front copper has even pad numbers, back copper odd pad numbers. 43 pads each. X position descends from 173.5836 mm (1/2) to 66.9036 mm (85/86). 
X-named nets on the back side are bus extension conductors and are NOT necessarily generic user-ready signals. Several unassigned pads lacked net attributes; those are marked `NC/unassigned`, not confirmed electrically unconnected on every other ELF variant.

| Pad | Copper face | Gerber net |
| ---: | :---: | --- |
| 1 | B | +5V |
| 2 | F | +5V |
| 3 | B | NC/unassigned |
| 4 | F | NC/unassigned |
| 5 | B | GND |
| 6 | F | CLOCK |
| 7 | B | NC/unassigned |
| 8 | F | /CLOCK |
| 9 | B | +8V |
| 10 | F | /LOAD |
| 11 | B | NC/unassigned |
| 12 | F | /DMA_IN |
| 13 | B | X13 |
| 14 | F | RUN |
| 15 | B | -8V |
| 16 | F | /DMA_OUT |
| 17 | B | X17 |
| 18 | F | Q |
| 19 | B | X19 |
| 20 | F | /INT |
| 21 | B | X21 |
| 22 | F | SC1 |
| 23 | B | X23 |
| 24 | F | /MWR |
| 25 | B | X25 |
| 26 | F | SC0 |
| 27 | B | X27 |
| 28 | F | TPA |
| 29 | B | X29 |
| 30 | F | /MRD |
| 31 | B | X31 |
| 32 | F | TPB |
| 33 | B | X33 |
| 34 | F | D7 |
| 35 | B | X35 |
| 36 | F | A7 |
| 37 | B | X37 |
| 38 | F | D6 |
| 39 | B | X39 |
| 40 | F | A6 |
| 41 | B | X41 |
| 42 | F | D5 |
| 43 | B | X43 |
| 44 | F | A5 |
| 45 | B | X45 |
| 46 | F | D4 |
| 47 | B | X47 |
| 48 | F | A4 |
| 49 | B | I64 |
| 50 | F | D3 |
| 51 | B | I65 |
| 52 | F | A3 |
| 53 | B | I66 |
| 54 | F | D2 |
| 55 | B | I67 |
| 56 | F | A2 |
| 57 | B | I63 |
| 58 | F | D1 |
| 59 | B | CASS_OUT |
| 60 | F | A1 |
| 61 | B | CASS_IN |
| 62 | F | D0 |
| 63 | B | I62 |
| 64 | F | A0 |
| 65 | B | I61 |
| 66 | F | /EF1 |
| 67 | B | I6C |
| 68 | F | N2 |
| 69 | B | GND |
| 70 | F | /EF2 |
| 71 | B | I6D |
| 72 | F | N1 |
| 73 | B | I6E |
| 74 | F | /EF3 |
| 75 | B | I6F |
| 76 | F | N0 |
| 77 | B | I6B |
| 78 | F | /EF4 |
| 79 | B | I6A |
| 80 | F | GND |
| 81 | B | SYNC |
| 82 | F | NC/unassigned |
| 83 | B | I69 |
| 84 | F | X84 |
| 85 | B | DISP_STAT |
| 86 | F | BUS_CLK |

## Critical distinction

The Hyperboard uses net labels `A0`–`A7` on even-numbered contacts. These are the 1802 multiplexed MA pins in the expansion-bus context, not a guaranteed continuously valid low address. Correct TPA address latching and address phase remain necessary.

## Update status
- The reusable connector footprint and its placed instance have been renumbered from temporary `F01/B01` labels to the actual copper-Gerber physical numbers `1`–`86`.
- Contact geometry was cross-checked against the **copper** Gerber aperture `D19`, which also reports a 1.397 × 8.890 mm rectangle (same as mask).
- Orientation still requires checking in KiCad using the original board's mating edge and component side.
- Actual electric symbol and footprint/schematic association still pending.
- No manufacturing claim about hard-gold fingers or bevel is made.
