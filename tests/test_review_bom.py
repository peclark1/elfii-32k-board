#!/usr/bin/env python3
"""Keep the manually curated assembly BOM synchronized with schematic instances."""
import csv
from pathlib import Path
import re

SCH = Path("hardware/kicad/elfii-32k-board.kicad_sch")
BOM = Path("hardware/bom/elfii-32k-prototype-bom.csv")

def expand(ref):
    if "-" not in ref:
        return [ref]
    a, b = ref.split("-", 1)
    x, y = re.fullmatch(r"([A-Z]+)([0-9]+)", a), re.fullmatch(r"([A-Z]+)([0-9]+)", b)
    assert x and y and x[1] == y[1] and int(x[2]) <= int(y[2]), ref
    return [f"{x[1]}{n}" for n in range(int(x[2]), int(y[2]) + 1)]

def main():
    instances = {}
    for section in SCH.read_text(encoding="utf-8").split("\n(symbol (lib_id ")[1:]:
        ref = re.search(r'\(property "Reference" "([^"]+)"', section)
        value = re.search(r'\(property "Value" "([^"]+)"', section)
        footprint = re.search(r'\(property "Footprint" "([^"]+)"', section)
        assert ref and value and footprint, "Incomplete schematic part instance"
        item = (value[1], footprint[1])
        if ref[1] in instances:
            assert instances[ref[1]] == item, "Mismatch across multi-unit symbol"
        instances[ref[1]] = item

    seen = set()
    rows = list(csv.DictReader(BOM.open(encoding="utf-8", newline="")))
    for row in rows:
        assert None not in row and None not in row.values(), f"Malformed CSV row: {row}"
        refs = expand(row["Reference"]) if row["Reference"] != "PCB" else []
        assert int(row["Quantity"]) == len(refs) or row["Reference"] == "PCB"
        for ref in refs:
            assert ref not in seen, f"Duplicate BOM component {ref}"
            seen.add(ref)
            assert ref in instances, f"Missing schematic ref {ref}"
            expected = instances[ref]
            got = (row["Value"], row["Footprint"])
            assert got == expected, (ref, got, expected)
    assert seen == set(instances), f"Parts missing/extraneous {set(instances) ^ seen}"
    assert "PCB" in {r["Reference"] for r in rows}
    assert instances["U3"][0] == "74HC151"
    print(f"PASS: assembly BOM matches {len(instances)} exact physical schematic refs")

if __name__ == "__main__":
    main()
