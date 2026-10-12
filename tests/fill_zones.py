#!/usr/bin/env python3
"""Refill KiCad PCB copper zones into a separate output board for DRC/Gerbers.

Requires KiCad's pcbnew Python bindings. Use /usr/bin/python3 on Ubuntu.
Never silently overwrite the source KiCad board.
"""
import sys
from pathlib import Path

import pcbnew


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: fill_zones.py input.kicad_pcb output.kicad_pcb")
    source, destination = map(Path, sys.argv[1:])
    if source.resolve() == destination.resolve():
        raise SystemExit("Refusing to overwrite the source PCB")
    destination.parent.mkdir(parents=True, exist_ok=True)
    pcb = pcbnew.LoadBoard(str(source))
    if pcb is None:
        # Isolate loader failure without changing the authoritative project.
        import tempfile
        original = source.read_text(encoding="utf-8")
        edits = {
            "remove connector power straps": "\\n".join(
                row for row in original.splitlines() if 'tstamp "ab102026-' not in row
            ),
            "remove copper zones and straps": None,
        }
        import re
        edits["remove copper zones and straps"] = re.sub(
            r'\\n\\(zone \\(net .*?\\n\\)\\n', "\\n",
            edits["remove connector power straps"],
            flags=re.S,
        )
        edits["revert power plane to original GND, no straps"] = (
            edits["remove connector power straps"]
            .replace('(zone (net 37) (net_name "/VCC") (layer "B.Cu")',
                     '(zone (net 18) (net_name "/GND") (layer "B.Cu")')
        )
        with tempfile.TemporaryDirectory() as tmp:
            for name, text in edits.items():
                trial = Path(tmp) / "trial.kicad_pcb"
                trial.write_text(text, encoding="utf-8")
                opened = pcbnew.LoadBoard(str(trial)) is not None
                print(f"DIAG: {name}: {'loads' if opened else 'fails'}", flush=True)
        raise SystemExit("Source board could not be loaded; see diagnostics above")
    zone_count = pcb.GetAreaCount()
    if zone_count < 2:
        raise SystemExit(f"Expected at least two GND pour zones; found {zone_count}")
    filler = pcbnew.ZONE_FILLER(pcb)
    filler.Fill(pcb.Zones())
    pcbnew.SaveBoard(str(destination), pcb)
    print(f"Filled {zone_count} zones and saved {destination}")


if __name__ == "__main__":
    main()
