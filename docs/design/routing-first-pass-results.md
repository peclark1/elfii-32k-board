# Wiring and routing — first material pass

The files on `main` now contain actual wires between 14 previously net-label-only signal endpoints in the schematic and actual two-layer PCB copper for selected signals.

## Schematic
- Visible wiring drawn across the 74HCT273 address latch, 62256 SRAM and HCT decode/control gates for A8–A15, LATCH_CLK, MISMATCH, NCE, NOE, NWE and NOT_ENABLE.
- The remaining data, multiplexed address, power and bus interface still use named net-label connections; a **fully drawn, comprehensible schematic is not yet complete**.
- Re-run real KiCad 9 ERC and exported pin-net tests after drawing each group.

## PCB — first pass
- A generated grid-router attempted 35 non-power signal nets, completing 25; 10 routes (D1,D2,D3,D5,MA1,MA2,MA3,MA5,MA6,MA7) could not be completed.
- **+5V and GND remain unrouted**.
- Routes contain 4193 very short copper segments and 36 vias. They require KiCad 9 DRC, cleanup/segment coalescing, placement review and human scrutiny.
- The board is **not fabrication-ready** even if the CI framework itself reports success: check the actual rule reports.

## Acceptance
1. The exported schematic netlist must exactly satisfy the expected pin connections.
2. Actual KiCad schematic ERC must remain zero.
3. Existing tracks must be free of cross-net shorts/clearance violations other than documented original edge-finger exceptions; otherwise reroute.
4. Remaining address, data, power, enable/control lines must be routed to completion.
5. Replace simplified footprints and clear PCB DRC before manufacturing.

This is an intermediate engineering checkpoint, not authorization to submit manufacturing files.
