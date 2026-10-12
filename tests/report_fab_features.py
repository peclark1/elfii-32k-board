#!/usr/bin/env python3
"""Extract numerical PCB manufacturing features for CAM review, NOT approval.

Use actual native .kicad_pcb copper/outline/footprints rather than
guessing limits from a selected PCB fabrication service's web page.
The historical connector geometry is deliberately preserved.
"""
from collections import Counter
from math import hypot
from pathlib import Path
import re
from test_routed_board_review import forms


BOARD = Path("hardware/kicad/elfii-32k-board.kicad_pcb")


def at(form, keyword):
    match = re.search(r"\(" + re.escape(keyword) + r" ([\d.-]+) ([\d.-]+)\)", form)
    if match is None:
        raise AssertionError(f"Cannot identify {keyword} in PCB feature")
    return (float(match.group(1)), float(match.group(2)))


def num(form, keyword):
    match = re.search(r"\(" + re.escape(keyword) + r" ([\d.-]+)\)", form)
    if match is None:
        raise AssertionError(f"Cannot identify {keyword} in PCB feature")
    return float(match.group(1))


def main():
    source = BOARD.read_text(encoding="utf-8")
    widths = Counter()
    lengths = Counter()
    max_lengths = {}
    for segment in forms(source, "segment"):
        w = num(segment, "width")
        a, b = at(segment, "start"), at(segment, "end")
        n = hypot(b[0]-a[0], b[1]-a[1])
        widths[w] += 1
        lengths[w] += n
        max_lengths[w] = max(max_lengths.get(w, 0), n)

    via_sizes = Counter()
    via_rings = []
    for via in forms(source, "via"):
        size, drill = num(via, "size"), num(via, "drill")
        via_sizes[(size, drill)] += 1
        via_rings.append((size - drill)/2)

    edge_segments = [
        line for line in forms(source, "gr_line")
        if '(layer "Edge.Cuts")' in line
    ]
    profile_y_max = max(
        y for line in edge_segments
        for y in (at(line, "start")[1], at(line, "end")[1])
    )
    profiles = list(forms(source, "footprint"))
    connector = [
        f for f in profiles if '(property "Reference" "J1"' in f
    ]
    assert len(connector) == 1, "Expected one original connector J1"
    j1 = connector[0]
    origin = at(j1, "at")
    fingers = []
    drill_rings = []
    drill_diameters = Counter()
    for footprint in profiles:
        for pad in forms(footprint, "pad"):
            pad_size = at(pad, "size")
            if "thru_hole" in pad.splitlines()[0]:
                match = re.search(r"\(drill ([\d.]+)\)", pad)
                if match:
                    drill = float(match.group(1))
                    drill_diameters[drill] += 1
                    drill_rings.append((min(pad_size) - drill) / 2)
            if footprint is j1:
                head = re.search(r'^\(pad "([^"]+)" smd rect', pad)
                if head is None:
                    continue
                layers = re.search(r"\(layers ([^)]+)\)", pad).group(1)
                face = "F.Cu" if '"F.Cu"' in layers else ("B.Cu" if '"B.Cu"' in layers else "OTHER")
                local = at(pad, "at")
                fingers.append((int(head.group(1)), face, origin[0]+local[0],
                                origin[1]+local[1], pad_size[0], pad_size[1]))
    assert len(fingers) == 86, f"Expected 86 edge contacts, got {len(fingers)}"
    assert Counter(x[1] for x in fingers) == {"F.Cu":43, "B.Cu":43}
    assert len(edge_segments) == 14
    pitch = sorted({round(x[2], 4) for x in fingers})
    min_pitch = min(pitch[i+1]-pitch[i] for i in range(len(pitch)-1))
    tip_y = max(x[3] + x[5]/2 for x in fingers)
    copper_setback = profile_y_max - tip_y
    print("Measured from native routed source board (not vendor approval)")
    print(f"Board profile: 14 outline segments; insertion edge Y={profile_y_max:.4f} mm")
    print(f"J1: {len(fingers)} fingers, 43 per copper face; pitch {min_pitch:.4f} mm")
    print(f"J1: {fingers[0][4]:.4f} x {fingers[0][5]:.4f} mm copper pads")
    print(f"J1: insertion-edge copper setback {copper_setback:.4f} mm")
    for width in sorted(widths):
        print(f"Traces {width:.3f} mm: {widths[width]} segments, "
              f"{lengths[width]:.2f} mm total, {max_lengths[width]:.2f} mm longest")
    for (size, drill), count in sorted(via_sizes.items()):
        print(f"Vias: {count} at {size:.3f}/{drill:.3f} mm diameter/drill, "
              f"nominal ring {(size-drill)/2:.3f} mm")
    if drill_rings:
        print(f"Smallest plated THT nominal radial ring {min(drill_rings):.3f} mm "
              f"(drilled diameter range {min(drill_diameters):.3f}–{max(drill_diameters):.3f} mm)")
    assert 0 < copper_setback < 0.2, "Historical connector copper setback unexpectedly changed"
    print("HOLD: J1 edge plating/bevel depth and connector wipe require fab CAM approval.")
    print("HOLD: Trace width/spacing, drill tolerances, copper weight and annular rings require fab approval.")
    print("HOLD: Approval to fabricate/install/merge is not implied by clean KiCad ERC/DRC.")


if __name__ == "__main__":
    main()
