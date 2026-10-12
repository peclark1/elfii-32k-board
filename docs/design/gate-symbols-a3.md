# Revision A3 — conventional logic gates and electrical review

> **Historical A2/A3 checkpoint, superseded on 2026-10-12:** The accepted
> Hyperboard-derived PCB physically routes **J1-69 to JP2-1**, with JP2-2
> to GND and the shunt normally open. The original Slot-5 motherboard
> RAM-disable action is established evidence. **J1-82 remains NC/unresolved**.
> Statements below describing J1-69 as disconnected or unverified apply
> only to the older experiment, not the revised PCB.


## Implemented in KiCad schematic

Changed **symbol graphics and schematic placement only**; the SRAM decode logic is intended to be electrically identical to A2.

- U3 (74HCT04): six one-input NOT-gate units plus one power unit.
  - Unit A: U3 pin 1 (TPA) → pin 2 (LATCH_CLK)
  - Unit B: U3 pin 3 (ENABLE) → pin 4 (NOT_ENABLE)
  - Units C–F: unused inputs tied to ground; corresponding unused outputs NC
  - Unit G: pins 14 (+5V) and 7 (GND)
- U4 (74HCT86): four two-input XOR-gate units plus one power unit.
  - Unit A: pins 1 A15, 2 REGION → pin 3 MISMATCH
  - Units B–D: unused inputs tied to GND, outputs NC
  - Unit E: pins 14 (+5V), 7 (GND)
- U5 (74HCT32): four two-input OR-gate units plus one power unit.
  - Unit A: pins 1 MISMATCH, 2 NOT_ENABLE → pin 3 NCE
  - Unit B: pins 4 NCE, 5 NMRD → pin 6 NOE
  - Unit C: pins 9 NCE, 10 NMWR → pin 8 NWE
  - Unit D: unused inputs tied to GND, output NC
  - Unit E: pins 14 (+5V), 7 (GND)

No PCB pads were moved or routed in this revision.

## Functional assertions

```text
NCE = (A15 XOR REGION) OR (NOT ENABLE)
NOE = NCE OR NMRD
NWE = NCE OR NMWR
```

An asserted-low NMRD or NMWR is expected to gate only the selected SRAM read/write control. Confirm their polarity independently against the original early Netronics motherboard circuitry.

## Validation requirements

The first validation gate is that `kicad-cli sch export netlist` accepts the new multi-unit definitions and that `tests/test_netlist.py` and `tests/test_pcb_net_assignment.py` pass without changes to their expected pin memberships. Also verify that the KiCad-generated schematic PDF displays every logical unit.

**Important:** Passing these export and connectivity tests is not KiCad ERC/DRC; TPA setup/hold, SRAM access timing, motherboard/giant-board memory overlap and the unresolved physical function of bus pins 69 and 82 remain pre-fabrication blockers.

## Manufacturing

DO NOT USE CI Gerbers for manufacture. Full PCB routing, authoritative footprints, clearance checking and bench measurements remain incomplete.
