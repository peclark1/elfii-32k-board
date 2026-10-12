#!/usr/bin/env python3
"""Verify actual Hyperboard-derived IC supplies, capacitor pads and zone ties.

Only C2-2 and U4-2 use selective solid GND zone connections to avoid
isolated islands / starved thermal spokes. Not an approval of solderability.
"""
from pathlib import Path
import re
from test_pcb_net_assignment import board_pads
from test_routed_board_review import forms

board = Path("hardware/kicad/elfii-32k-board.kicad_pcb")
contents = board.read_text()
nets = board_pads(board)
for ref, vcc, ground in (("U1", "20", "10"), ("U2", "28", "14"),
                         ("U3", "16", "8"), ("U4", "14", "7")):
    assert nets[(ref, vcc)] == "+5V", f"{ref} VCC not powered"
    assert nets[(ref, ground)] == "GND", f"{ref} not grounded"
for i in range(1, 6):
    assert nets[(f"C{i}", "1")] == "+5V", f"C{i} positive not powered"
    assert nets[(f"C{i}", "2")] == "GND", f"C{i} ground not connected"

zones = list(forms(contents, "zone"))
assert len(zones) == 2
for z in zones:
    assert '(net_name "GND")' in z
    assert '(island_removal_mode 0)' in z, "Isolated copper should be removed"

expected_overrides = {("C2", "2"), ("U4", "2")}
found = set()
for footprint in forms(contents, "footprint"):
    label = re.search(r'\(property "Reference" "([^"]+)"', footprint)
    if not label:
        continue
    ref = label.group(1)
    for pad in forms(footprint, "pad"):
        num = re.match(r'\(pad "([^"]+)"', pad)
        if num and '(zone_connect 2)' in pad:
            found.add((ref, num.group(1)))
# The two new overrides plus pre-existing J1-1 power pad are intentional.
assert expected_overrides <= found, f"Missing local GND zone pad ties: {expected_overrides - found}"
for seg in forms(contents, "segment"):
    if '(net 26)' in seg:
        width = float(re.search(r'\(width ([\d.]+)\)', seg).group(1))
        assert width >= 0.20, "Supply backbone contains <0.20 mm +5V neckdown"
print("PASS: U1-U4/C1-C5 power net pad assignments, two cleared-island GND zones")
print("PASS: targeted C2-2 and U4-2 solid GND tie overrides, +5V >= 0.20 mm")
