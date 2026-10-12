# KiCad copper zone fill validation

The first KiCad9 CLI run with `--refill-zones` failed because that flag is unsupported. Main now includes a separate `tests/fill_zones.py` using the installed KiCad `pcbnew` Python bindings to save a temporary zone-filled PCB to `out/elfii-32k-filled.kicad_pcb`. DRC and Gerber exports use this temporary filled copy.

This is not evidence of board correctness. The purpose of this check is to ensure both GND zones actually fill without shorts, and to measure the airwire reduction. Power +5 and ten signal nets remain incomplete.
