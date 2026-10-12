#!/usr/bin/env python3
"""Validate expected ELF II SRAM schematic connections from KiCad-exported netlist.

This is an independent pin/net assertion set, NOT a replacement for electrical
rule checking, analog/timing verification, or physical board validation.
"""
import re
import sys
from pathlib import Path


def balanced_forms(source: str, expression: str):
    """Return parenthesized top-level expressions with the given initial tag."""
    out = []
    pattern = "(" + expression
    start = 0
    while (start := source.find(pattern, start)) != -1:
        depth = 0
        in_string = False
        escaped = False
        for i in range(start, len(source)):
            c = source[i]
            if in_string:
                if escaped:
                    escaped = False
                elif c == "\\":
                    escaped = True
                elif c == '"':
                    in_string = False
            elif c == '"':
                in_string = True
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    out.append(source[start : i + 1])
                    start = i + 1
                    break
        else:
            raise ValueError(f"Unbalanced ({expression} expression")
    return out


def read_nets(path: Path):
    data = path.read_text(encoding="utf-8")
    # KiCad legacy-export style: nets list of (net (code "...") (name "...")
    # and (node (ref "U1") (pin "3")) entries.
    result = {}
    for net in balanced_forms(data, "net "):
        name_match = re.search(r'\(name "([^"]+)"\)', net)
        if not name_match:
            continue
        nodes = set(re.findall(r'\(node\s+\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)', net))
        result[name_match.group(1)] = nodes
    if not result:
        raise ValueError("No KiCad nets found; netlist layout or format differs")
    return result


EXPECTED = {
    "VCC": [("U1", "1"), ("U1", "20"), ("U2", "28"), ("U3", "14"), ("U4", "14"), ("U5", "14")],
    "GND": [("U1", "10"), ("U2", "14"), ("U3", "7"), ("U4", "7"), ("U5", "7")],
    "TPA": [("J1", "28"), ("U3", "1")],
    "LATCH_CLK": [("U3", "2"), ("U1", "11")],
    "A15": [("U1", "19"), ("U4", "1")],
    "REGION": [("JP1", "2"), ("U4", "2"), ("R2", "1")],
    "ENABLE": [("JP2", "1"), ("U3", "3"), ("R1", "1")],
    "NOT_ENABLE": [("U3", "4"), ("U5", "2")],
    "MISMATCH": [("U4", "3"), ("U5", "1")],
    "NCE": [("U5", "3"), ("U2", "20"), ("U5", "4"), ("U5", "9")],
    "NOE": [("U5", "6"), ("U2", "22")],
    "NWE": [("U5", "8"), ("U2", "27")],
    "NMRD": [("J1", "30"), ("U5", "5")],
    "NMWR": [("J1", "24"), ("U5", "10")],
}
for index in range(8):
    EXPECTED[f"MA{index}"] = [
        ("J1", str(64 - index * 4)),
        ("U1", str([3, 4, 7, 8, 13, 14, 17, 18][index])),
        ("U2", str([10, 9, 8, 7, 6, 5, 4, 3][index])),
    ]
    EXPECTED[f"D{index}"] = [("J1", str(62 - index * 4)), ("U2", str([11, 12, 13, 15, 16, 17, 18, 19][index]))]
for index, (latch, ram) in enumerate(zip([2, 5, 6, 9, 12, 15, 16], [25, 24, 21, 23, 2, 26, 1]), start=8):
    EXPECTED[f"A{index}"] = [("U1", str(latch)), ("U2", str(ram))]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: test_netlist.py path/to/exported.net")
    nets = read_nets(Path(sys.argv[1]))
    errors = []
    for signal, expected in EXPECTED.items():
        actual = nets.get(signal, set())
        for item in expected:
            if item not in actual:
                errors.append(f"{signal} missing {item}; actual={sorted(actual)}")
    if errors:
        print("\n".join(errors))
        raise SystemExit(f"FAIL: {len(errors)} missing expected connections")
    print(f"PASS: {sum(map(len, EXPECTED.values()))} required pin/net memberships across {len(EXPECTED)} nets")


if __name__ == "__main__":
    main()
