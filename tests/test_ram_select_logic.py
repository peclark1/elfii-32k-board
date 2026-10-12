#!/usr/bin/env python3
"""Truth-table checks for the Hyperboard-derived RAM selection.

The source circuit uses a 74LS151:
- S0/S1/S2 = A12/A13/A14, selecting one 4K page-enable switch.
- An ON switch supplies logic 1; the /Z output therefore asserts low.
- /E is qualified by A15 (LOW 32K) or /A15 (HIGH 32K).

This checks logical intent only; KiCad wiring is covered by test_netlist.py.
"""
from itertools import product


def ram_cs_n(address: int, page_switches: tuple[int, ...], high_half: bool) -> int:
    a15 = (address >> 15) & 1
    selected_half = a15 == int(high_half)
    page = (address >> 12) & 0x7
    enabled_page = bool(page_switches[page])
    return int(not (selected_half and enabled_page))


def run_tests():
    checks = 0

    # Exhaust every A15/page combination and every state of the selected switch.
    for high_half, a15, page, enabled in product((False, True), (0, 1), range(8), (0, 1)):
        switches = [0] * 8
        switches[page] = enabled
        address = (a15 << 15) | (page << 12)
        cs_n = ram_cs_n(address, tuple(switches), high_half)
        expected = int(not ((a15 == int(high_half)) and enabled))
        assert cs_n == expected, (high_half, a15, page, enabled, cs_n, expected)
        checks += 1

    # With all page switches ON, exactly one 32K half responds.
    all_on = (1,) * 8
    for high_half in (False, True):
        for address in range(0, 0x10000, 0x1000):
            selected = not ram_cs_n(address, all_on, high_half)
            assert selected == (((address >> 15) & 1) == int(high_half))
            checks += 1

    # With page 0 OFF and the rest ON, the first 4K page of the chosen half stays Hi-Z.
    page0_off = (0, 1, 1, 1, 1, 1, 1, 1)
    for high_half in (False, True):
        base = 0x8000 if high_half else 0x0000
        assert ram_cs_n(base, page0_off, high_half) == 1
        assert ram_cs_n(base + 0x1000, page0_off, high_half) == 0
        checks += 2

    print(f"PASS: {checks} Hyperboard-derived RAM-select truth-table checks")


if __name__ == "__main__":
    run_tests()
