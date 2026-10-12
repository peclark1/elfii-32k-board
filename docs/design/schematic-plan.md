# KiCad schematic plan — Rev A

Status: design specification only; no electrical netlist has been approved.

## Sheet 1: ELF II bus and power
- J1: physically verified Netronics 86-contact 0.1-inch-class edge fingers (pitch and finger geometry **TBD by measurement**).
- Add explicit, numbered net labels and per-IC 100 nF bypass capacitors.
- Include card-enable jumper with pull resistor ensuring an unambiguous disabled state when open.

## Sheet 2: Address capture
- U1: 74LS273 (or timing-verified alternative).
- MA0–MA7 sampled on TPA to yield A8–A15.
- During memory access MA0–MA7 are the A0–A7 input to RAM; qualify setup/hold and timing.
- Verify latch clock polarity; transistor/logic inversion only if timing requires it.

## Sheet 3: SRAM and chip select
- U2: 62256-compatible DIP-28 32K × 8 SRAM.
- A0–A7 from low-byte MA bus; A8–A14 from latched upper address.
- Latched A15 determines lower versus upper 32K region.
- Decoder generation conditional on region selection, card enable and memory cycle.
- /OE controlled by /MRD and selected-chip qualification.
- /WE controlled by /MWR and selected-chip qualification.
- Use timing-verified NAND/NOR/inverter gates. The 74LS138 shown in earlier concept art is not inherently needed for a single A15 half-space selection; minimize parts.
- Define unused/floating CMOS/TTL inputs and power-up default states.

## Initial mapping choices
| Selector | Address span | Notes |
| --- | --- | --- |
| LOW | 0000–7FFF | Default conceptual target, original ELF II low RAM conflict must be resolved |
| HIGH | 8000–FFFF | May overlap Giant Board/Hyperboard ROM; check before using |
| DISABLED | none | For diagnostics |

## Required control truth-table tests
- Disabled: SRAM never enables or drives D0–D7; writes blocked.
- Selected READ: /CE=0, /OE=0, /WE=1.
- Selected WRITE: /CE=0, /OE=1, /WE=0.
- Nonselected access: /CE=1, /OE=1, /WE=1.
- Reset / non-memory cycles: explicitly specify outputs and bus state.

## Work sequence
1. Exact connector assignment and schematic symbols/footprint.
2. High address latch circuit from cited drawings.
3. Decoder/read/write circuit, logic simulation or truth-table review.
4. Real KiCad schematic + ERC.
5. Component placement and PCB routing + DRC.
6. Hardware fabrication only after documented review.
