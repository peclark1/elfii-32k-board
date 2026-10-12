# A5d — restore solid power-zone attachments

The canonical footprint geometry conversion kept all 109 component pad positions and net numbers but initially dropped 12 per-pad `zone_connect 2` overrides. DRC then reported 3 starved thermals and 22 missing connections.

The 12 IC/capacitor overrides and existing J1 override have been restored on main, with a permanent 13-contact regression test. This run must confirm that KiCad 9 loads/zone-fills the physical PCB, there are no copper shorts or new clearance errors, and the starved thermal count falls back toward zero.

**This still leaves the ten named address/data signal nets unrouted.** Connector edge-finger fabrication constraints and final stock-footprint verification are separate blockers.
