# Source PCB parser check

The earlier A4 zone-fill attempt returned a null board object from pcbnew.LoadBoard after the F.Cu GND/B.Cu VCC plane update. This CI run exports Gerbers directly from the source first, so errors can be attributed to PCB parser input versus zone-filler code. The source remains incomplete and unrouted.