#!/usr/bin/env python3
"""Physical copper regression on the routed Hyperboard-derived engineering preview.

Independent point-graph connectivity for J1-69, physically unsafe via placement
and zone/track constraints; this is NOT a replacement for filled KiCad DRC.
"""
from collections import defaultdict, deque
from pathlib import Path
import re
from test_pcb_net_assignment import board_pads

PCB = Path("hardware/kicad/elfii-32k-board.kicad_pcb")


def forms(src, token):
    search = re.compile(r"\(" + re.escape(token) + r"(?=\s)")
    pos = 0
    while (match := search.search(src, pos)):
        start = match.start()
        depth, quoted, escaped = 0, False, False
        for end in range(start, len(src)):
            c = src[end]
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
                    yield src[start:end + 1]
                    pos = end + 1
                    break
        else:
            raise ValueError(f"Unbalanced KiCad S-expression ({token})")


def point(form, keyword):
    m = re.search(r"\(" + keyword + r" ([\d.-]+) ([\d.-]+)\)", form)
    assert m, f"Missing {keyword} in {form[:80]}"
    return tuple(round(float(x), 4) for x in m.groups())


def run():
    src = PCB.read_text(encoding="utf-8")
    pads = board_pads(PCB)
    assert pads[("J1", "69")] == pads[("JP2", "1")] == "MB_RAM_DISABLE"
    assert pads[("JP2", "2")] == "GND"
    assert pads[("J1", "82")] is None
    assert "(thickness 1.6)" in src
    zones = list(forms(src, "zone"))
    assert len(zones) == 2, f"Expected two new GND pours, got {len(zones)}"
    assert {re.search(r'\(layer "([^"]+)"\)', z).group(1) for z in zones} == {"F.Cu", "B.Cu"}
    for z in zones:
        assert '(net_name "GND")' in z
        assert '(clearance 0.3)' in z
        points = re.findall(r"\(xy ([\d.-]+) ([\d.-]+)\)", z)
        assert points and max(float(y) for _, y in points) <= 141.5, "GND zone extends into finger tongue"

    segments = list(forms(src, "segment"))
    vias = list(forms(src, "via"))
    edges = defaultdict(set)
    thin = 0
    for seg in segments:
        a, b = point(seg, "start"), point(seg, "end")
        assert a != b, "Zero-length trace"
        width = float(re.search(r"\(width ([\d.]+)\)", seg).group(1))
        assert width >= 0.15, "Sub-0.15 mm trace"
        thin += width < 0.2
        assert re.search(r'\(layer "(F.Cu|B.Cu)"\)', seg)
        net = int(re.search(r"\(net (\d+)\)", seg).group(1))
        layer = re.search(r'\(layer "([^"]+)"\)', seg).group(1)
        if net == 28:
            edges[(a, layer)].add((b, layer))
            edges[(b, layer)].add((a, layer))
    for v in vias:
        at = point(v, "at")
        assert not (64.516 <= at[0] <= 176.022 and at[1] > 144.272), (
            f"Via inside exposed 86-finger insertion tongue: {at}"
        )
        assert "(size 0.6)" in v and "(drill 0.3)" in v
        if "(net 28)" in v:
            edges[(at, "F.Cu")].add((at, "B.Cu"))
            edges[(at, "B.Cu")].add((at, "F.Cu"))

    # Physical pad centers from the separately regression-locked J1 footprint
    # and the through-hole JP2 pin-1 origin.
    source = ((87.2236, 148.7424), "B.Cu")
    target = ((190.0, 103.0), "F.Cu")
    visited, queue = {source}, deque([source])
    while queue:
        current = queue.popleft()
        for neighbour in edges[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    assert target in visited, "J1-69 copper is not actually routed to JP2-1!"
    assert ((94.2318, 116.9313), "F.Cu") in visited, "J1-69 layer via not connected"
    assert any("(at 175.3 142.2793)" in v and "(net 26)" in v for v in vias)
    assert not any("(at 174.793 150.627)" in v for v in vias)
    print(f"PASS: {len(segments)} segments, {len(vias)} vias, two GND zones, edge via clear")
    print("PASS: J1-69 -> JP2-1 physical copper path; JP2-2 GND; J1-82 NC")
    print(f"REVIEW: {thin} signal/supply neckdown segments at 0.15 mm require final fab approval")


if __name__ == "__main__":
    run()
