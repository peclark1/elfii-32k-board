# A5b: tied bypass rails and solid power-zone connections

The KiCad schematic now visibly connects all five bypass capacitors to common +5V and GND rails, rather than repeating isolated net labels. Both rails have explicit intermediate junctions.

The PCB has F.Cu GND / B.Cu +5 V pours. In the preceding DRC, four thermal spokes were starved, and a total of 26 items remained unconnected (16 signal connections, 7 GND and 3 VCC). Thirteen specific power/ground pads were changed to solid copper zone connections as a tentative correction.

**Verify with KiCad 9:** schema ERC and pin/net regression unchanged, no new copper shorts or zone clearances, reduced thermal and power unconnected counts. Any remaining isolated net or loss of signal nets is a blocker. The 86 edge-finger and 14 library-footprint warnings remain independent.

Do not fabricate; ten signal nets, original hardware compatibility and footprint work remain incomplete.
