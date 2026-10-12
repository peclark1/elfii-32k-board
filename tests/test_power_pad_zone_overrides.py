#!/usr/bin/env python3
"""Review decoupling, power-net pads and copper zones for current U1-U4 design.

Supersedes the obsolete A5 U5 and /VCC zone-connect override assertions.
A filled KiCad DRC additionally checks the real thermal/zone connections.
"""
from pathlib import Path
from test_pcb_net_assignment import board_pads
from test_routed_board_review import forms

board = Path("hardware/kicad/elfii-32k-board.kicad_pcb")
nets = board_pads(board)
for ref, vcc, ground in (("U1", "20", "10"), ("U2", "28", "14"),
                         ("U3", "16", "8"), ("U4", "14", "7")):
    assert nets[(ref, vcc)] == "+5V", f"{ref} VCC not powered"
    assert nets[(ref, ground)] == "GND", f"{ref} not grounded"
for i in range(1, 6):
    assert nets[(f"C{i}", "1")] == "+5V", f"C{i} positive not powered"
    assert nets[(f"C{i}", "2")] == "GND", f"C{i} ground not connected"
zones = list(forms(board.read_text(), "zone"))
assert len(zones) == 2 and all('(net_name "GND")' in z for z in zones)
print("PASS: four ICs and five supply bypass/bulk capacitors on correct power nets; dual GND zones present")
