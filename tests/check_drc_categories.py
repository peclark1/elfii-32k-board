#!/usr/bin/env python3
"""Fail CI on newly introduced KiCad PCB DRC errors, even while unrouted.

Approved *existing* classes are only card-edge finger clearance, provisional
footprint-library differences, and intentionally incomplete connections.
These are NOT fabrication approvals and still must be resolved.
"""
import re
import sys
from collections import Counter
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: check_drc_categories.py out/drc.txt")
data = Path(sys.argv[1]).read_text(encoding="utf-8")
if "Drc report" not in data:
    raise SystemExit("FAIL: KiCad DRC report missing or unreadable")
counts = Counter(re.findall(r'^\[([a-z][a-z0-9_]+)\]:', data, re.M))
allowed = {
    "copper_edge_clearance",
    "lib_footprint_mismatch",
    "unconnected_items",
}
unexpected = {kind: num for kind, num in counts.items() if kind not in allowed}
if unexpected:
    for kind, num in sorted(unexpected.items()):
        print(f"FAIL: new non-baseline PCB rule violation: {kind} ({num})")
    raise SystemExit(1)
if counts["copper_edge_clearance"] > 86:
    raise SystemExit(f"FAIL: connector-edge violations increased: {counts['copper_edge_clearance']}")
if counts["lib_footprint_mismatch"] > 14:
    raise SystemExit(f"FAIL: footprint mismatches increased: {counts['lib_footprint_mismatch']}")
if counts["unconnected_items"] > 25:
    raise SystemExit(f"FAIL: unrouted connections regressed: {counts['unconnected_items']}")
print(
    "PASS: no newly introduced short/crossing/mask/via/thermal DRC classes; "
    f"existing intentional/incomplete issues: {dict(counts)}"
)
print("NOT A FABRICATION PASS: edge clearances, footprint checks, and airwires remain.")
