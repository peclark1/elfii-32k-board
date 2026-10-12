# A5e — ground strap routing

After the solid-pad power fixes and canonical footprint insertion, actual KiCad9 DRC reported **20 unconnected items** (16 address/data and 4 GND), 86 intentional edge-finger clearance findings and 14 KiCad9 footprint-library mismatches.

Three explicit F.Cu ground tracks were added on main:
- J1 front contact 80 (74.5236, 148.7424) to interior GND pour (74.5236, 140.335), 0.4 mm.
- C5 GND pin 2 (145.5,95.76) to SRAM U2 GND pin14 (145.38,88.51), 0.3 mm.
- U5 spare-gate grounded input pins 12 (135.81,108.46) to 13 (135.81,105.92), 0.3 mm.

Static copper clearance checks showed no nearby foreign track, plated via, or copper pad within 0.55 mm edge-to-edge on these segments. The KiCad9 DRC must independently confirm these clearances and whether the remaining GND zone-island finding disappears.

The PCB remains incomplete and must not be manufactured.
