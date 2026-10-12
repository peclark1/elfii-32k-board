# Original ELF II bus verification before routing

This is the shortest set of **unpowered bench observations** that will resolve the remaining electrical compatibility questions. Record meter observations rather than assuming the Hyperboard connector functions are identical to the user's early original motherboard.

## Safety and setup

- Remove power, disconnect the supply and discharge capacitors before using continuity/ohms mode.
- Remove the new 32K card and Giant Board if necessary to access the contacts and circuits without accidentally bridging the card edge.
- Identify connector contact orientation from the original Netronics diagram and board copper: **connector viewed from component side**. Photograph and number it before touching the meter.
- Do **not** apply voltage or install jumpers on contacts 69 or 82 as a test.
- Record as “open/unknown” where the meter shows semiconductor pathways or changing resistances rather than asserting a true direct connection.

## Primary tests

| Point | Measurement | Why it matters |
| --- | --- | --- |
| J1-1 / J1-2 | Continuity to 5 V distribution (unpowered) | Power feed confirmation |
| J1-5 / J1-80 | Continuity to 0 V ground | Known ground returns |
| J1-69 | Resistance to ground, then trace to original motherboard memory disable/decode network | Netronics original 4K card describes contact 69 as “MOTHER BD. MEMORIES OFF”; Hyperboard labelled GND |
| J1-82 | Continuity to pad 80 and ground | Original and Hyperboard references may differ |
| J1-24 / J1-30 | Continuity to 1802 /MWR and /MRD circuitry | Control-signal orientation and pin numbering |
| J1-28 | Continuity to 1802 TPA | Address latch reference |
| J1-36/40/.../64 | Continuity to multiplexed MA7...MA0 lines | High-byte/low-byte capture |
| J1-34/38/.../62 | Continuity to D7...D0 | Byte order |

## After passive checks

With a scope or logic analyzer, investigate only the verified pins:
- Confirm TPA edge and latched A8–A15 stability across memory cycles.
- Confirm /MRD and /MWR are not asserted together in ordinary operation.
- Characterize bus drive / timing and signal levels with Giant Board present and absent.
- Check whether the native 256-byte RAM drives D0–D7 during overlapping regions.
- Confirm which memory banks the Giant Board actively drives and whether they depend on its jumper positions.

## Recording template

| Measurement | Value or waveform | Test configuration | Notes |
| --- | --- | --- | --- |
| J1-69 to ground (unpowered) | — | ELF II, expansion unplugged | |
| J1-69 to onboard RAM enable | — | ELF II, expansion unplugged | |
| J1-82 to J1-80 | — | ELF II, expansion unplugged | |
| TPA waveform | — | Bare ELF II | |
| Giant Board ROM/RAM ranges | — | ELF II + Giant Board | |

Once these are known, update the KiCad connector assignment and decide whether a jumper-controlled original-RAM-disable feature belongs in the **Rev B** schematic. Keep J1-69 disconnected until verified.

Source for contact 69: `ELF II - 4K Memory Board Schematic.pdf`, sheet 2, “MOTHER BD. MEMORIES OFF / IF USED”.
