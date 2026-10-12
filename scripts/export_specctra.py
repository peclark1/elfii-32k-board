#!/usr/bin/env python3
"""Export a KiCad 9 PCB as Specctra DSN for FreeRouting.

The source board is read-only. FreeRouting routing should be imported into a
copy and checked with KiCad DRC before replacing the authoritative PCB.
"""
from pathlib import Path
import sys

import pcbnew


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: export_specctra.py input.kicad_pcb output.dsn")
    source, dest = map(Path, sys.argv[1:])
    if source.resolve() == dest.resolve():
        raise SystemExit("Cannot overwrite source PCB")
    pcb = pcbnew.LoadBoard(str(source))
    if pcb is None:
        raise SystemExit(f"KiCad could not load board: {source}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    result = pcbnew.ExportSpecctraDSN(pcb, str(dest))
    if not result or not dest.exists() or dest.stat().st_size == 0:
        raise SystemExit("KiCad Specctra DSN export failed")
    print(f"Exported {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
