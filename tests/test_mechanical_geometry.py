#!/usr/bin/env python3
"""Guard the original 86-finger copper and exact measured card outline.

KiCad 9 rewrites PCB S-expressions with multiline properties/geometry. Parse
both original and KiCad9-saved boards by complete S-expressions instead of
using fragile whitespace-dependent regexes. No fabrication approval implied.
"""
from hashlib import sha256
from pathlib import Path
import re
import sys

BOARD = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("hardware/kicad/elfii-32k-board.kicad_pcb")
OUTLINE_SHA256 = "f395f8a74e71894db1cd142bd78cfc542dd4f4d63e9f449eaeb58fd98ca8da19"
FINGER_SHA256 = "f9394fe5680a644c3366593a7f2f33651640ed1e015784241c8b26cfe838998e"


def balanced_forms(source, expression):
    """Extract whole KiCad S-expressions without stopping at nested parentheses."""
    pattern = "(" + expression
    out = []
    i = 0
    while (start := source.find(pattern, i)) != -1:
        depth, quoted, escaped = 0, False, False
        for j in range(start, len(source)):
            c = source[j]
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
                    out.append(source[start:j + 1])
                    i = j + 1
                    break
        else:
            raise ValueError(f"Unbalanced ({expression}")
    return out


def check():
    source = BOARD.read_text(encoding="utf-8")
    edge = []
    for form in balanced_forms(source, "gr_line"):
        if not re.search(r'\(layer\s+"Edge.Cuts"\)', form):
            continue
        pair = re.search(
            r'\(start\s+([\d.-]+)\s+([\d.-]+)\)\s*'
            r'\(end\s+([\d.-]+)\s+([\d.-]+)\)', form
        )
        if pair:
            edge.append(pair.groups())
    assert len(edge) == 14, f"Expected 14 measured outline segments; found {len(edge)}"
    outline = sorted(
        tuple(sorted(((float(x1), float(y1)), (float(x2), float(y2)))))
        for x1, y1, x2, y2 in edge
    )
    assert sha256(repr(outline).encode()).hexdigest() == OUTLINE_SHA256, (
        "Measured full-size PCB Edge.Cuts profile changed"
    )

    # New KiCad9 uses (property "Reference" "J1"); earlier board files used
    # (fp_text reference "J1"). Both must resolve to the same physical pads.
    j1 = [
        f for f in balanced_forms(source, "footprint ")
        if re.search(r'\((?:fp_text\s+reference|property\s+"Reference")\s+"J1"', f)
    ]
    assert len(j1) == 1, f"Expected one 86-finger connector; found {len(j1)}"
    foot = j1[0]
    assert re.search(r'\(at\s+66\.9036\s+148\.7424\)', foot), (
        "Measured connector origin/orientation moved"
    )
    fingers = []
    for pad in balanced_forms(foot, "pad "):
        number = re.search(r'^\(pad\s+"(\d+)"\s+smd\s+rect', pad)
        if not number:
            continue
        at = re.search(r'\(at\s+([\d.-]+)\s+([\d.-]+)\)', pad)
        size = re.search(r'\(size\s+([\d.-]+)\s+([\d.-]+)\)', pad)
        layers = re.search(r'\(layers\s+"([^"]+)"\s+"([^"]+)"\)', pad)
        assert at and size and layers, f"Unparseable finger {number.group(1)}"
        fingers.append(
            (int(number.group(1)),
             *(round(float(v), 4) for v in (*at.groups(), *size.groups())),
             *layers.groups())
        )
    assert len(fingers) == 86, f"Expected 86 copper fingers; found {len(fingers)}"
    fingers.sort()
    assert [f[0] for f in fingers] == list(range(1, 87))
    assert sha256(repr(fingers).encode()).hexdigest() == FINGER_SHA256, (
        "Gerber-derived finger numbering, layers, spacing or size changed"
    )
    print("PASS: 86 fingers and 14 measured outline segments unchanged")


if __name__ == "__main__":
    check()
