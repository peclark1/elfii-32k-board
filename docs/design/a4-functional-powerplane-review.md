# Functional schematic and power distribution — validation

## Schematic Rev A4
- The 74HCT273 and 62256 symbol pin placements are now arranged by function while preserving their **actual physical DIP pin numbers**.
- A8 through A14 are drawn as short, visible three-segment wires from U1 outputs to U2 inputs.
- Long, unreadable cross-page wiring was removed.
- MA0-MA7 and D0-D7 retain explicit named bus nets. The next review should consider whether to draw KiCad buses and bus entries for these groups.
- The electrical netlist and ERC need to be rerun to confirm that moving symbols did not change any pin mapping.

## Two-layer power distribution
- F.Cu ground pour with solid pad connections.
- B.Cu +5 V pour with solid pad connections.
- The +5V front finger and GND back finger have short copper straps and plated vias joining the opposite-face supply plane.
- Finger copper geometry remains unchanged, including original known DRC exceptions.
- KiCad Python fills the zones for DRC in a temporary board file; source remains unfilled until editor refresh.

## Remaining incomplete work
Ten signal groups previously failed the router (D1,D2,D3,D5,MA1,MA2,MA3,MA5,MA6,MA7). Measure the actual unrouted count after zone filling; do not assume VCC and GND connected without KiCad DRC. Confirm any leftover starved fills or isolated islands. Simplified library footprints and edge-finger fabrication still need review. Hardware bank overlap and TPA timing are not settled. This is **not fabrication-ready**.
