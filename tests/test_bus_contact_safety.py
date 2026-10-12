#!/usr/bin/env python3
"""Electrical safety guard against silently grounding disputed ELF II contacts.

This enforces the conservative Rev A2 decision, *not* a claim about which
contacts the original motherboard physically bonds to ground.
"""
from pathlib import Path
from test_pcb_net_assignment import board_pads


def main():
    board = Path("hardware/kicad/elfii-32k-board.kicad_pcb")
    nets = board_pads(board)
    # The period Netronics 4K memory board explicitly calls contact 69
    # "MOTHER BD. MEMORIES OFF"; do not quietly revert to a GND pin label.
    symbol_lib = Path("hardware/kicad/ELFII_Expansion.kicad_sym").read_text()
    embedded_schematic = Path("hardware/kicad/elfii-32k-board.kicad_sch").read_text()
    for source, body in (("library", symbol_lib), ("schematic", embedded_schematic)):
        import re
        matches = re.findall(
            r'\(name "([^"]+)"[^\n]*\(number "69"', body
        )
        assert matches == ["MEMORY_OFF?"], (
            f"{source} pin 69 must be labeled MEMORY_OFF? (period Netronics reference): {matches}"
        )
    for pad in ("69", "82"):
        assert nets[("J1", pad)] is None, f"J1 pad {pad} has unresolved function, must stay NC"
    for pad in ("5", "80"):
        assert nets[("J1", pad)] == "GND", f"J1 pad {pad} must be existing ground return"
    print("PASS: bus contact 69 and 82 left NC; pads 5 and 80 retain GND")


if __name__ == "__main__":
    main()
