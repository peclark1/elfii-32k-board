# A4 schematic and power plane test status

Revision A4 groups SRAM/latch pins by function and draws short, visible A8–A14 wires. The first KiCad9 netlist test found that U3 pin 2 had become disconnected from `LATCH_CLK`: that label was unintentionally omitted when the long wire routing was removed. It was restored in the main branch at commit `a06f183`.

This validation run must confirm all 62256 and 74HCT pin assignments, zero ERC findings, a zone-filled F.Cu GND/B.Cu +5V PCB, and no new shorts/clearance issues. PCB is only partially routed and simplified footprints remain unresolved.

**Do not fabricate until remaining signal airwires and all design rules have been addressed.**
