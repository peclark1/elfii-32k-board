# PCB routing safety regression and future edge-contact approach

A finer-grid A* path successfully connected J1-58 to U2-12 electrically, but **KiCad DRC rejected it**: the back-layer route interfered with unassigned 86-contact connector fingers and it introduced solder-mask bridges, copper shorts and close via clearance. Three trial GND straps also crossed existing tracks. These eight provisional copper items/groups were reverted from main in commit `c7754e2`; **do not count D1 as routed**.

The original grid routing model considered only pads having a net; that was inadequate for an 86-contact two-sided edge connector because unassigned fingers are still exposed metal. Any replacement routing algorithm must treat **all 86 connector pads**, even unassigned, as physical obstacles.

New `tests/check_drc_categories.py` is now a mandatory CI check after real KiCad 9 PCB DRC. It fails on new shorting, crossings, mask, starved thermals or clearance failures, while temporarily allowing only 86 inherited card-edge clearance reports, up to 14 reference-footprint library mismatches and up to 25 unrouted items.

The schematic with MA/D buses, real bypass power wiring and all 14 improved mechanical footprints is retained, as is the original verified 613-segment partial copper. The ten missing signal nets plus remaining ground connectivity still need genuine routing and independent hardware checks.

**No current board is fabrication ready.**
