#!/usr/bin/env python3
"""Import a FreeRouting Specctra .ses session into a separate KiCad board.

No source file is overwritten. Run real KiCad DRC on the produced PCB before
considering its traces for the authoritative design.
"""
import sys
from pathlib import Path
import pcbnew


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: import_specctra.py source.kicad_pcb route.ses result.kicad_pcb")
    source, session, output = map(Path, sys.argv[1:])
    if not session.is_file() or session.stat().st_size == 0:
        raise SystemExit("Specctra router did not produce a session")
    if source.resolve() == output.resolve():
        raise SystemExit("Refusing to overwrite source PCB")
    board = pcbnew.LoadBoard(str(source))
    if board is None:
        raise SystemExit("Unable to open KiCad source board")
    original = len(board.GetTracks())
    if not pcbnew.ImportSpecctraSES(board, str(session)):
        raise SystemExit("KiCad failed to import Freerouting session")
    output.parent.mkdir(parents=True, exist_ok=True)
    pcbnew.SaveBoard(str(output), board)
    print(f"Imported session: {original} source tracks/vias -> {len(board.GetTracks())} result tracks/vias")


if __name__ == "__main__":
    main()
