# Hyperboard 32K SRAM PCB — routing checkpoint (2026-10-12)

## Current, verified result

The **new Hyperboard-derived circuit** has completed its first two-layer copper
routing pass. This is NOT the earlier A5 custom-logic board.

- **Source:** `main` at `ceee8d6e4f12c433345f38dfb0dad634cce6a1a2`.
- **GitHub Actions:** [successful, independently validated routing trial](https://github.com/peclark1/elfii-32k-board/actions/runs/38270282254)
- **Review-only routed PCB:** [`experiment/hyperboard-route-ceee8d6e`](https://github.com/peclark1/elfii-32k-board/tree/experiment/hyperboard-route-ceee8d6e)
- **Review-branch commit:** `5070d67a9f58bde8a14c3973796e9a14bba43058`.
- **Downloadable action artifact:** `hyperboard-route-preview` (DSN, SES, source
  netlist, unrouted/routed KiCad files, native DRC reports, review SVG, router log
  and `routing-summary.json`).

KiCad 9 / Freerouting 2.5 actual measurements **in the temporary routing workspace**:

| Check | Before copper | Routed preview |
| --- | ---: | ---: |
| Unconnected items | 96 | **0** |
| Copper track segments | 0 | **426** |
| Plated vias | 0 | **27** |
| Staging-directory DRC findings (excludes airwires) | 87 | **87** |
| Intentional J1 copper-to-edge findings | 86 | 86 |
| Footprint-library mismatch/missing issue | 1 | 1 |
| New routing clearance/short/mask/silk/thermal issue | 0 | **0** |

### Full-project native DRC: **0 violations**

A separate verification run checked out the routed experiment branch and ran
KiCad 9 DRC **from `hardware/kicad/`**, with its local `fp-lib-table` and
`elfii-32k-board.kicad_dru` present. This test produced:

- **0 DRC violations; 0 unconnected pads; 0 footprint errors.**
- All 86 card-edge clearances are correctly scoped under the original
  project-specific J1-only design rule.
- The staging-only `lib_footprint_issues` report disappears because the
  project-local `ELFII_Expansion` footprint library is available.

Independent proof: [GitHub Actions run 38270750084](https://github.com/peclark1/elfii-32k-board/actions/runs/38270750084),
artifact `routed-board-project-directory-drc`.

**This DRC result does not mean that the edge fingers are fabricator-approved,
nor does it prove compatibility with the early original ELF II.**

Additional automated acceptance:

- KiCad schematic ERC: zero errors and warnings.
- Hyperboard-specific schematic pin/net regression: 138 expected memberships
  across 41 nets, including MA, data, 573 high latch, page selector and controls.
- KiCad exported schematic to PCB pad/net consistency: 137 connected pins;
  204 physical pads reviewed; **J1 contact 69 intentionally exempt/NC in this historical route checkpoint; revised netlist validation now requires JP2 routing**.
- Full mechanically measured 86 edge fingers and 14 board-outline segments:
  unchanged.
- Output file opens in native KiCad 9, and Freerouting SES imports successfully.

## Status — electrically routed, **not fabrication ready**

These are the remaining decisions and hard blockers:

1. **Slot-5 onboard RAM inhibit is resolved as a function, but the earlier
   routed preview still has an open connector contact.** The original
   Netronics label is `MOTHER BD. MEMORIES OFF`; the Hyperboard grounds
   J1-69 and is already known from prior work to disable the user's original
   ELF II motherboard RAM when plugged into slot 5. The revised PCB
   generator now routes **J1-69 to JP2-1; JP2-2 to GND**, so a closed jumper
   reproduces that behavior. Re-run autorouting/DRC and do not fabricate
   the **old** `experiment/hyperboard-route-ceee8d6e` branch, which left
   J1-69 NC. Contact J1-82 remains unverified/NC.
2. **Onboard 2101 RAM and Giant Board coexistence:** test actual early motherboard
   and installed expansion configuration, then establish a safe memory map
   before enabling the new RAM on hardware.
3. **Timing and read/write bus compatibility:** capture/confirm TPA high-byte
   latch and /CS, /OE, /WE timing at the installed clock, including selected
   and unselected pages and high/low 32K settings.
4. **Edge connector production details:** 86 copper-to-Edge.Cuts findings
   arise because card-edge fingers intentionally approach the insertion edge.
   Confirm finished 1.6-mm board thickness, bevel depth, selective gold
   plating, socket engagement and solder-mask keep-out with fabricator.
5. **Footprint library:** the one staging-directory warning is resolved
   in the actual project directory; maintain the proper KiCad project-local
   library and scoped J1-only edge rule when integrating into `main`.
6. **PCB quality review:** inspect both copper layers and all vias in KiCad,
   especially supply/return integrity, decoupler routing, unused-finger
   clearance, track neck-downs and mounting/slot clearance.

The review branch deliberately retains
`hardware/kicad/SCHEMATIC_REBUILD_IN_PROGRESS`; `main` retains the old A5
routing study instead of pretending it matches the current electrical schematic.

## Next development action

Review front/back SVGs and native routed PCB from the Action artifact.
Then address the single library-footprint finding and evaluate the electrical
and mechanical open questions above. With the Slot-5 J1-69 routing requirement now decided, validate a newly
routed revision in which J1-69 physically reaches JP2-1. Once that revision
passes full KiCad ERC, netlist, and PCB DRC checks, consider promotion onto
`main`; other physical/bus/fabrication holds remain.
