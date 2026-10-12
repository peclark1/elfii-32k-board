#!/usr/bin/env python3
"""Protect the proven Slot-5 RAM-disable contact and unresolved J1-82.

Original motherboard RAM-disable on pin 69 is established project evidence.
The shunt to ground stays optional, not permanently installed.
"""
from pathlib import Path
import re
from test_pcb_net_assignment import board_pads


def main():
    nets = board_pads(Path("hardware/kicad/elfii-32k-board.kicad_pcb"))
    library = Path("hardware/kicad/ELFII_Expansion.kicad_sym").read_text()
    schematic = Path("hardware/kicad/elfii-32k-board.kicad_sch").read_text()
    for name, data in (("library", library), ("schematic", schematic)):
        matches = re.findall(r'\(name "([^"]+)"[^\n]*\(number "69"', data)
        assert matches == ["MEMORY_OFF?"], (name, matches)
    assert nets[("J1", "69")] == "MB_RAM_DISABLE", "J1-69 physically goes to JP2, not NC or GND"
    assert nets[("JP2", "1")] == "MB_RAM_DISABLE", "JP2-1 is RAM-disable"
    assert nets[("JP2", "2")] == "GND", "JP2-2 is ground"
    assert nets[("J1", "82")] is None, "J1-82 stays NC"
    for number in ("5", "80"):
        assert nets[("J1", number)] == "GND", f"J1-{number} must remain a GND return"
    print("PASS: J1-69->JP2-1, JP2-2 GND, shunt optional, J1-82 NC")


if __name__ == "__main__":
    main()
