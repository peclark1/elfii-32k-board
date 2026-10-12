# Isolated FreeRouting 2.5 routing trial

This experiment uses KiCad9's built-in Specctra DSN export and a pinned FreeRouting v2.5.0 CLI binary. It never modifies or pushes the source board; routing results will be saved as independent workflow artifacts and reimported to a **copy** for KiCad DRC comparison. The experiment branch is not merged unless resulting copper validates.

Data inputs remain the two-layer, full-size ELF II 32K card; memory-map and original-bus hardware uncertainties still block fabrication.
