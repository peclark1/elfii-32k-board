# ELF II 32K Static RAM Expansion

A standalone, period-styled **32 KiB SRAM expansion board** for the original Netronics ELF II (RCA CDP1802) expansion bus.

**Status: research / initial schematic design. Not electrically verified; do not fabricate yet.**

## Goals

- Use one through-hole 62256-compatible 32K × 8 SRAM and conventional through-hole logic.
- Connect to the **original 86-contact Netronics ELF II bus**, using a verified edge connector footprint and pin numbering.
- Latch the **high address byte A8–A15 at TPA**; use the later MA0–MA7 low byte as A0–A7. The previous visual mockup incorrectly reversed this.
- Select the 32K region (0000–7FFF or 8000–FFFF) with an unmistakable hardware setting; default to **LOW** for stand-alone RAM use, subject to compatibility review.
- Allow a physical disable jumper and avoid bus contention with onboard 2101 RAM, Giant Board, and Hyperboard memory.
- Mimic the appearance and dimensions of original period Netronics expansion hardware where practical.

## Documents

- [Design goals](docs/design/design-goals.md)
- [Bus signal verification](docs/design/bus-signals.md)
- [Schematic plan](docs/design/schematic-plan.md)
- [Memory mapping and compatibility](docs/design/compatibility-notes.md)
- [Original documentation review](docs/reference/source-notes.md)

## KiCad

The **KiCad PCB now contains the measured Hyperboard Rev 2 outline and 86-contact edge connector**, and project-local libraries contain a matching two-unit schematic symbol with copper-Gerber-derived pin numbering. The schematic is not electrically connected, and no board fabrication is authorized. Do not treat earlier generated pictures as wiring drawings. The next stage is to implement the 1802/Netronics bus interface with reviewable signal names, footprint assignments and ERC checks.

## License

License selection is pending. Historical source drawings may have separate copyrights; they are references, not assumed freely redistributable assets.

## Electrical schematic progress (draft)

An initial connected KiCad schematic (U1–U5, J1, JP1–JP2, R1–R2, C1–C5) is committed. It uses actual DIP pin numbers, net labels, and the two-unit 86-contact connector, plus a project-local `ELFII_32K.kicad_sym` library. See [electrical design](docs/design/sram-electrical-design.md) and the [truth-table test](tests/test_ram_select_logic.py). **KiCad 9 schematic ERC now passes with 0 errors and 0 warnings; bus timing and physical compatibility remain unverified.**

## Original early ELF II compatibility checks

The original Netronics 4K memory-board schematic identifies expansion contact **69** as **“MOTHER BD. MEMORIES OFF” (if used)**, whereas the AVI Hyperboard Rev 2 manufacturing netlist labels the same contact as GND. **Do not connect contact 69 to GND on the original motherboard without verification.** The current 32K expansion PCB and schematic leave contact 69 unconnected and note its historical function; contact 82 likewise remains NC pending measurement. See [period-source cross-check](docs/reference/original-4k-board-crosscheck.md) and the [bench verification procedure](docs/design/early-elfii-bus-bench-validation.md).

The schematic documents a potential low-32K overlap with the original ELF II memory. The schematic now passes KiCad 9 ERC, but motherboard/Giant Board electrical coexistence and PCB DRC **are not yet verified/cleared; do not fabricate or install yet**.

## Current engineering milestone (Rev A3)

Conventional multi-unit gate symbols are in the KiCad schematic; all tested pin/net connections were preserved. **Actual KiCad 9 schematic ERC now reports 0 errors and 0 warnings.** The board remains unrouted, with **100 PCB DRC violations and 87 unconnected items** requiring further work. See [verified ERC cleanup](docs/design/erc-cleanup-a3.md) and [revision A3 gate map](docs/design/gate-symbols-a3.md).

## Completion criteria — visible wiring and routed PCB

**Engineering status: INCOMPLETE.** KiCad's clean ERC currently verifies a schematic that makes most connections through global net labels on short pin stubs. It is electrically connected in the netlist, but it does **not** provide an easy-to-follow wired circuit diagram. The PCB contains placed parts and net assignments but **zero routed copper tracks** (87 unconnected items in the last KiCad DRC).

Before calling the circuit complete:

1. **Make the schematic legible:** draw and label the actual interconnections between the 1802 expansion bus, address latch, 62256 SRAM, decoder gates, configuration jumpers and power/decoupling. Use buses or clearly named off-page connectors only where they improve legibility; no unexplained label-only spaghetti. Inspect the exported PDF at readable scale.
2. **Re-run full ERC and pin/net regression tests** and compare the exported netlist before and after rewiring, detecting accidental electrical changes.
3. **Resolve bus compatibility:** early motherboard 2101 RAM overlap and optional memory-disable contact 69, contact 82 uncertainty, Giant Board memory map, and timing/voltage margins before enabling a bank on the physical ELF II.
4. **Replace first-pass simplified PCB footprints** with authoritative KiCad library footprints; review component placement and edge-connector finger fabrication rules.
5. **Actually route all intended PCB nets** with copper traces and appropriate +5V/GND distribution. A ground zone alone is not equivalent to a fully routed board.
6. **Run full PCB DRC and visually review Gerbers.** All unconnected items must be resolved; remaining edge-connector exceptions must be deliberately reviewed, not hidden as generic design-rule suppressions.

**Passing ERC, pin/net tests, or Gerber export does not satisfy items 1, 5 or 6. Do not fabricate the current board.**
