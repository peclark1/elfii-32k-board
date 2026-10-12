#!/usr/bin/env python3
"""Measure REAL routed +5V copper to each IC and its local bypass capacitor.

No schematic-only shortcuts: trace F.Cu/B.Cu segments, copper vias, and plated
through-hole pads. This does not model filled GND planes or dynamic impedance.
"""
from collections import defaultdict
from heapq import heappop, heappush
from math import cos, sin, radians, hypot, inf
from pathlib import Path
import re
from test_routed_board_review import forms

PCB = Path("hardware/kicad/elfii-32k-board.kicad_pcb")
EXPECTED = (
    ("C1", "U1", "20", 6.00),
    ("C2", "U2", "28", 6.50),
    ("C3", "U3", "16", 7.00),
    ("C4", "U4", "14", 13.00),
)
NET = "+5V"


def coords(text, keyword):
    match = re.search(r"\(" + keyword + r" ([\d.-]+) ([\d.-]+)\)", text)
    if not match:
        raise ValueError(f"Missing {keyword} coordinate")
    return tuple(round(float(v), 4) for v in match.groups())


def point_key(xy, layer):
    return (xy[0], xy[1], layer)


def add_edge(graph, a, b, length):
    graph[a].append((b, length))
    graph[b].append((a, length))


def collect_board(source):
    graph = defaultdict(list)
    pads = {}
    track_length, min_width, sections = 0.0, inf, 0
    for segment in forms(source, "segment"):
        net_match = re.search(r"\(net \d+\)", segment)
        # The KiCad source uses stable net ID 26, but verify the name in
        # the global net table to avoid quietly examining a different net.
        if not net_match or net_match.group() != "(net 26)":
            continue
        layer = re.search(r'\(layer "(F.Cu|B.Cu)"\)', segment).group(1)
        a, b = coords(segment, "start"), coords(segment, "end")
        width = float(re.search(r"\(width ([\d.]+)\)", segment).group(1))
        length = hypot(a[0] - b[0], a[1] - b[1])
        add_edge(graph, point_key(a, layer), point_key(b, layer), length)
        track_length += length
        min_width = min(min_width, width)
        sections += 1
    for via in forms(source, "via"):
        if "(net 26)" in via:
            at = coords(via, "at")
            add_edge(graph, point_key(at, "F.Cu"), point_key(at, "B.Cu"), 0.0)

    for footprint in forms(source, "footprint"):
        ref_match = re.search(r'\(property "Reference" "([^"]+)"', footprint)
        if not ref_match:
            continue
        ref = ref_match.group(1)
        origin = re.search(r"\(at ([\d.-]+) ([\d.-]+)(?: ([\d.-]+))?\)", footprint)
        fx, fy, theta = float(origin[1]), float(origin[2]), radians(float(origin[3] or 0))
        for pad in forms(footprint, "pad"):
            if not re.search(r'\(net 26 "\+5V"\)', pad):
                continue
            pin = re.search(r'^\(pad "([^"]+)"', pad).group(1)
            px, py = coords(pad, "at")
            # KiCad Y increases downward, hence clockwise local rotation.
            location = (round(fx + px*cos(theta) + py*sin(theta), 4),
                        round(fy - px*sin(theta) + py*cos(theta), 4))
            plated = bool(re.match(r'^\(pad "[^"]+" thru_hole', pad))
            layer = "B.Cu" if '(layers "B.Cu" "B.Mask")' in pad else "F.Cu"
            if plated:
                add_edge(graph, point_key(location, "F.Cu"),
                         point_key(location, "B.Cu"), 0.0)
            key = (ref, pin)
            if key in pads:
                raise AssertionError(f"Duplicate physical pad {key}")
            pads[key] = point_key(location, layer)

    return graph, pads, track_length, min_width, sections


def distance(graph, source, target):
    queue = [(0.0, source)]
    seen = set()
    while queue:
        d, node = heappop(queue)
        if node in seen:
            continue
        if node == target:
            return d
        seen.add(node)
        for neighbour, length in graph[node]:
            if neighbour not in seen:
                heappush(queue, (d + length, neighbour))
    return inf


def main():
    source = PCB.read_text(encoding="utf-8")
    assert re.search(r'\(net 26 "\+5V"\)', source), "Unexpected +5V net ID"
    graph, pads, total_mm, min_width, count = collect_board(source)
    assert count == 34, f"+5V track count changed: {count}; review power distribution"
    assert min_width >= 0.20, f"Supply track neckdown to {min_width} mm"
    assert 235 < total_mm < 245, f"Unexpected +5V total routed length: {total_mm:.2f} mm"

    front = pads[("J1", "2")]
    back = pads[("J1", "1")]
    assert front[-1] == "F.Cu" and back[-1] == "B.Cu"
    link = distance(graph, front, back)
    assert link < 20, "The two +5V connector faces are not physically joined"
    print(f"PASS: +5V {count} segments, {total_mm:.1f} mm overall, "
          f"minimum {min_width:.2f} mm, J1-1/J1-2 link {link:.1f} mm")
    for cap, ic, vcc_pin, maximum in EXPECTED:
        to_cap = distance(graph, front, pads[(cap, "1")])
        to_ic = distance(graph, front, pads[(ic, vcc_pin)])
        local = distance(graph, pads[(cap, "1")], pads[(ic, vcc_pin)])
        assert to_cap < 200 and to_ic < 200, f"+5V not copper-routed to {cap}/{ic}"
        assert local <= maximum, (
            f"{cap} to {ic} VCC routed path {local:.2f} mm exceeds "
            f"{maximum:.2f} mm review threshold"
        )
        print(f"PASS: {cap} to {ic} VCC={local:.2f} mm copper; "
              f"J1-2 to {ic} VCC={to_ic:.1f} mm")
    assert distance(graph, front, pads[("C5", "1")]) < 200, "C5 bulk input path disconnected"
    print("REVIEW: GND-return loop inductance, actual IC current and copper weight "
          "remain physical/manufacturing checks; no fabrication approval.")


if __name__ == "__main__":
    main()
