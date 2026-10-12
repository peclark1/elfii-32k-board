# Current working state — ELF II 32K board

## Verified progress

- The A4 schematic groups 74HCT273/62256 pins by function and includes seven direct, visible A8-A14 latch-to-SRAM wires. The MA0-MA7/D0-D7 connections and most control/power hookups still use named net labels. KiCad exported pin/net tests passed once the missing LATCH_CLK label was restored.
- The PCB has **4,193 real copper track segments** and **36 plated vias** connecting 25 signal nets on two layers. KiCad DRC on this first routing checkpoint, using 0.6mm/0.3mm vias, reported **zero track/via clearance violations**, with 56 remaining unconnected items before zones.
- The F.Cu and B.Cu PCB GND zones are retained with solid pad connection settings. An earlier zone-filled test (before solid pad conversion) reduced 56 missing connections to 33; the current source must be zone-filled and retested.
- The original board outline and physical 86-contact connector are retained. Pins 69 and 82 remain unconnected pending original motherboard verification.
- Schema ERC was clean (0 errors / 0 warnings) before the A4 functional redraw; A4 regression pin-net tests pass but a fresh complete ERC is still required on the current exact commit.

## Failed experiment deliberately rolled back

A trial F.Cu GND/B.Cu +5V split plane with connector power straps was committed briefly, but KiCad 9 could not load the resulting PCB file. **The source board on main was restored to the previous two-GND-zone, partially routed checkpoint** in commit `2610becf`. Therefore no completed +5V plane should be claimed. Power remains unrouted.

The diagnostic PRs #14 and #15, which targeted this abandoned experiment, were closed rather than merged.

## Not completed

- Ten signal nets: D1, D2, D3, D5 and MA1, MA2, MA3, MA5, MA6, MA7.
- +5V connections; KiCad review/physical fit of the ground zones.
- Original 2101 motherboard memory conflict and Giant Board ROM/RAM map.
- Original bus contact 69 electrical behavior and latch/TPA timing on actual hardware.
- 86 intentional edge-finger clearance findings, 14 simplified-footprint library mismatches, remaining unconnected items.
- PCB routing, all-rule DRC, finished visual schematic review and fabrication authorization.

**Do not manufacture or install until these checks and all remaining copper are completed.**

## Next implementation pass

Route remaining ten nets in the GUI or a DRC-aware router instead of assuming a coarse-grid autorouter will converge. Replace the 14 simplified footprint drawings with actual KiCad library footprints. Add a complete and verified +5V supply/ground return; fill zones and verify DRC. Use the schematic netlist regression and KiCad9 ERC as mandatory requirements before any fab output.
