#!/usr/bin/env python3
"""Validate the Hyperboard-derived ELF II SRAM schematic from a KiCad netlist.

These assertions are intentionally pin-specific.  They guard the source-traced
74HC573/CY62256/74LS151 architecture against accidental rewiring; they do not
replace KiCad ERC or bench timing/compatibility checks.
"""
import re
import sys
from pathlib import Path


def balanced_forms(source: str, expression: str):
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
    result = {}
    for net in balanced_forms(data, "net "):
        name_match = re.search(r'\(name "([^"]+)"\)', net)
        if not name_match:
            continue
        nodes = set(re.findall(r'\(node\s+\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)', net))
        result[name_match.group(1).lstrip("/")] = nodes
    if not result:
        raise ValueError("No KiCad nets found; netlist layout or format differs")
    return result


EXPECTED = {
    # Core controls
    "TPA": [("J1", "28"), ("U1", "11")],
    "~MRD": [("J1", "30"), ("U2", "22")],
    "~MWR": [("J1", "24"), ("U2", "27")],
    "RAM_CS_N": [("U3", "6"), ("U2", "20")],
    # 32K half select
    "A15": [("U1", "19"), ("U4", "12"), ("U4", "13"), ("JP1", "1")],
    "A15_N": [("U4", "11"), ("JP1", "3")],
    "HALF_EN": [("JP1", "2"), ("U3", "7")],
    # Optional motherboard-RAM disable -- never the SRAM /CS net
    "MB_RAM_DISABLE": [("J1", "69"), ("JP2", "1")],
}

# Direct low-byte address path and reversed high-byte capture into the 573.
latch_d_pin_for_ma = {7:"2", 6:"3", 5:"4", 4:"5", 3:"6", 2:"7", 1:"8", 0:"9"}
ram_addr_pin = {0:"10", 1:"9", 2:"8", 3:"7", 4:"6", 5:"5", 6:"4", 7:"3"}
edge_ma_pin = {7:"36", 6:"40", 5:"44", 4:"48", 3:"52", 2:"56", 1:"60", 0:"64"}
for bit in range(8):
    EXPECTED[f"MA{bit}"] = [
        ("J1", edge_ma_pin[bit]),
        ("U1", latch_d_pin_for_ma[bit]),
        ("U2", ram_addr_pin[bit]),
    ]

# Latched high-byte outputs. A15 is above; A14..A8 feed both RAM and page decode as applicable.
high = {
    "A14": [("U1","18"), ("U2","1"), ("U3","9")],
    "A13": [("U1","17"), ("U2","26"), ("U3","10")],
    "A12": [("U1","16"), ("U2","2"), ("U3","11")],
    "A11": [("U1","15"), ("U2","23")],
    "A10": [("U1","14"), ("U2","21")],
    "A9":  [("U1","13"), ("U2","24")],
    "A8":  [("U1","12"), ("U2","25")],
}
EXPECTED.update(high)

# Bidirectional data bus.
edge_d_pin = {7:"34", 6:"38", 5:"42", 4:"46", 3:"50", 2:"54", 1:"58", 0:"62"}
ram_d_pin = {0:"11", 1:"12", 2:"13", 3:"15", 4:"16", 5:"17", 6:"18", 7:"19"}
for bit in range(8):
    EXPECTED[f"D{bit}"] = [("J1", edge_d_pin[bit]), ("U2", ram_d_pin[bit])]

# Hyperboard page map: SW1 -> 22K pulldown -> 74LS151 I0..I7.
mux_i_pin = ["4","3","2","1","15","14","13","12"]
for page in range(8):
    EXPECTED[f"PAGE{page}"] = [
        ("SW1", str(16-page)),
        ("RN1", str(2+page)),
        ("U3", mux_i_pin[page]),
    ]

# Power and defined unused inputs.
EXPECTED["+5V"] = [
    ("J1","2"), ("J1","1"),
    ("U1","20"), ("U2","28"), ("U3","16"), ("U4","14"),
    *[("SW1", str(i)) for i in range(1,9)],
    *[(f"C{i}", "1") for i in range(1,6)],
]
EXPECTED["GND"] = [
    ("J1","80"), ("J1","5"),
    ("U1","1"), ("U1","10"), ("U2","14"), ("U3","8"), ("U4","7"),
    ("RN1","1"), ("JP2","2"),
    ("U4","1"), ("U4","2"), ("U4","5"), ("U4","6"), ("U4","8"), ("U4","9"),
    *[(f"C{i}", "2") for i in range(1,6)],
]


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

    # Explicitly guard the source correction: connector P3-69 must not land on SRAM /CS.
    cs_nodes = nets.get("RAM_CS_N", set())
    if ("J1", "69") in cs_nodes:
        errors.append("RAM_CS_N incorrectly contains J1-69; Hyperboard P3 RAM_CE is not SRAM /CS")

    if errors:
        # Show the actual net for each missing device pin, so an incorrect
        # connection can be distinguished from a truly unconnected pin.
        reverse = {}
        for net_name, pins in nets.items():
            for item in pins:
                reverse.setdefault(item, []).append(net_name)
        print(f"FAIL: {len(errors)} source pin-map violations")
        for signal, required in EXPECTED.items():
            actual = nets.get(signal, set())
            for item in required:
                if item not in actual:
                    print(f"  {signal}: {item} is on {reverse.get(item, ['<unconnected>'])}")
        raise SystemExit(f"FAIL: {len(errors)} source pin-map violations")
    count = sum(map(len, EXPECTED.values()))
    print(f"PASS: {count} required Hyperboard-derived pin/net memberships across {len(EXPECTED)} nets")


if __name__ == "__main__":
    main()
