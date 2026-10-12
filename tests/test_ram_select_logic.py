#!/usr/bin/env python3
"""Truth-table checks for the proposed ELF II 32K RAM select logic.

Pure Python (no external packages). This validates logical expectations,
NOT KiCad wiring, analog bus timing, or physical compatibility.
"""
from itertools import product


def ram_signals(enabled: bool, a15: int, region: int, n_mrd: int, n_mwr: int):
    mismatch = a15 ^ region
    n_ce = mismatch or (not enabled)
    n_oe = n_ce or bool(n_mrd)
    n_we = n_ce or bool(n_mwr)
    return tuple(int(v) for v in (n_ce, n_oe, n_we))


def run_tests():
    count = 0
    for en, a15, region, mrd, mwr in product((0, 1), repeat=5):
        ce, oe, we = ram_signals(bool(en), a15, region, mrd, mwr)
        selected = bool(en and a15 == region)
        assert ce == int(not selected), (en, a15, region, mrd, mwr, ce)
        assert oe == int(not (selected and mrd == 0)), (en, a15, region, mrd, mwr, oe)
        assert we == int(not (selected and mwr == 0)), (en, a15, region, mrd, mwr, we)
        if not en or a15 != region:
            assert (ce, oe, we) == (1, 1, 1)
        count += 1
    print(f"PASS: {count} exhaustive select/read/write combinations")


if __name__ == "__main__":
    run_tests()
