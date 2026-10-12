#!/usr/bin/env python3
"""Guard the real Hyperboard-derived 86-finger edge and full-size outline.

The electrical schematic/old PCB can be regenerated independently. This test
ensures an electrical redesign cannot quietly change the copper finger shapes
or the measured mechanical profile. It does NOT approve finger bevel/plating,
solder-mask details, mating-clearance or early-Netronics pin compatibility.
"""
from hashlib import sha256
from pathlib import Path
import re
import sys

BOARD = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("hardware/kicad/elfii-32k-board.kicad_pcb")
OUTLINE_SHA256 = "f395f8a74e71894db1cd142bd78cfc542dd4f4d63e9f449eaeb58fd98ca8da19"
FINGER_SHA256 = "f9394fe5680a644c3366593a7f2f33651640ed1e015784241c8b26cfe838998e"


def check():
    source = BOARD.read_text(encoding="utf-8")
    edge = re.findall(
        r'\(gr_line \(start ([\d.-]+) ([\d.-]+)\) '
        r'\(end ([\d.-]+) ([\d.-]+)\) .*?\(layer "Edge.Cuts"\)',
        source,
    )
    assert len(edge) == 14, f"Expected 14 measured outline segments; found {len(edge)}"
    outline = sorted(
        tuple(sorted(((float(x1), float(y1)), (float(x2), float(y2)))))
        for x1, y1, x2, y2 in edge
    )
    assert sha256(repr(outline).encode()).hexdigest() == OUTLINE_SHA256, (
        "Measured full-size PCB Edge.Cuts profile changed"
    )

    name = '(footprint "ELFII_Expansion:ELFII_Edge_86_Rev2_Unverified"'
    assert source.count(name) == 1, "Original 86-finger footprint missing/duplicated"
    foot = source[source.index(name):]
    # Connector is the first footprint on the original board.
    next_start = foot.find('(footprint "', len(name))
    if next_start >= 0:
        foot = foot[:next_start]
    assert '(at 66.9036 148.7424)' in foot, (
        "Measured connector origin/orientation moved"
    )
    pads = re.findall(
        r'\(pad "(\d+)" smd rect \(at ([\d.-]+) ([\d.-]+)\) '
        r'\(size ([\d.-]+) ([\d.-]+)\) '
        r'\(layers "([^"]+)" "([^"]+)"\)',
        foot,
    )
    assert len(pads) == 86, f"Expected 86 copper fingers; found {len(pads)}"
    fingers = sorted(
        (int(n), round(float(x), 4), round(float(y), 4),
         round(float(w), 4), round(float(h), 4), copper, mask)
        for n, x, y, w, h, copper, mask in pads
    )
    assert [x[0] for x in fingers] == list(range(1, 87))
    assert sha256(repr(fingers).encode()).hexdigest() == FINGER_SHA256, (
        "Original Gerber-derived finger numbering, layers, spacing or size changed"
    )
    print("PASS: 86 fingers and 14 measured outline segments unchanged")


if __name__ == "__main__":
    check()
