# Hyperboard SRAM routing preview — NOT for fabrication

This branch replaces the old A5 PCB routing **only for preview**
with copper from a separate Freerouting 2.5 trial on the
Hyperboard-derived KiCad 9 schematic/placement.

This board is not authorized for fabrication or installation.
Unresolved: edge finger-to-outline DRC findings, connector finish,
early-Netronics contact 82, JP2 shunt, and compatibility with
original 2101 RAM/Giant Board, and 1802 TPA/control timing.

The original contact J1-69 now connects to JP2-1; JP2-2
connects to GND. Closing JP2 reproduces the known-working
Hyperboard's Slot-5 onboard-RAM-disable connection. J1-69 is
not hardwired to GND. The preview still needs final physical
and functional validation before fabrication.

See the routing run's uploaded hyperboard-route-preview artifact
for before/after DRC, full routing log, and review SVGs.
