# Early Netronics ELF II compatibility and memory mapping

## Known concerns
- Original early-revision motherboard carries 256 bytes using 2101 RAM and dedicated decoding logic.
- The motherboard's SPST LOAD circuit differs from later SPDT versions; keep board interactions under review.
- Giant Board modifies signals and provides firmware; its installed memory map must be measured/documented.
- The AVI Hyperboard has its own 32K SRAM and 32K ROM: simultaneous population can cause decoding/contention.
- Original Netronics 4K memory schematic, page 4, documents a motherboard RAM isolation modification. **Do not automatically apply this modification** to a restored machine.

## Draft conflict matrix
| System combination | Status |
| --- | --- |
| Bare original ELF II + 32K card | Needs 2101 decode isolation or verified coexistence |
| ELF II + Giant Board + 32K card | Target configuration; exact ROM/RAM range to verify |
| ELF II + Hyperboard + 32K card | Not a rev-A target until memory selection rules verified |
| AVI ELF II reproduction + 32K card | Unverified; onboard SRAM may conflict |

## Decisions before layout
- Which board configuration is the initial hardware target?
- Should LOW and HIGH be mutually exclusive via one 3-position jumper rather than two independent DIP toggles?
- Can the existing low RAM be disabled without permanent board modification?
- Does the Giant Board already provide memory addressing/isolating signals necessary for safe operation?

The design must not drive the data bus outside enabled memory reads. Evaluate all bus loads and startup states with schematic review.
