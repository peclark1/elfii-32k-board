# PCB route/via spacing correction — first-pass DRC

KiCad 9 DRC baseline after first 25-signal-net routing:
- 151 DRC findings / 56 unconnected items.
- 86 intentional edge-connector-finger clearances carried forward.
- 14 baseline simplified-footprint library mismatches.
- **51 new copper track/via clearance violations** at nominal 0.108 mm where at least 0.200 mm is required.

Cause: 0.8 mm diameter via adjacent to 0.254 mm track at a centre spacing of 0.635 mm leaves only 0.108 mm clearance.

First corrective action on main: shrink the **36 placed vias** to 0.6 mm diameter with 0.3 mm drill, yielding 0.208 mm nominal adjacent track clearance at the routing grid. Verify this is supported by the intended PCB fabricator and yields an acceptable finished annular ring; KiCad DRC is required to confirm before proceeding.

**This adjustment is provisional.** Even if the via clearance check passes, the board remains incomplete (56 unrouted items), with unresolved finger-edge rules and simplified footprints, and requires board-current capacity/voltage/timing validation before manufacture.
