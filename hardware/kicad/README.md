# ELF II 32K SRAM KiCad — Hyperboard-derived review

**Review branch only:** `feature/hyperboard-pcb-prefab-review`.
**Do not fabricate, install, or replace main's authoritative PCB.**

The schematic follows the AVI Hyperboard Rev 2 RAM path (U1 74HC573,
U2 CY62256, U3 74HC151, U4 CD4011). The source PCB on this feature
branch is the **physically routed Hyperboard-derived revision**, not
the obsolete A5 netlist and routing study still preserved on main.

The `SCHEMATIC_REBUILD_IN_PROGRESS` marker intentionally remains.
The dedicated `prefabrication-review.yml` workflow **always** checks
the fully routed preview, regardless of this marker, using original
mechanical regression, source netlist/ERC, netlist-to-PCB pad matching,
insertion-area via screening, full copper connectivity and filled
native KiCad 9 DRC in the actual local footprint-library directory.

The accepted revision connects J1-69 to JP2-1; JP2-2 goes to GND.
Closing the removable shunt invokes the **previously established
Slot-5 motherboard-RAM-disable** function. The shunt is normally open.
J1-82 remains unconnected pending independent verification.

The physical review adds two GND zones kept behind the edge-finger
tongue and moves a +5V via out of the bevel/finger region. Long narrow
power routing and copper neckdowns, decoupling loops, physical
connector height/fit, ground-zone effectiveness, early-ELF timing,
memory coexistence and manufacturer-approved hard-gold/edge bevel
remain open.

See `docs/design/prefabrication-layout-review-2026-10-12.md` for
measured routing facts and release holds.
