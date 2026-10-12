#!/usr/bin/env python3
"""Guard copper zone syntax that previously made PCB unreadable by KiCad."""
from pathlib import Path
import re

board = Path("hardware/kicad/elfii-32k-board.kicad_pcb").read_text(encoding="utf-8")
zones = re.findall(r'\(connect_pads(?:\s+[^()]*)?\s*\(clearance\s+[\d.]+\)\)', board)
assert len(zones) == 2, f"Expected two copper zone connect_pads settings, found {len(zones)}"
for zone in zones:
    assert " full " not in zone, f"Invalid KiCad zone connect_pads value: {zone}"
print("PASS: both copper zones use accepted KiCad connect_pads syntax")
