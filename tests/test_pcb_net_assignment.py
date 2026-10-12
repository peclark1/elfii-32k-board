#!/usr/bin/env python3
"""Compare physical PCB pad net assignments with KiCad-exported schematic netlist.

This is a connectivity consistency check, NOT PCB DRC, impedance/timing analysis,
or a substitute for full independent schematic review.
"""
import re
import sys
from pathlib import Path
from test_netlist import read_nets, balanced_forms


def board_pads(path):
    data = Path(path).read_text(encoding="utf-8")
    assignments = {}
    for footprint in balanced_forms(data, "footprint "):
        match = re.search(
            r'\((?:fp_text\s+reference|property\s+"Reference")\s+"([^"]+)"',
            footprint,
        )
        if not match:
            continue
        ref = match.group(1)
        for pad in balanced_forms(footprint, "pad "):
            number_match = re.search(r'^\(pad "([^"]+)"', pad)
            if not number_match:
                continue
            key = (ref, number_match.group(1))
            net_match = re.search(r'\(net\s+\d+\s+"([^"]+)"\)', pad)
            net = net_match.group(1).lstrip("/") if net_match else None
            if key in assignments:
                raise ValueError(f"Duplicate PCB pad {key}")
            assignments[key] = net
    return assignments


def main():
    if len(sys.argv) not in (3, 4) or (
        len(sys.argv) == 4 and sys.argv[3] != "--candidate-contact-69-open"
    ):
        raise SystemExit(
            "usage: test_pcb_net_assignment.py export.net board.kicad_pcb "
            "[--candidate-contact-69-open]"
        )
    candidate_69_open = len(sys.argv) == 4
    expected = {}
    for name, nodes in read_nets(Path(sys.argv[1])).items():
        # KiCad invents pseudo-nets for intentionally unconnected symbol pins.
        # They have no physical copper net and must not be copied onto PCB pads.
        if name.startswith("unconnected-"):
            continue
        for node in nodes:
            # The user's ORIGINAL early-Netronics contact 69 is an explicit
            # unresolved safety exception on the exploratory PCB ONLY.
            # The schematic's optional JP2 circuit is not yet routed to it.
            if candidate_69_open and node == ("J1", "69"):
                continue
            if node in expected and expected[node] != name:
                raise ValueError(f"Schematic pin {node} on multiple nets")
            expected[node] = name

    actual = board_pads(Path(sys.argv[2]))
    if candidate_69_open and actual.get(("J1", "69")) is not None:
        raise SystemExit("FAIL: early Netronics J1 contact 69 must remain NC on candidate")

    missing = sorted((node, net) for node, net in expected.items() if actual.get(node) != net)
    unexpected = sorted((node, net) for node, net in actual.items() if net is not None and expected.get(node) != net)
    if missing or unexpected:
        for node, net in missing:
            print(f"MISSING or WRONG: {node} should be {net}, PCB has {actual.get(node)}")
        for node, net in unexpected:
            print(f"UNEXPECTED: {node} PCB net {net}, schematic net {expected.get(node)}")
        raise SystemExit(f"FAIL: {len(missing)} mismatches and {len(unexpected)} unexpected pad assignments")
    print(f"PASS: all {len(expected)} schematic-connected pins match PCB pad nets; {len(actual)} physical pads checked")
    if candidate_69_open:
        print("HOLD: J1 contact 69 intentionally NC despite optional JP2 in schematic; NOT RELEASED")


if __name__ == "__main__":
    main()
