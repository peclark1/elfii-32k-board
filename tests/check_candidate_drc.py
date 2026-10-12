#!/usr/bin/env python3
"""Reject new candidate PCB geometry/electrical DRC classes.

This guard deliberately permits the historic J1 edge-finger clearance rules,
the project-local footprint-library warning, and expected unrouted airwires.
It does NOT make the candidate fabrication-ready: those remaining items must
be cleared or approved explicitly with the intended manufacturer.
"""
import re
import sys
from collections import Counter
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: check_candidate_drc.py output/drc-unrouted.txt")
text = Path(sys.argv[1]).read_text(encoding="utf-8")
if not re.search(r'\*\* Found \d+ DRC violations \*\*', text):
    raise SystemExit("FAIL: missing real KiCad9 DRC summary")
issues = re.split(r'(?=^\[[a-z][a-z0-9_]+\]:)', text, flags=re.M)
problems = {}
counts = Counter()
for issue in issues:
    match = re.match(r'^\[([a-z][a-z0-9_]+)\]:', issue)
    if not match:
        continue
    kind = match.group(1)
    counts[kind] += 1
    if kind in ("copper_edge_clearance", "unconnected_items", "lib_footprint_issues"):
        if kind == "copper_edge_clearance" and "of J1 " not in issue:
            problems.setdefault(kind, []).append("Edge clearance outside verified connector J1")
    else:
        problems.setdefault(kind, []).append(" | ".join(issue.splitlines()[:5]))
if counts["copper_edge_clearance"] > 87:
    problems.setdefault("copper_edge_clearance", []).append("More than 87 historical J1 finger edge warnings")
if counts["unconnected_items"] > 120:
    problems.setdefault("unconnected_items", []).append("Unrouted connection count exceeded initial placement budget")
if counts["lib_footprint_issues"] > 1:
    problems.setdefault("lib_footprint_issues", []).append("More than one missing project-local footprint")
if problems:
    for key, values in sorted(problems.items()):
        print(f"FAIL {key}: {len(values)} problems")
        for value in values[:3]:
            print("  " + value)
    raise SystemExit(1)
print(f"PASS: candidate contains no new PCB DRC classes: {dict(counts)}")
print("HOLD: card-edge process, optional JP2 motherboard-RAM-disable shunt, hardware timing and fabrication remain unapproved.")
