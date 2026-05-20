"""Test-only numeric helpers (not production code)."""

from __future__ import annotations

EPS_ABS = 1e-9
EPS_REL = 1e-9

METER_RATIO = 1.0
FEET_RATIO = 3.28084
YARD_RATIO = 1.09361


def assert_close(actual: float, expected: float) -> None:
    """PRD §3.3 EPS: |a-b| <= max(EPS_ABS, EPS_REL * max(|a|, |b|))."""
    tolerance = max(EPS_ABS, EPS_REL * max(abs(actual), abs(expected)))
    assert abs(actual - expected) <= tolerance
