#!/usr/bin/env python3
"""Ensure authored schematic placements and all wire ends stay on KiCad 50mil grid."""
import re
from pathlib import Path

GRID_MM = 1.27
s = Path("hardware/kicad/elfii-32k-board.kicad_sch").read_text()
start = s.index("(lib_symbols")
depth = 0
quoted = False
escaped = False
end = None
for i in range(start, len(s)):
    c = s[i]
    if quoted:
        if escaped:
            escaped = False
        elif c == "\\":
            escaped = True
        elif c == '"':
            quoted = False
    elif c == '"':
        quoted = True
    elif c == "(":
        depth += 1
    elif c == ")":
        depth -= 1
        if depth == 0:
            end = i + 1
            break
assert end is not None

# Library symbol graphics live in local coordinate systems and need not be
# snapped here; schematic *instances*, wires, no-connects and labels do.
body = s[end:]
bad = []
count = 0
for match in re.finditer(r"\((?:at|xy) (-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", body):
    for text in match.groups():
        value = float(text)
        count += 1
        if abs(value / GRID_MM - round(value / GRID_MM)) > 1e-4:
            bad.append((match.group(0), text))
if bad:
    print(*bad[:50], sep="\n")
    raise SystemExit(f"FAIL: {len(bad)} schematic coordinates off {GRID_MM}mm grid")
print(f"PASS: {count} schematic x/y coordinates on {GRID_MM}mm grid")
