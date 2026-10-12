# ERC cleanup — Rev A3

## Baseline: first actual KiCad 9 rule check

GitHub Actions run `38192151661` used KiCad 9 to check the Rev A3 schematic and unrouted board:

- **ERC:** 156 findings: **154 endpoint-off-grid** warnings, **2 power pins not driven** errors.
- **DRC:** 100 findings: **86 board-edge clearance** issues on the deliberate edge connector fingers; **14 library-footprint mismatches** on the first-pass generic component footprints.
- **Unconnected nets/items:** 87, consistent with the board not being routed yet.

These numbers are *actual output of the first check*, not judgments about readiness for manufacture.

## Fixes now in main

1. Give the expansion connector pin **1 (+5V)** and pin **5 (GND)** KiCad `power_out` electrical types, since these supply power to the card. Other power contacts remain passive. This lets ERC recognize the external power source without attaching an arbitrary non-physical PWR_FLAG to logic.
2. Snap all placed schematic instances, labels, wires, no-connect markers and graphical annotations to a **1.27 mm / 50 mil grid**. The signal nets and MCU-to-SRAM pin mapping are intended to remain identical.
3. Add `tests/test_schematic_grid.py` as a permanent regression check.
4. Preserve the original 86-contact connector copper and its purposefully edge-reaching fingers unchanged.

## Validation acceptance criteria

- KiCad 9 schematic/netlist export and the regression checks must continue to pass.
- Expected ERC warning reduction: the large body of `endpoint_off_grid` findings should disappear and `power_pin_not_driven` findings should be resolved. **Do not claim success until confirmed by a new real ERC report**.
- Do not suppress or silently ignore ERC failures with unreviewed exceptions.
- The DRC will stay nonzero because the board is deliberately unrouted; first investigate the 14 footprint mismatches separately, then the nonstandard edge-connector clearance requirement.

## Remaining hardware decisions

- CDP1802 TPA latch edge/timing margins (scope measurement on restored ELF II).
- Whether period `MOTHER BD. MEMORIES OFF` contact 69 is usable on this exact early revision. **Still NC**.
- Original 256-byte RAM and Giant Board ROM/RAM coexistence before enabling either 32K bank.
- Correct manufacture finish/plating and bevel of fingers and test-fitted edge geometry.

The KiCad ERC/DRC workflow intentionally archives diagnostics instead of failing the build until we have a reviewed policy for the intentional remaining exceptions.

## Validated result — KiCad 9 run 38192326858

**Actual ERC: 0 violations, 0 errors, 0 warnings.** The 154 off-grid warnings and two undriven power errors were eliminated. KiCad PDF and netlist export passed; all control logic, original bus-contact safeguards, pin/net mapping, PCB pad assignment and 50-mil grid regression tests passed. The schematic ERC check has therefore been promoted to a **mandatory passing CI gate** on main.

**Actual DRC: 100 violations and 87 unconnected items** remain unchanged while the PCB is deliberately unrouted. The 100 findings comprise 86 intentional edge-finger copper-to-edge clearance reports and 14 library-footprint mismatches; these are not yet accepted as manufacturing-safe and must be addressed during layout cleanup.
