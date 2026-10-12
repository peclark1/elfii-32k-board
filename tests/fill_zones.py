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
    zone_count = pcb.GetAreaCount()
    if zone_count < 2:
        raise SystemExit(f"Expected at least two GND pour zones; found {zone_count}")
    filler = pcbnew.ZONE_FILLER(pcb)
    filler.Fill(pcb.Zones())
    pcbnew.SaveBoard(str(destination), pcb)
    print(f"Filled {zone_count} zones and saved {destination}")


if __name__ == "__main__":
    main()
