# Verify PCB file after moving power straps before zones

This validation run checks KiCad's raw PCB parser and subsequent zone fill after power straps were moved ahead of the copper zone entries. If loading fails, stop; do not certify filled power planes or start new routing.
