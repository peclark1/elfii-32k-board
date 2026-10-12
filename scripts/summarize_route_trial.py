#!/usr/bin/env python3
"""Report objective Freerouting preview metrics from native KiCad 9 PCB/DRC.

Preview only: success does NOT approve early ELF II contact 69, the card-edge
plating/bevel/clearances, 2101 conflict, or TPA bus timing for fabrication.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pcbnew


def pcb_metrics(filename):
    board = pcbnew.LoadBoard(str(filename))
    if board is None:
        raise RuntimeError(f"KiCad could not load {filename}")
    tracks = list(board.GetTracks())
    return {
        "footprints": len(list(board.GetFootprints())),
        "pads": sum(len(list(fp.Pads())) for fp in board.GetFootprints()),
        "track_segments": sum(not isinstance(t, pcbnew.PCB_VIA) for t in tracks),
        "vias": sum(isinstance(t, pcbnew.PCB_VIA) for t in tracks),
    }


def drc_metrics(filename):
    txt = Path(filename).read_text(encoding="utf-8")
    violations = re.search(r"\\*\\* Found (\\d+) DRC violations \\*\\*", txt)
    missing = re.search(r"\\*\\* Found (\\d+) unconnected items \\*\\*", txt)
    if not violations or not missing:
        raise RuntimeError(f"Native KiCad DRC summary missing from {filename}")
    types = Counter(re.findall(r"^\\[([a-z][a-z0-9_]+)\\]:", txt, re.M))
    return {
        "violations": int(violations.group(1)),
        "unconnected_items": int(missing.group(1)),
        "categories": dict(types),
    }


def main():
    if len(sys.argv) != 6:
        raise SystemExit(
            "usage: summarize_route_trial.py before.kicad_pcb after.kicad_pcb "
            "before.drc after.drc summary.json"
        )
    b_pcb, a_pcb, b_drc, a_drc, output = map(Path, sys.argv[1:])
    before = {"pcb": pcb_metrics(b_pcb), "drc": drc_metrics(b_drc)}
    after = {"pcb": pcb_metrics(a_pcb), "drc": drc_metrics(a_drc)}
    result = {
        "status": "UNAPPROVED ROUTING PREVIEW",
        "before": before,
        "after": after,
        "reduction_in_unconnected_items": (
            before["drc"]["unconnected_items"] - after["drc"]["unconnected_items"]
        ),
        "constraints": [
            "Original edge contact 69 is kept physically unconnected pending early Netronics check",
            "86 intentional J1 copper/board-edge DRC findings require fabrication review",
            "Original motherboard 2101, Giant Board overlap, timing and edge bevel unresolved",
            "Passing electrical DRC does not authorize fabrication",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["reduction_in_unconnected_items"] <= 0:
        print("WARNING: router failed to reduce outstanding connectivity")


if __name__ == "__main__":
    main()
