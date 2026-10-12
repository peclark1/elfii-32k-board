# Hyperboard Rev 2 RAM source trace (in progress)

**Status:** source-backed pin inventory; not a finished standalone design. No changes to PCB geometry or previous routing are implied. Primary source: `AVIELF2HYPERBOARD-KiCad-Rev2 (1).pdf`, sheet 1 (KiCad 7 Rev 2, 2026-03-17). Cross-check: `AVIELF2v1-Sch.pdf`, sheet 1. The PDF is a rendered schematic, **not** an exported electrical netlist. Connections below marked TBD require source-path tracing before translation to KiCad.

## Address, data, controls (visually traced)

| Hyperboard component / pins | Signal and role | Standalone card | Evidence/qualification |
|---|---|---|---|
| A8 74HC573 D0..D7 = pins 2,3,4,5,6,7,8,9 | MA7,MA6,MA5,MA4,MA3,MA2,MA1,MA0 respectively | **Keep** | Captures the **high** byte, reversed ordering by bit index. |
| A8 Q0..Q7 = pins 19,18,17,16,15,14,13,12 | A15,A14,A13,A12,A11,A10,A9,A8 respectively | **Keep** | High address outputs. A15 used by range selection but **not** SRAM address input. |
| A8 pin 11 LE; pin 1 /OE | TPA to LE; /OE tied GND; pin 20 +5V, pin 10 GND | **Keep** | Transparent during TPA; holds captured upper address when TPA falls. |
| A11 CY62256 pins 10,9,8,7,6,5,4,3 | A0,A1,A2,A3,A4,A5,A6,A7 | **Keep** | Low MA byte provided directly later in the 1802 bus cycle. |
| A11 pins 25,24,21,23,2,26,1 | A8,A9,A10,A11,A12,A13,A14 | **Keep** | 62256 addresses A8..A14 respectively; A15 is range/decode input. |
| A11 pins 11,12,13,15,16,17,18,19 | D0,D1,D2,D3,D4,D5,D6,D7 | **Keep** | SRAM bidirectional data bus, direct connection to ELF expansion data contacts. |
| A11 pin 22 /OE; pin 27 /WE | /MRD; /MWR respectively | **Keep** | Direct controls, not a logic gate replacement. Final /CE must prevent unintended accesses. |
| A11 pin 20 /CS; pin 28 VCC; pin 14 GND | active-low SRAM select; +5V; ground | **Keep** | The Hyperboard's select derives from a shared RAM/ROM mapper, **not** simply A15. |
| SW1 8-position DIP (1..8 → 16..9), RN3 22k, U1 74LS151 | Each switch ties +5V to a mapper input; RN3 holds open entries low. U1 I0..I7 = pins 4,3,2,1,15,14,13,12; S0,S1,S2 = pins 11,10,9 on A12,A13,A14. | **Redesign/reduce after trace** | Enables a selectable mapping by **eight 4KiB pages**, not just one hardcoded half. U1 pin 6 is inverted /Z (pin 5 Z unused); enable pin 7; output network into /CS still needs formal netlist-level verification. |
| J8 2x2, J7, J6; A13A/B 74HC74; A7D 4011; R9/R10/R11 | Shared high-half/low-half RAM-vs-ROM and autoboot selection network | **Simplify, once verified** | J8 positions labelled LOW 32K / NORMAL / HIGH 32K; boot logic involves A15, BUS_CLK, RUN. Don't transplant that circuitry wholesale. |
| A1/A2 CDP1853 | I/O port selection, not SRAM address latching | **Omit unless subsequent tracing contradicts** | Each has its own decoded output bank; should not be assumed part of /CS. |
| A9 74HC244, A15 header | 8-bit buffer/header alongside parallel output-port circuitry | **Omit unless subsequent tracing contradicts** | Not necessary to latch MA high byte or connect SRAM data. |
| A10 28C256 | ROM | **Omit** | Has its own /CE selection and is the reason the Hyperboard has ROM/RAM switching. |
| C4 and other 0.1uF bypass; C10/C11 bulk | +5V decoupling | **Keep local bypass per IC plus bulk** | Hyperboard uses distributed bypass. Confirm value/count near final IC inventory. |

## Architecture and cross-check

The 1802 presents its *high* address byte on MA0..MA7 during TPA; A8 74HC573 stores that byte and drives A8..A15. Later MA0..MA7 becomes the SRAM low address byte A0..A7. This is the same **74HC573 + 62256** fundamental arrangement used by the AVI ELF II motherboard (A2 74HC573 / A1 CY62256). The motherboard adds an 8-switch RAM mapping mechanism and its own onboard-select circuitry, while the Hyperboard combines RAM and ROM ranges with boot choices. Thus **copy the proven address/data/read-write architecture, but isolate and verify the Hyperboard's /CS mapper before choosing a simpler standalone implementation.**

## Mandatory next verification gates

1. Trace /CS electrically from A11 pin 20 through J8, R9/R10/R11, U1 pin 6 and the boot/ROM network; record exact polarity and all jumper cases. No guessing from isolated labels.
2. Determine whether a simplified 32K LOW/HIGH jumper covers our intended use, or whether 4K-page DIP mapping is essential for coexistence with Giant Board / onboard 2101 RAM.
3. Verify bus contacts for early Netronics board; especially **contact 69 must not be grounded** based only on AVI labels, and contact 82 remains unverified.
4. Build an actual source-to-target pin map, modify schematic **only after** closing (1)-(3); use visible wires/buses, KiCad 9 ERC + extracted-netlist regression; then regenerate PCB connections without modifying 86-finger geometry/outline.
5. Run KiCad 9 PCB DRC and inspect edge fingers before any fabrication release.

**Do not interpret this research commit as ERC-validated, a complete electrical rebuild, or fabrication approval.**
