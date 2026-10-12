# Hyperboard Rev 2 mechanical geometry — measured from Gerbers

Source supplied by project owner: `AVIELF2HYPERBOARD-Rev-2-gerbers (2).zip`, KiCad/Pcbnew 7.0.8 Gerber generation date 2026-05-26.

## Board outline
From `Edge_Cuts.gbr`, units millimeters (Gerber coordinates are absolute):
- Extreme X: 31.115 to 208.915 mm => 177.800 mm nominal width (Gerber aperture 0.100 mm).
- Extreme Y: -153.289 to -26.162 mm => 127.127 mm nominal height.
- Job file reports 177.9 × 127.227 mm because the 0.100 mm profile stroke is included in its reported size.
- Board shape has a connector tongue, stepped shoulders, and 1.27 mm chamfers. It is **not** a simple rectangle.
- Stack: two copper layers, nominal PCB thickness 1.6 mm, material FR4 in the job stackup.

## Card-edge copper
From `F_Mask.gbr`, apertures for connector `P3`:
- 43 pads on the component side; the back mask should be separately checked for an equivalent 43 pads, yielding the expected 86 contacts.
- Rectangular mask opening: 1.397 × 8.890 mm.
- Finger pitch: 2.540 mm.
- Finger center X range: 66.9036 mm to 173.5836 mm inclusive (42 pitch intervals = 106.6800 mm).
- Finger center Y: -148.7424 mm.
- Finger opening from Y=-144.2974 to -153.1874 mm, approximately 0.1016 mm before the edge at -153.289 mm.
- These dimensions are **solder-mask openings**, and coincide with the expected edge-finger geometry; compare `F_Cu.gbr` and `B_Cu.gbr` prior to freezing the actual copper footprint.
- Coordinate orientation and pad numbering are not derivable from mask openings alone. Resolve pad 1/component side against the Hyperboard schematic and original ELF II connector diagram.

## Manufacturing caveats
- No hard-gold/ENIG edge-finger finish can be established from this Gerber set. `gbrjob` has `Finish: None`.
- No edge bevel or plating requirement can be inferred. Specify and validate with PCB fabrication house.
- No non-plated drill hits are present in NPTH.drl.
- Do not assume the generic plated drill hits are intended as mounting holes without identification.
- Mechanical compatibility with the user's actual Netronics card cage must be checked on a physical print.
- The generic Gerber manufacturing rule section lists outer-layer 0.20 mm clearances and min trace width 0.25 mm, but actual routing requirements should be decided after PCB design.

## Proposed KiCad action
1. Build outline in `hardware/kicad/elfii-32k-board.kicad_pcb` using the exact segmented Edge.Cuts geometry in the source.
2. Build a reusable **86-contact edge connector footprint** with both copper/mask sides and actual numbered pad assignments, after reviewing copper and original schematic.
3. Initially keep the board outline at original Hyperboard dimensions. Shrink only after component placement and a printed mechanical trial.
4. Preserve attribution to AVI-ELF-II and confirm permission/license for reuse of original layout data before publishing anything beyond factual measurements.

## PCB coordinates on Edge.Cuts
```text
(207.645,144.272) -> (176.022,144.272)
( 32.385, 26.162) -> (207.645, 26.162)
(207.645, 26.162) -> (208.915, 27.432)
(176.022,152.019) -> (174.752,153.289)
( 64.516,144.272) -> ( 32.385,144.272)
(174.752,153.289) -> ( 65.786,153.289)
( 32.385,144.272) -> ( 31.115,143.002)
( 65.786,153.289) -> ( 64.516,152.019)
( 64.516,152.019) -> ( 64.516,144.272)
( 31.115, 27.432) -> ( 32.385, 26.162)
(208.915, 27.432) -> (208.915,143.002)
( 31.115,143.002) -> ( 31.115, 27.432)
(208.915,143.002) -> (207.645,144.272)
(176.022,144.272) -> (176.022,152.019)
```
The Edge.Cuts Gerber uses negative Y, as standard Gerber screen coordinates; the list above expresses positive KiCad board Y coordinates for direct geometric reconstruction.
