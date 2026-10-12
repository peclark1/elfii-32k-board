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
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: test_pcb_net_assignment.py export.net board.kicad_pcb"
        )

    expected = {}
    for name, nodes in read_nets(Path(sys.argv[1])).items():
        if name.startswith("unconnected-"):
            continue
        for node in nodes:
            if node in expected and expected[node] != name:
                raise ValueError(f"Schematic pin {node} on multiple nets")
            expected[node] = name

    actual = board_pads(Path(sys.argv[2]))
    # Slot-5 known-working Hyperboard behavior: J1-69 is an original RAM
    # inhibit input. It must reach JP2-1, not be directly grounded or NC.
    if expected.get(("J1", "69")) != "MB_RAM_DISABLE" or expected.get(("JP2", "1")) != "MB_RAM_DISABLE":
        raise SystemExit("FAIL: schematic J1-69 / JP2-1 must share MB_RAM_DISABLE")
    if actual.get(("J1", "69")) != "MB_RAM_DISABLE":
        raise SystemExit("FAIL: PCB J1-69 must be on MB_RAM_DISABLE, not open or GND")
    if actual.get(("JP2", "2")) != "GND":
        raise SystemExit("FAIL: PCB JP2-2 must connect to GND")
    if actual.get(("J1", "82")) is not None:
        raise SystemExit("FAIL: unverified J1-82 must remain NC")

    missing = sorted((node, net) for node, net in expected.items() if actual.get(node) != net)
    unexpected = sorted((node, net) for node, net in actual.items() if net is not None and expected.get(node) != net)
    if missing or unexpected:
        for node, net in missing:
            print(f"MISSING or WRONG: {node} should be {net}, PCB has {actual.get(node)}")
        for node, net in unexpected:
            print(f"UNEXPECTED: {node} PCB net {net}, schematic net {expected.get(node)}")
        raise SystemExit(f"FAIL: {len(missing)} mismatches and {len(unexpected)} unexpected pad assignments")
    print(f"PASS: all {len(expected)} schematic-connected pins match PCB pad nets; {len(actual)} physical pads checked")
    print("PASS: J1-69 -> JP2-1 is selectively shunted to GND via JP2-2; J1-82 remains NC")


if __name__ == "__main__":
    main()
