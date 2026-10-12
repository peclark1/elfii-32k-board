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
