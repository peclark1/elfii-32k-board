# Hyperboard SRAM routing preview — NOT for fabrication

This branch replaces the old A5 PCB routing **only for preview**
with copper from a separate Freerouting 2.5 trial on the
Hyperboard-derived KiCad 9 schematic/placement.

This board is not authorized for fabrication or installation.
Unresolved: edge finger-to-outline DRC findings, connector finish,
the early Netronics contact 69/82 behavior, compatibility with
original 2101 RAM/Giant Board, and 1802 TPA/control timing.

The schematic's optional contact-69 disable jumper intentionally
remains **electrically disconnected at the actual J1-69 finger**.
SCHEMATIC_REBUILD_IN_PROGRESS stays in place for this reason:
the preview does not yet constitute production netlist sync.

See the routing run's uploaded hyperboard-route-preview artifact
for before/after DRC, full routing log, and review SVGs.
