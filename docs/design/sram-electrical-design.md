# 32K SRAM control logic — initial electrical review

Status: **proposed combinational design, not bench verified**. Sources: original ELF II manual bus pinout, Hyperboard Rev2 P3 copper Gerber net attributes, *ELF II Memory & ADC Board* sheet 1.

## Memory interface (actual DIP-28 62256 pin numbers)

The 1802 drives its high address byte on MA0–MA7 during the first address phase. Capture it into U1 on the **falling edge of TPA** using positive-edge 74HCT273 CLK driven by inverted TPA. The low-byte MA0–MA7 then connect directly to SRAM A0–A7; latched outputs supply SRAM A8–A14 and select bit A15.

### Proposed devices
| Ref | Device | Purpose |
|---|---|---|
| U1 | 74HCT273 DIP-20 | 8-bit high address latch, use inverted TPA |
| U2 | CY62256-compatible 32Kx8 DIP-28 | SRAM |
| U3 | 74HCT04 DIP-14 | Invert TPA and card enable |
| U4 | 74HCT86 DIP-14 | XOR latched A15 with region select |
| U5 | 74HCT32 DIP-14 | Three OR gates for CE/OE/WE |
| JP1 | 3-pin header | REGION: GND=LOW 32K, +5V=HIGH 32K |
| JP2 | 2-pin header | Card enable (shunt to +5V); R1 pulls ENABLE low |
| R1 | 10k | ENABLE pulldown, card disabled with shunt removed |
| R2 | 10k | REGION pulldown, LOW default if shunt removed |
| C1–C5 | 0.1uF | One near each IC |

74HCT family is chosen to ease TTL-compatible logic levels while using CMOS RAM; confirm real parts' propagation and setup/hold at ~1.79 MHz CPU clock. Use +5V power only.

## Memory selection

Define:
- A15 = U1.Q7, latched.
- REGION = 0 for 0000–7FFF, 1 for 8000–FFFF.
- ENABLE = 0 unless JP2 fitted.
- MISMATCH = A15 XOR REGION.
- nCE = MISMATCH OR NOT(ENABLE).
- nOE = nCE OR nMRD.
- nWE = nCE OR nMWR.

| ENABLE | A15 == REGION | nMRD | nMWR | nCE | nOE | nWE | Meaning |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 0 | any | any | any | 1 | 1 | 1 | disabled |
| 1 | 0 | any | any | 1 | 1 | 1 | other half |
| 1 | 1 | 0 | 1 | 0 | 0 | 1 | read |
| 1 | 1 | 1 | 0 | 0 | 1 | 0 | write |
| 1 | 1 | 1 | 1 | 0 | 1 | 1 | idle |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 | invalid simult. read/write (not expected; requires check) |

A disabled SRAM is not allowed to drive the data bus. On reset, the latch output is initialized by /MR tied high (or controllably reset if timing evidence warrants it); card disabled can still protect against undefined address until first TPA.

## Pin-accurate wiring targets

### U1 74HCT273 (DIP20)
- D0 3 <- bus MA0 pad64; Q0 2 -> SRAM A8 pin25.
- D1 4 <- MA1 pad60; Q1 5 -> SRAM A9 pin24.
- D2 7 <- MA2 pad56; Q2 6 -> SRAM A10 pin21.
- D3 8 <- MA3 pad52; Q3 9 -> SRAM A11 pin23.
- D4 13 <- MA4 pad48; Q4 12 -> SRAM A12 pin2.
- D5 14 <- MA5 pad44; Q5 15 -> SRAM A13 pin26.
- D6 17 <- MA6 pad40; Q6 16 -> SRAM A14 pin1.
- D7 18 <- MA7 pad36; Q7 19 -> A15 select logic.
- CLK 11 <- inverted TPA from U3 pin2; /MR pin1 -> +5V; VCC 20 / GND 10.

### U2 62256 DIP28
- A0 pin10 <- bus MA0 pad64; A1 pin9 <- MA1 pad60; A2 pin8 <- MA2 pad56; A3 pin7 <- MA3 pad52.
- A4 pin6 <- MA4 pad48; A5 pin5 <- MA5 pad44; A6 pin4 <- MA6 pad40; A7 pin3 <- MA7 pad36.
- A8 pin25, A9 pin24, A10 pin21, A11 pin23, A12 pin2, A13 pin26, A14 pin1 <- corresponding U1 outputs.
- D0 pin11 <- bus pad62; D1 pin12 <- pad58; D2 pin13 <- pad54; D3 pin15 <- pad50.
- D4 pin16 <- pad46; D5 pin17 <- pad42; D6 pin18 <- pad38; D7 pin19 <- pad34.
- /CE pin20 <- nCE; /OE pin22 <- nOE; /WE pin27 <- nWE; VCC 28 / GND 14.

### U3 74HCT04 DIP14
- Invert TPA: input pin1 <- pad28; output pin2 -> U1 CLK pin11.
- Invert enable: input pin3 <- ENABLE; output pin4 -> U5 pin2.
- Unused inputs pins5,9,11,13 to GND; unused outputs pins6,8,10,12 NC. Power pins14,7.

### U4 74HCT86 DIP14
- XOR: pin1 <- latched A15, pin2 <- REGION; output pin3 -> U5 pin1.
- Tie unused inputs (4,5,9,10,12,13) to GND; outputs (6,8,11) NC. Power pins14,7.

### U5 74HCT32 DIP14
- CE OR: inputs 1=MISMATCH, 2=NOT_ENABLE; output3 = nCE.
- OE OR: inputs 4=nCE,5=nMRD bus pad30; output6=nOE.
- WE OR: inputs 9=nCE,10=nMWR bus pad24; output8=nWE.
- Tie unused inputs 12,13 to GND; output11 NC. Power pins14,7.

## Important open checks
1. Verify whether inverted-TPA transition is the correct high-address capture edge **at the connector** on the early-motherboard revision. The supplied Memory & ADC schematic shows a TPA inverter on the latch clock, but propagation timing must be confirmed.
2. Resolve motherboard 2101 low-RAM contention before using LOW. For the current restored motherboard the 2101 chips were reported removed; verify their actual status before testing.
3. Verify Giant Board ROM space and other memory decode prior to using HIGH.
4. Verify which physical connector fingers are dedicated MA vs data, and cross-check first-to-last pad orientation against original manual.
5. Decide what behavior is required for anomalous simultaneous /MRD and /MWR assertion and during initial power-up, and whether extra qualification is needed.
6. No claims of safe fabrication are made until a real KiCad ERC/DRC and hardware review.
