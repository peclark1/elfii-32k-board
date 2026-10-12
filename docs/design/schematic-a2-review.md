# Schematic review — Rev A2

This review records what is verified and what still needs confirmation before routing.

## Confirmed from the owner's early Netronics ELF II assembly manual

The page labelled **ELF II BUS DEFINITION — connector viewed from component side of PC board** gives:

| Board contact | Original signal legend | Our schematic label |
| ---: | --- | --- |
| 1, 2 | +5 | VCC |
| 5, 80 | GND | GND |
| 69 | Not independently verified from this manual illustration | GND (Hyperboard Gerber label; needs cross-check) |
| 24 | MWR | NMWR |
| 28 | TPA | TPA |
| 30 | MREAD | NMRD |
| 34/38/42/46/50/54/58/62 | D7...D0 | D7...D0 |
| 36/40/44/48/52/56/60/64 | A7...A0 (multiplexed CDP1802) | MA7...MA0 |

The external-bus connector illustration must not be mistaken for the IC itself. Electrical polarity is **not explicitly established by the drawing alone**. Our labels NMRD/NMWR and the negative logic are based on CDP1802 signal behavior and require review against the actual early motherboard.

**Important mechanical point:** the manual explicitly states *component-side viewing direction*. Compare pad numbering on the KiCad PCB and face of the actual Netronics socket before fabrication; Gerber front/back metadata by itself is not sufficient to confirm connector insertion orientation.

## Electrical truth-table assumptions to verify

- The CDP1802 high-address byte is present on MA0–MA7 during TPA, and the low-address byte follows.
- U3 inverted TPA is used as U1 74HCT273 active-positive CLK. That implies high-byte capture on TPA's falling edge, **not** an assumption that the latch clock is a direct TPA pulse.
- U2 SRAM /CE is enabled in the selected 32K half whenever card enabled; /OE and /WE are gated by the board's memory read/write signals.
- A disabled card leaves all SRAM data pins three-state.
- On-board 2101 RAM and Giant Board ROM/RAM decode may overlap either half of address space. **No half is declared safe yet.**

## Schematic presentation changes

- Net labels on left-facing IC and connector pins now align outward rather than over the device body.
- 62 deliberately unused edge-connector pins have been marked with KiCad no-connect symbols (the other 24 pins are wired in the draft).
- There are no functional changes to the SRAM /CE, /OE, /WE logic in this step.
- KiCad CI now exports an actual schematic PDF into the workflow artifact for an easier human review.

## ERC preparation / outstanding work

- KiCad 7 on Ubuntu 24.04 supports CLI PDF/netlist/Gerber export, but **not** `sch erc` or `pcb drc`. Run these in KiCad GUI or update the CI runner to a CLI release that supports those subcommands.
- The 5 V source enters through passive J1 contacts. The schematic may need explicit PWR_FLAG objects to satisfy ERC 'power input not driven' warnings. Add only after observing the actual ERC report.
- Decide whether connector unused signals should remain untouched as marked or exposed with test pads for diagnostics.
- Compare HCT propagation/setup and address hold with CDP1802 clock frequency, SRAM access time and signal loading.
- Validate physical edge connector and initial board component placement independently.
- Verify the sockets, Giant Board, and onboard 2101 RAM configuration before applying power.

Do **not** order from the CI-generated Gerbers. They are for import/export verification only.
