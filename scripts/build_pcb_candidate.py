#!/usr/bin/env python3
"""Generate a Hyperboard-derived placement candidate using native KiCad pcbnew.

This deliberately does *not* mutate hardware/kicad/elfii-32k-board.kicad_pcb.
The existing J1 Gerber-derived 86-finger footprint, its position, board outline,
and mechanical geometry are left intact. All *obsolete* copper routing and
components are removed from the candidate, not carried forward accidentally.
Pass the KiCad9-exported netlist and a separate output PCB path.
"""
import sys
import re
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from test_netlist import read_nets  # noqa: E402
from test_routed_board_review import forms  # noqa: E402

BOARD = ROOT / "hardware/kicad/elfii-32k-board.kicad_pcb"

# First-pass assembly-oriented, through-hole component placement (mm in board
# coordinates). KiCad DIP origins are at pin 1, not at the package center.
# Position the 100nF bypass capacitors near each IC power pin (U1 pin 20,
# U2 pin 28, U3 pin 16, U4 pin 14); verify courtyard/clearances in native DRC.
# No routing/clearances have yet been accepted for fabrication.
PARTS = {
    "U1": ("Package_DIP:DIP-20_W7.62mm", "74HC573", 81.0, 69.0),
    "U2": ("Package_DIP:DIP-28_W15.24mm", "CY62256-70PC", 121.0, 69.0),
    "U3": ("Package_DIP:DIP-16_W7.62mm", "74HC151", 159.0, 73.0),
    "U4": ("Package_DIP:DIP-14_W7.62mm", "CD4011", 184.0, 74.0),
    "SW1": (
        "Button_Switch_THT:SW_DIP_SPSTx08_Slide_9.78x22.5mm_W7.62mm_P2.54mm",
        "RAM_PAGE_ENABLE", 157.0, 111.0,
    ),
    "RN1": ("Resistor_THT:R_Array_SIP9", "8x22K", 180.0, 124.0),
    "JP1": (
        "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
        "RAM_HALF", 197.0, 98.0,
    ),
    "JP2": (
        "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
        "MB_RAM_DISABLE_SLOT5", 190.0, 103.0,
    ),
    "C1": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 94.0, 69.0),
    "C2": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 142.0, 69.0),
    "C3": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 173.0, 73.0),
    "C4": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 199.0, 65.0),
    "C5": ("Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", "10u POLARIZED PIN1=+5V", 199.0, 48.0),
}

# Slot-5 baseline: the known-working AVI Hyperboard grounds expansion contact 69,
# which disables the original motherboard RAM. On this standalone PCB J1-69
# must instead route to JP2 pin 1 (MB_RAM_DISABLE) and JP2 pin 2 to GND.
# Closing JP2 reproduces the Hyperboard grounding action; the default
# mechanical state is OPEN without a jumper. J1-82 is still NC.
RESERVED_OPEN_CONTACTS = {("J1", "82")}


def footprint_library_location(library: str) -> Path:
    paths = (
        Path("/usr/share/kicad/footprints"),
        Path("/usr/local/share/kicad/footprints"),
        Path("/usr/share/kicad9/footprints"),
    )
    for directory in paths:
        folder = directory / (library + ".pretty")
        if folder.is_dir():
            return folder
    raise RuntimeError(f"KiCad footprint library not installed: {library}")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_pcb_candidate.py KiCad-exported.net output.kicad_pcb")
    netlist = Path(sys.argv[1])
    target = Path(sys.argv[2])
    if target.resolve() == BOARD.resolve():
        raise SystemExit("Refusing to overwrite original PCB")
    # Deleting hundreds of old PCB_TRACK objects through KiCad9's Python SWIG
    # bindings can crash the interpreter. Work on a *textual temporary copy*
    # instead, then let pcbnew load a clean, valid KiCad board. This retains the
    # exact edge-contact footprint bytes and all Edge.Cuts shapes.
    target.parent.mkdir(parents=True, exist_ok=True)
    source = BOARD.read_text(encoding="utf-8")
    stripped = {"segment": 0, "via": 0, "zone": 0, "footprint": 0}
    for kind in ("segment", "via", "zone"):
        blocks = list(forms(source, kind))
        stripped[kind] = len(blocks)
        for block in blocks:
            source = source.replace(block, "", 1)
    for block in list(forms(source, "footprint")):
        if not re.search(r'\((?:fp_text\s+reference|property\s+"Reference")\s+"J1"', block):
            source = source.replace(block, "", 1)
            stripped["footprint"] += 1
    safe_base = target.parent / "elfii-32k-candidate-blank-base.kicad_pcb"
    safe_base.write_text(source, encoding="utf-8")
    print(f"Removed old architecture on temporary board: {stripped}", flush=True)

    board = pcbnew.LoadBoard(str(safe_base))
    if board is None:
        raise RuntimeError("KiCad9 cannot load mechanically preserved base PCB")
    original_j1 = [fp for fp in board.GetFootprints() if fp.GetReference() == "J1"]
    if len(original_j1) != 1:
        raise RuntimeError("Expected exactly one original Gerber-derived edge connector")
    assert len(list(original_j1[0].Pads())) == 86, "Original 86 copper fingers missing"

    pin_nets = {}
    for signal, nodes in read_nets(netlist).items():
        if signal.startswith("unconnected-"):
            continue
        for ref, pin in nodes:
            pair = ref, pin
            if pair in pin_nets and pin_nets[pair] != signal:
                raise RuntimeError(f"Conflicting pin nets for {pair}")
            pin_nets[pair] = signal

    for ref, (library_id, value, x, y) in PARTS.items():
        library, name = library_id.split(":", 1)
        fp = pcbnew.FootprintLoad(str(footprint_library_location(library)), name)
        if fp is None:
            raise RuntimeError(f"KiCad9 cannot load footprint {library_id}")
        fp.SetReference(ref)
        fp.SetValue(value)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        board.Add(fp)

    connected = set()
    missing_pads = []
    for footprint in board.GetFootprints():
        ref = footprint.GetReference()
        for pad in footprint.Pads():
            key = ref, pad.GetNumber()
            pad.SetNetCode(0)
            if key in RESERVED_OPEN_CONTACTS:
                continue
            signal = pin_nets.get(key)
            if signal is None:
                continue
            name = signal if signal in ("+5V", "GND") else "/" + signal
            net = board.FindNet(name)
            if net is None:
                net = pcbnew.NETINFO_ITEM(board, name)
                board.Add(net)
            pad.SetNet(net)
            connected.add(key)

    for key in pin_nets:
        if key not in connected and key not in RESERVED_OPEN_CONTACTS:
            missing_pads.append(key)
    if missing_pads:
        raise RuntimeError(f"Schematic pins lacking physical PCB pads: {sorted(missing_pads)}")

    target.parent.mkdir(parents=True, exist_ok=True)
    pcbnew.SaveBoard(str(target), board)
    print(f"Candidate: {target} ({target.stat().st_size} bytes)")
    print(f"Footprints: {len(list(board.GetFootprints()))}; tracks: {len(list(board.GetTracks()))}")
    print(f"Schematic pin memberships assigned: {len(connected)}")
    print("J1-69 connected to JP2-1 (MB_RAM_DISABLE); JP2-2 is GND. Install JP2 shunt in Slot 5 to reproduce proven Hyperboard RAM inhibit.")
    print("J1-82 remains NC; verify C5 radial pin1 polarity and finger fabrication before manufacturing.")
    print("UNROUTED PLACEMENT STUDY ONLY. DO NOT FABRICATE.")


if __name__ == "__main__":
    main()
