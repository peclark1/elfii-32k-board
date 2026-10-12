# KiCad 9 ERC / DRC validation status

As of revision A3, GitHub Actions uses the official KiCad 9 Ubuntu releases PPA on Ubuntu 24.04 and calls:

```sh
kicad-cli sch erc hardware/kicad/elfii-32k-board.kicad_sch -o out/erc.txt
kicad-cli pcb drc hardware/kicad/elfii-32k-board.kicad_pcb -o out/drc.txt
```

The resulting files are archived alongside the schematic PDF, netlist and Gerber export in the `kicad-import-exports` workflow artifact.

**Reports are diagnostic only at this stage:** ERC/DRC commands have temporary `|| true` handling because the PCB is deliberately not routed and some validation findings are expected. The CI job passing **does not** mean ERC or DRC passed.

Once all intended schematic connections and the final footprints are verified, promote ERC to a required passing gate; promote DRC only when the PCB is routed and the design-rule settings have been established.

## Checks to investigate from ERC

1. Power driving: passive connector +5 and GND may need ERC power flags, but ensure they reflect real power-feed source.
2. Pin drive types: memory data bus, /OE /WE /CE, and the latch should use appropriate output/input/bidirectional types.
3. Unused pins: deliberate NC marks on 86-contact expansion connector and unused logic outputs.
4. Confirm that the 74HCT04 inverter is the correct TPA latch polarity against the actual CPU timing and original board.

## Checks to investigate from DRC

1. Incomplete routing, expected until routing begins.
2. Simplified footprints on original first-pass placement. Replace with authoritative package designs before fabrication.
3. Connector finger/copper clearance and motherboard socket orientation.
4. Edge plating/bevel and keepout details, none of which a netlist test validates.

No fabrication approval is implied by automated CLI output.
