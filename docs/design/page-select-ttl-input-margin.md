# 74LS151 page-switch pull-down margin — design review

**Status: electrical risk requiring resolution before fabrication.** This review is distinct from the source tracing and does **not** claim the Hyperboard's physical implementation was faulty in service.

## What the Hyperboard source actually shows

The Rev 2 sheet shows **SW1** connecting each of eight page inputs to **+5 V** when closed; **RN3 = 8 × 22 kΩ to GND** for open positions; and **U1 = 74LS151** receiving these signals on multiplexer data inputs I0..I7. The standalone schematic originally copied that arrangement as SW1, RN1 (22 kΩ) and U3 (74LS151). The 74LS151's inverted output (~Z, pin 6) is used as active-low SRAM chip select.

## Additional datasheet engineering check (not asserted by source schematic)

According to the 74LS151 electrical specification, **I_IL may reach −0.4 mA** while the guaranteed input LOW limit is **0.8 V**. A passive pull-down must therefore satisfy **R ≤ 0.8 V / 0.4 mA = 2 kΩ** to meet the worst-case LOW-current specification. The source's **22 kΩ cannot guarantee a valid OFF/LOW state** over the published LS TTL limits.

- TI 74LS151: https://www.ti.com/lit/ds/symlink/sn74ls151.pdf
- Motorola 74LS151 tables (historical): https://www.bitsavers.org/components/motorola/_dataBooks/1977_Motorola_Semiconductor_Data_Library_Volume_9_Series_B_LS_TTL.pdf
- TI SN74HC151: https://www.ti.com/lit/ds/symlink/sn74hc151.pdf

**Recommended standalone adaptation:** use the pin-compatible, DIP-16 **74HC151**, which draws at most about **1 µA input leakage** and can safely use 22 kΩ pull-downs; retain the eight DIP page switches and address-bus decode scheme exactly as traced. HC151 pin assignments and active-low inverted output match LS151, but timing must still be checked on the 1802 bus. An alternate exact-LS implementation would reduce RN1 to approximately 1 kΩ, at the cost of up to ~5 mA per enabled page switch.

## Physical bench acceptance before fab

Check that each page OFF yields a confidently low U3 data input and each ON a valid high input, and verify SRAM /CS timing against TPA, A15, MRD/MWR, especially when switching page/half. KiCad ERC and netlist checks **cannot** validate TTL input current margins. A known-working Hyperboard demonstration does not replace datasheet-corner analysis.

**Source-vs-adaptation provenance:** SW1+RN3+LS151 is original Hyperboard circuitry; changing U3 to HC151 is an explicit reliability adaptation for this standalone card, not a claim that the Rev 2 source used HC151.
