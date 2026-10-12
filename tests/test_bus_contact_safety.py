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
    for pad in ("69", "82"):
        assert nets[("J1", pad)] is None, f"J1 pad {pad} has unresolved function, must stay NC"
    for pad in ("5", "80"):
        assert nets[("J1", pad)] == "GND", f"J1 pad {pad} must be existing ground return"
    print("PASS: bus contact 69 and 82 left NC; pads 5 and 80 retain GND")


if __name__ == "__main__":
    main()
