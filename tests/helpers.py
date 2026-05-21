"""Test helpers (not production code)."""

from __future__ import annotations

import math

EPS_ABS = 1e-9
EPS_REL = 1e-9

METER_RATIO = 1.0
FEET_RATIO = 3.28084
YARD_RATIO = 1.09361


def assert_close(actual: float, expected: float) -> None:
    """PRD §3.3 EPS: |a-b| <= max(EPS_ABS, EPS_REL * max(|a|, |b|))."""
    tolerance = max(EPS_ABS, EPS_REL * max(abs(actual), abs(expected), 1.0))
    assert abs(actual - expected) <= tolerance


def assert_approx(actual: float, expected: float, tol: float = 1e-5) -> None:
    """PRD EPS with optional tolerance override for README-style checks."""
    delta = max(EPS_ABS, EPS_REL * max(abs(actual), abs(expected), 1.0))
    limit = max(delta, tol)
    assert math.isclose(actual, expected, abs_tol=limit), f"{actual} != {expected}"
