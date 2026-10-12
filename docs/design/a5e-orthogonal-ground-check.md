# Orthogonal ground traces and Specctra export checkpoint

This run validates the **current main** after a ground-bypass trace was corrected to vertical (its endpoint is inside the U2 GND pad). Previous doc-only PR #23 was based on the earlier skewed version and its track-quality test failed as intended.

KiCad must confirm:
- Schematic ERC and all pin/net mapping checks pass.
- Copper topology test passes.
- Filled PCB DRC shows no new short or copper clearances.
- The edge connector ground finger and bypass GND pins are connected where new tracks were added.
- ExportSpecctraDSN succeeds, creating `out/elfii-32k-board.dsn`.

This PCB remains intentionally unfinished and not fabrication-ready.
