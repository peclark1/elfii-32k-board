#!/usr/bin/env python3
"""Protect documented solid power/ground pad connections across footprint updates."""
import re
from pathlib import Path

board = Path("hardware/kicad/elfii-32k-board.kicad_pcb").read_text(encoding="utf-8")
expected = {
    "J1": {"1"},
    "U1": {"10", "20"},
    "U2": {"14"},
    "U3": {"5", "7", "9"},
    "U4": {"5", "14"},
    "U5": {"7"},
    "C3": {"1"},
    "C4": {"1", "2"},
}

# Footprint blocks have no nested footprint children; locating the reference
# within the block allows pin-number checks without assumptions about order.
matches = list(re.finditer(r'\(footprint "', board))
for i, m in enumerate(matches):
    block = board[m.start():matches[i + 1].start() if i + 1 < len(matches) else len(board)]
    ref = re.search(r'\(fp_text reference "([^"]+)"', block)
    if not ref or ref.group(1) not in expected:
        continue
    pins = expected.pop(ref.group(1))
    for number in pins:
        match = re.search(r'^\s*\(pad "' + re.escape(number) + r'" [^\n]*$', block, re.M)
        assert match, f"Missing {ref.group(1)}:{number}"
        line = match.group()
        assert "(zone_connect 2)" in line, f"Lost solid zone connection on {ref.group(1)}:{number}"
        assert re.search(r'\(net \d+ "/(?:VCC|GND)"\)', line), f"Solid zone pad is not a power net: {ref.group(1)}:{number}"
assert not expected, f"Expected footprint(s) missing: {sorted(expected)}"
print("PASS: all 13 verified power-contact zone overrides preserved")
