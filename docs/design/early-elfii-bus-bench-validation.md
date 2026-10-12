# Original ELF II bus — remaining compatibility and timing verification

**Slot-5 motherboard RAM disable via contact J1-69 is already established project evidence.** Do not reopen the settled question without conflicting bench evidence. This table covers the outstanding observations. Record meter observations rather than assuming the Hyperboard connector functions are identical to the user's early original motherboard.

## Safety and setup

- Remove power, disconnect the supply and discharge capacitors before using continuity/ohms mode.
- Remove the new 32K card and Giant Board if necessary to access the contacts and circuits without accidentally bridging the card edge.
- Identify connector contact orientation from the original Netronics diagram and board copper: **connector viewed from component side**. Photograph and number it before touching the meter.
- Do not inject power into J1-82. J1-69 is connected to JP2-1, with JP2-2 grounded and the shunt normally open; any later powered test requires the intended known-working Slot-5 configuration.
- Record as “open/unknown” where the meter shows semiconductor pathways or changing resistances rather than asserting a true direct connection.

## Primary tests

| Point | Measurement | Why it matters |
| --- | --- | --- |
| J1-1 / J1-2 | Continuity to 5 V distribution (unpowered) | Power feed confirmation |
| J1-5 / J1-80 | Continuity to 0 V ground | Known ground returns |
| J1-69 | **Previously established Slot-5 motherboard RAM disable** | Implemented on J1-69 → JP2-1, optional JP2-2 GND shunt; no new proof requested |
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
- Verify the intended **system memory map** and contention during overlap (without reopening established J1-69 disabling behavior).
- Confirm which memory banks the Giant Board actively drives and whether they depend on its jumper positions.

## Recording template

| Measurement | Value or waveform | Test configuration | Notes |
| --- | --- | --- | --- |
| JP2 shunt installation state | — | Slot-5 intended configuration | Defaults open; earlier RAM-disable bench evidence accepted |
| J1-82 to J1-80 | — | ELF II, expansion unplugged | |
| TPA waveform | — | Bare ELF II | |
| Giant Board ROM/RAM ranges | — | ELF II + Giant Board | |

J1-69 is **already wired** to the optional JP2 shunt in both schematic and revised PCB. Do not return J1-69 to NC. Keep J1-82 unresolved until independently verified. The remaining gates are physical clearance, timing and coexistence.

Source for contact 69: `ELF II - 4K Memory Board Schematic.pdf`, sheet 2, “MOTHER BD. MEMORIES OFF / IF USED”.
