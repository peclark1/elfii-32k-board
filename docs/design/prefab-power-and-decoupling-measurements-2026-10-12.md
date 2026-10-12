# 32K SRAM card — measured power routing and decoupling review
Date: 2026-10-12  
Scope: `feature/hyperboard-pcb-prefab-review`; not manufacturing approval.

## Method and limits

These are measurements of the **current physical KiCad PCB**, not inferred
schematic connections: each F.Cu/B.Cu +5V track segment, the plated supply via
and plated through-hole pad transitions form a weighted connectivity graph.
Paths use actual segment lengths in millimeters. `tests/test_power_distribution.py`
regresses the connector-to-IC and capacitor-to-IC power feeds in independent CI.

Separately, KiCad 9 fills both GND planes in a **temporary copy** and checks
the actual filled copper with project-local full-board DRC; these zones are
not included in the +5V graph. DRC connectivity does not measure high-frequency
GND return impedance, ringing, dynamic voltage droop or effective bypass
inductance. No bench measurements or physical card-cage checks have been done.

## Physical +5V routing

- 34 segments, **239.58 mm total**, all **0.20 mm** wide, with one
  0.60 mm / 0.30 mm plated supply via at (175.3, 142.2793).
- The upper-IC supply spine includes a straight 39.099 mm 0.20 mm section.
  There are **no remaining 0.15 mm +5V segments**.
- Supply is copper-continuous from front finger **J1-2** to back finger
  **J1-1** over an approximately **14.3 mm** routed path, and from
  J1-2 to each IC power pin and capacitor positive pad.
- Shortest power routes from J1-2 to IC VCC:
  
  | IC supply | Copper route length |
  | --- | ---: |
  | U1-20 | 153.2 mm |
  | U2-28 | 104.2 mm |
  | U3-16 | 124.8 mm |
  | U4-14 | 151.1 mm |
  | C5-1 bulk power feed | 180.2 mm |

A simple, **illustrative worst-case** DC-resistance calculation (uniform
35 µm copper, 0.20 mm track, copper resistivity 0.0172 ohm-mm²/m at 20 °C)
gives about 0.37 ohm for a 153 mm route and 0.44 ohm for 180 mm. These
are *not* measured board impedances, and actual shared-branch current,
via/contact resistance, plating and copper weight matter. At 100 mA along
one entire 153 mm track the illustrative drop would be ~37 mV, not
an assurance of supply integrity. The long, narrow supply routing
therefore **remains a supply current/voltage/transient review hold** pending
device-current budget and operating scope measurements.

## Local 100 nF decoupler feed geometry

| Capacitor | IC VCC | Actual +5V copper path | Physical assessment |
| --- | --- | ---: | --- |
| C1-1 | U1-20 (74HC573) | 5.38 mm, 1 F.Cu segment | Compact supply leg |
| C2-1 | U2-28 (CY62256) | 5.76 mm, 1 F.Cu segment | Compact supply leg |
| C3-1 | U3-16 (74HC151) | 6.38 mm, 1 F.Cu segment | Compact supply leg |
| C4-1 | U4-14 (CD4011) | 12.06 mm, 4 graph edges, via THT pad transitions | Longest/least favorable local bypass feed |

C4's power feed passes along **B.Cu** between its plated pad and U4's
plated VCC pin, returning to F.Cu through the pads. The direct pad-center
separation is 11.64 mm; the actual routed copper is 12.06 mm.

The IC ground pins are on other package corners, and the effective return
paths pass through filled GND copper and other ground connections. These
numbers are **only the positive half of the bypass loop**, so they cannot
establish total loop inductance. C4/U4 is a candidate for tighter bypass
placement or additional local decoupling **if subsequent signal/power
measurements justify a copper change**. Retain the validated routing until
there is a concrete design requirement rather than moving a capacitor
blindly and invalidating the finished route.

C5 is bulk decoupling/storage, **not** a substitute for C1–C4.

