#!/usr/bin/env python3
"""Regression checks for physical copper tracks in the current ELF II board.

This supplements (and never replaces) KiCad's real PCB DRC.
"""
from collections import Counter
from pathlib import Path
import re

board = Path("hardware/kicad/elfii-32k-board.kicad_pcb").read_text(encoding="utf-8")
segments = re.findall(
    r'\(segment \(start ([-\d.]+) ([-\d.]+)\) '
    r'\(end ([-\d.]+) ([-\d.]+)\) \(width ([-\d.]+)\) '
    r'\(layer "([^"]+)"\) \(net (\d+)\)',
    board,
)
vias = re.findall(r'\(via \(at [-\d.]+ [-\d.]+\)', board)
assert segments, "PCB has no copper tracks"
assert len(segments) <= 800, (
    f"PCB still has {len(segments)} tiny router segments; coalesce contiguous runs"
)
assert len(vias) <= 50, f"More than 50 vias in this routing checkpoint: {len(vias)}"
net_counts = Counter()
for x1, y1, x2, y2, width, layer, net in segments:
    assert (x1, y1) != (x2, y2), f"Zero-length copper track on {net}"
    assert layer in ("F.Cu", "B.Cu"), f"Unexpected copper layer {layer}"
    assert float(width) >= 0.254, f"Undersized track {width}"
    assert (x1 == x2) or (y1 == y2), (
        f"Non-orthogonal segment in current first-pass router on net {net}"
    )
    net_counts[net] += 1
print(f"PASS: {len(segments)} routed copper segments, {len(vias)} vias, "
      f"{len(net_counts)} nets with traces")
