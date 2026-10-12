# PCB parser repair

KiCad rejected `connect_pads full (clearance 0.3)` in both ground-zone declarations: the valid default syntax is `(connect_pads (clearance 0.3))`. Both were corrected in `main` in commit `2827e855`, and a regression test was added. This branch triggers KiCad 9 validation of the source board and the filled-zone copy. The board remains partially routed and is not fabrication-ready.