## Ground-return and physical copper checkpoint

- Two native GND fills, F.Cu and B.Cu; both stop at Y=141.5 mm, short
  of the exposed connector-finger tongue. Disconnected islands are removed.
- **C2-2 and U4-2** have selective solid-pad GND connections to avoid
  isolated copper and insufficient thermal spokes; the full filled-board
  KiCad 9 DRC is mandatory, not optional.
- There remain **51 explicit 0.20 mm GND tracks**, ~401.05 mm total,
  before adding the two filled ground regions. The ground fills reduce
  impedance in principle but do not by themselves prove a good transient
  return route or manual solderability of solid copper connections.
- Full board: **437 copper segments and 35 plated vias**. Following the
  width-only engineering improvement at commit `cea7e443`, **402 segments
  are 0.20 mm and 35 remaining signal segments are 0.15 mm** (42.94 mm
  total, none longer than 4.82 mm). Confirm fabricator minimum width/space,
  copper weight and annular rings before manufacturing approval.
- The historical 86-contact, 2.54 mm-pitch, two-sided connector and exact
  original outline remain unchanged. The moved supply via is above the
  finger tongue at Y=142.2793, not in the exposed insertion interval.
  J1-69 connects only to normally-open JP2-1; JP2-2 is GND;
  J1-82 remains NC.

## Release decisions still required

1. Establish actual SRAM/logic current budget and check power/ground
   droop and switching behavior on test hardware before installation.
2. Decide with a PCB manufacturer whether 0.15 mm signal routing,
   0.20 mm supplies and the 0.60/0.30 mm vias meet the chosen process.
3. Verify plated card-edge geometry, selective hard-gold finish or
   approved alternative, 1.6 mm thickness tolerance, bevel, and mask
   specifications. The historical copper ends ~0.10 mm shy of the edge.
4. Bench-verify original 1802 timing, motherboard 2101/Giant Board memory
   coexistence, and unverified J1-82 before connecting the board.
5. Confirm real socket/component clearances and thermal/solderability
   at the two solid GND pads.

**Release status: routed engineering checkpoint, not approved to make, order,
merge, or install.** See the independent full-board KiCad 9 filled-copper
workflow, not only the unrouted placement-candidate report.


## Independent filled-copper SVG visual inspection

The independent KiCad CI artifact `elfii-prefab-review-evidence`
contains SVGs rendered from the actual **zone-filled PCB** for
F.Cu, B.Cu, F.SilkS, and Edge.Cuts (review sample: successful run
38276341833). Inspection found:

- Both ground-filled faces cover the main board body but intentionally
  stop just above the row of exposed connector fingers; there is no
  flooded copper over the insertion tongue.
- The front face has an extensive GND region surrounding the upper
  IC/data traces. Long parallel data/address breakout paths create
  several local voids without a DRC connectivity violation.
- The back face contains **long narrow interruptions/channels** in its
  ground fill as signals fan out from the edge connector to the ICs.
  Native DRC reports zero unconnected pads and no short/clearance
  violations, but visual continuity alone does not establish
  low-inductance return geometry. Check this with real switching
  waveforms before changing copper.
- F.SilkS remains plainly marked **“PINOUT UNVERIFIED – DO NOT FAB”**,
  preserving the manufacturing safety hold.
- The review views are not sufficient to validate installed card-cage
  clearance, component height, edge bevel, hard-gold plating or solder
  behavior at the two selective solid GND pad ties.

The SVG inspection **found no additional demonstrated KiCad electrical
defect requiring rerouting**. Do not infer that an all-green native
DRC implies signal integrity, manufacturing authorization or safe
installation.

## Additional card-edge manufacturability finding

The historic edge-finger copper ends just **0.1016 mm** from the insertion
edge. Supplier bevel guidance may require a substantially larger setback;
this is an **unresolved CAM compatibility issue**, not permission to modify
J1. See [connector fabrication questions](card-edge-cam-manufacturing-review-2026-10-12.md).
