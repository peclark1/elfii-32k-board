# A5 schematic and track cleanup

## Real design changes already committed to main
- Replaced 4,193 tiny PCB copper segments with 613 longer collinear runs, while retaining the same pad/net assignments and 36 plated vias. This is a geometric simplification, not new routing.
- Drew visible A15, MISMATCH and NOT_ENABLE connections between actual latch and decoder pins.
- Added native KiCad buses `MA[0..7]` beside U1 and `D[0..7]` beside U2, with 16 bus entries and physical electrical wire stubs to the relevant pins. Other bus net endpoints still use named net labels.
- Added a PCB track-quality regression test that accepts the original very short pad-to-grid lead-ins but rejects long non-orthogonal traces.

## Validation
KiCad 9 ERC, exported netlist pin-to-net checks, filled-zone PCB DRC and source-board import must all pass. The original connector remains unmodified.

## Remaining work
The source remains an intermediate prototype: ten signal nets and +5V distribution still unconnected, incomplete DRC, questionable custom footprint geometry and unverified bus/memory-map integration. It is not fabrication ready.
