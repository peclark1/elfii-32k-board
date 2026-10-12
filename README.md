# Netronics ELF II — Standalone 32 KiB SRAM Expansion Card

A period-styled, through-hole 32 KiB SRAM card for the **original Netronics
ELF II / RCA CDP1802 expansion bus**, designed to use the full-size historical
86-contact, two-sided expansion-card outline.

**Engineering status: active Hyperboard-derived redesign. No fabrication
authorization; do not insert the PCB into a working ELF II yet.**

## Current electrical design

The first-generation custom 74HCT273/XOR/OR implementation is **superseded**.
The active schematic follows the AVI ELF II Hyperboard Rev 2 RAM circuit:

- **U1 74HC573:** transparently captures multiplexed high address A8–A15
  during TPA; direct MA0–MA7 become the low byte A0–A7.
- **U2 CY62256-compatible 32K × 8 SRAM:** direct D0–D7, /MRD to /OE,
  /MWR to /WE, and decoded active-low /CS.
- **U3 74HC151:** selects which of eight 4 KiB pages are enabled by SW1,
  with RN1 providing 22 kΩ pull-downs. The HC151 is an intentional
  pin-compatible reliability adaptation of the original Hyperboard LS151
  (documented TTL LOW-current concern).
- **U4 CD4011:** derives complementary A15 for a simple selectable
  LOW $0000–$7FFF versus HIGH $8000–$FFFF memory half.
- Local decoupling, a bulk capacitor and an optional *normally open*
  early-Netronics motherboard-RAM-disable feature.

The 86 edge pads and original measured card outline are **not being
redesigned**. The new circuit omits the Hyperboard's ROM, UART, I/O,
cassette and boot functions.

## KiCad schematic and PCB status

- `hardware/kicad/elfii-32k-board.kicad_sch` is the **active new
  Hyperboard-derived schematic**. KiCad 9 ERC and pin-specific netlist
  regression tests have passed (138 checked pin memberships across 41 nets).
- `hardware/kicad/elfii-32k-board.kicad_pcb` is synchronized with the active electrical schematic on the **dedicated review branch**. `main` continues to retain its older A5 PCB study until final release gates are met.
- `scripts/build_pcb_candidate.py` creates a physically preserved,
  new-architecture through-hole PCB from the current KiCad netlist,
  without touching the obsolete PCB traces. The initial candidate has
  14 footprints and begins unrouted.
- `.github/workflows/hyperboard-routing-trial.yml` runs an isolated
  Freerouting trial on the new candidate, then checks a separate routed
  PCB using native KiCad 9 DRC and uploads reviewable results as a GitHub
  Actions artifact. Routing results are **experimental**, not yet promoted
  to the authoritative PCB.

The `SCHEMATIC_REBUILD_IN_PROGRESS` marker keeps outdated PCB
consistency/DRC checks from mistakenly accepting the old file as current.
It is removed only after a genuine schematic-to-PCB synchronization.

## Verified routing milestone — 12 October 2026

The initial 426-track/27-via trial was superseded by the coordinator-accepted [revised 438-track, 35-via Hyperboard PCB preview](https://github.com/peclark1/elfii-32k-board/tree/experiment/hyperboard-route-b57bb49a), where **J1-69 is physically routed to JP2-1**. The [pre-fabrication review branch](https://github.com/peclark1/elfii-32k-board/tree/feature/hyperboard-pcb-prefab-review) adds two GND zones, moves a dangerous +5V via out of the finger region, and independently verifies the copper in CI. This is a **review only, not fabrication authorization**. See [the updated PCB review](docs/design/prefabrication-layout-review-2026-10-12.md), [measured +5V and decoupling paths](docs/design/prefab-power-and-decoupling-measurements-2026-10-12.md), and [the historical checkpoint](docs/design/hyperboard-routing-checkpoint-2026-10-12.md).

## Critical safety holds

1. **J1-69:** original Slot-5 motherboard-RAM-disable behavior is established prior project evidence. The revised PCB connects J1-69 to JP2-1 and JP2-2 to GND; **shunt is normally open**, with no permanent ground strap. **J1-82 remains NC** until independently understood.
2. Verify collisions and memory mapping against onboard 2101 RAM,
   Giant Board and any other memory devices.
3. Check 1802 TPA/address, /CS, /OE and /WE timing and bus contention on
   actual hardware.
4. Resolve intentional edge-finger DRC clearances with the fabricator's
   gold fingers, plating, bevel, PCB thickness and mating-socket specs.
5. Require full electrically matching PCB netlist, fully routed copper,
   no unexplained ERC/DRC issues, and physical/visual review prior to Gerbers.

## Reference and design documentation

- [Hyperboard RAM source trace](docs/design/hyperboard-ram-circuit-trace.md)
- [New electrical architecture](docs/design/hyperboard-ram-rebuild.md)
- [74LS151 input-margin review](docs/design/page-select-ttl-input-margin.md)
- [Early ELF II bus bench verification](docs/design/early-elfii-bus-bench-validation.md)
- [Card-edge CAM and fabrication hold](docs/design/card-edge-cam-manufacturing-review-2026-10-12.md)
- [Power feed and bypass copper measurements](docs/design/prefab-power-and-decoupling-measurements-2026-10-12.md)
- [KiCad project instructions](hardware/kicad/README.md)
- [Original ELF II period sources](docs/reference/source-notes.md)

## License

License selection pending. Original Netronics and AVI/Hyperboard drawings
are historical reference material, not presumed freely redistributable.
