#!/usr/bin/env python3
"""Generate a Hyperboard-derived placement candidate using native KiCad pcbnew.

This deliberately does *not* mutate hardware/kicad/elfii-32k-board.kicad_pcb.
The existing J1 Gerber-derived 86-finger footprint, its position, board outline,
and mechanical geometry are left intact. All *obsolete* copper routing and
components are removed from the candidate, not carried forward accidentally.
Pass the KiCad9-exported netlist and a separate output PCB path.
"""
import sys
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from test_netlist import read_nets, balanced_forms  # noqa: E402

BOARD = ROOT / "hardware/kicad/elfii-32k-board.kicad_pcb"

# First-pass assembly-oriented, through-hole component placement (mm in board
# coordinates). No routing/clearances have yet been accepted for fabrication.
PARTS = {
    "U1": ("Package_DIP:DIP-20_W7.62mm", "74HC573", 81.0, 69.0),
    "U2": ("Package_DIP:DIP-28_W15.24mm", "CY62256-70PC", 121.0, 69.0),
    "U3": ("Package_DIP:DIP-16_W7.62mm", "74LS151", 159.0, 73.0),
    "U4": ("Package_DIP:DIP-14_W7.62mm", "CD4011", 184.0, 74.0),
    "SW1": (
        "Button_Switch_THT:SW_DIP_SPSTx08_Slide_9.78x22.5mm_W7.62mm_P2.54mm",
        "RAM_PAGE_ENABLE", 157.0, 111.0,
    ),
    "RN1": ("Resistor_THT:R_Array_SIP9", "8x22K", 188.0, 113.0),
    "JP1": (
        "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
        "RAM_HALF", 190.0, 92.0,
    ),
    "JP2": (
        "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
        "MEM_DISABLE_UNVERIFIED", 190.0, 103.0,
    ),
    "C1": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 86.0, 94.0),
    "C2": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 126.0, 104.0),
    "C3": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 160.0, 93.0),
    "C4": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "100n", 185.0, 86.0),
    "C5": ("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", "10u REVIEW FOOTPRINT", 199.0, 48.0),
}

# Physical edge-contact 69 is disputed on the EARLY Netronics motherboard.
# Keep the copper finger but do not connect it to a jumper or GND. JP2 remains
# on this exploratory layout with a disconnected motherboard end; must be
# resolved before synchronization can be considered complete.
RESERVED_OPEN_CONTACTS = {("J1", "69"), ("J1", "82")}


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
        blocks = balanced_forms(source, kind + " ")
        stripped[kind] = len(blocks)
        for block in blocks:
            source = source.replace(block, "", 1)
    for block in balanced_forms(source, "footprint "):
        if 'fp_text reference "J1"' not in block:
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
    print("J1 contact 69 RESERVED NC. C5 footprint and finger fabrication STILL UNVERIFIED.")
    print("UNROUTED PLACEMENT STUDY ONLY. DO NOT FABRICATE.")


if __name__ == "__main__":
    main()
