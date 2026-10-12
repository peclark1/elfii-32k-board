# A5 route cleanup — verification checkpoint

- Physically unchanged copper geometry was consolidated from **4,193** to **613** longer orthogonal KiCad tracks (3,580 redundant joints removed) without moving pads or vias.
- Original 36 vias and two GND zones retained.
- Three explicit active decode connections were drawn in the schematic: A15 → XOR select gate; XOR MISMATCH → OR select gate; inverted ENABLE → OR select gate. Other control fanouts still use labeled nets.
- `tests/test_track_quality.py` enforces routing segment consolidation to prevent regression.
- Automated KiCad 9 schematic ERC, pin/net test, source PCB load, filled-zone DRC and Gerber export must pass before any further routing.

## Incomplete
Ten named signal nets and +5 V power distribution remain open; the PCB is not ready for fabrication. Footprints need canonical replacements and card-edge manufacturing rules need a physical review.
