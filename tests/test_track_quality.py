#!/usr/bin/env python3
"""Canonical PCB copper-quality regression (revised Hyperboard board).

Previously this file applied obsolete A5 rules (minimum 0.254 mm) and
ignored real KiCad9 multiline segments. The independent geometry and
continuity review now parses complete S-expressions.
"""
from test_routed_board_review import run

if __name__ == "__main__":
    run()
