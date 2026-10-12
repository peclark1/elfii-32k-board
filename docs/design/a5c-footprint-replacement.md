# A5c — KiCad footprint replacement

All **14 placed components** other than the custom 86-finger edge connector were rebuilt using source geometry from KiCad's published through-hole component footprint library. The changes preserve:

- Original pad numbers and all assigned electrical nets.
- Exact physical pad center coordinates (checked for all **109** component pads).
- Existing schematic reference/path mapping.
- The board outline, 613 consolidated track segments and 36 routing vias.

The new footprints provide DIP pin-one marks, outline silkscreen, fabrication shapes and courtyards; resistors, capacitors and jumper headers have their proper mechanical envelopes.

Original source libraries were historical-format `.kicad_mod` definitions, converted to the current KiCad footprint representation. **Real KiCad 9 source parsing and DRC remain mandatory before approval**; any footprint-library mismatch must be investigated before fabrication, and 3D model support may need refresh.

The board remains incomplete: 10 non-power nets are unrouted and +5V/GND pours require final connectivity review. This is a validation checkpoint, not a finished PCB.
