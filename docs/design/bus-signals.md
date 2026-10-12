# Original Netronics ELF II expansion bus — verification worksheet

**Warning:** The previous image-generation mockup invented a 22-pin bus. The original ELF II bus has 86 contacts. We now have the precise physical connector numbering and Hyperboard net labels from its X2 Gerbers (see `../reference/hyperboard-rev2-p3-netlist.md`). It must still be independently checked against the early original Netronics schematic before fabrication.

The original ELF II assembly manual's bus definition (page 13) is the primary period reference. The Popular Electronics ELF II article (page 4, Figure 6) is a useful cross-check. Connector odd/even side convention and viewing orientation must be recorded before assigning pad numbers.

## Required net groups
| Signal | Role | Status |
| --- | --- | --- |
| +5V, GND | power reference | verify exact contacts and current budget |
| MA0–MA7 | CDP1802 multiplexed address | verify pinouts and buffering |
| D0–D7 | bidirectional data | verify bus naming/orientation |
| TPA | high address latch timing | verify edge polarity |
| /MRD | memory read control | verify active level and bus connection |
| /MWR | memory write control | verify active level and bus connection |
| A15 | latched high-order address, **not** independent unlatched bus line | derive from latch |
| /CLEAR, SC0, SC1, N2 | possible control qualifications | verify need |
| CLOCK | possible timing diagnostics | optional, verify |

## CDP1802 address timing
On each memory-address cycle the CDP1802 presents the high address byte on MA0–MA7 for capture at TPA; MA0–MA7 subsequently present the low address byte. The latch outputs supply A8–A15, **not A0–A7**. Review latch timing and use the correct active TPA edge per CDP1802 documentation.

## Required follow-up
- Cross-check the complete numbered 86-contact table extracted from the Hyperboard P3 copper-Gerber metadata with the original ELF II pinout; preserve source and confidence.
- Compare the bus assignment to both the original and the AVI reproduction schematics; ensure early-motherboard revisions are handled.
- Confirm whether signals are available from the expansion connector or require the card to create buffered equivalents.
