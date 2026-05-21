"""RED: ConversionEngine meter-hub conversion (PRD F-01, F-03, M-02)."""

from __future__ import annotations

import pytest

from entity.conversion_engine import ConversionEngine
from entity.unit_registry import UnitRegistry
from tests.helpers import FEET_RATIO, assert_close


def test_convert_meter_2_5_to_feet_and_yard_raw(default_registry: UnitRegistry) -> None:
    """meter:2.5 → feet≈8.2021, yard≈2.7340 (hub factors, no feet↔yard shortcut)."""
    engine = ConversionEngine(default_registry)
    rows = engine.convert_all(source_unit="meter", source_amount=2.5)
    by_unit = {row.target_unit: row.target_amount for row in rows}

    assert_close(by_unit["feet"], 8.2021)
    assert_close(by_unit["yard"], 2.734025)


def test_convert_feet_1_to_meter_inverse_within_eps(default_registry: UnitRegistry) -> None:
    """feet:1 → meter≈0.3048 reverse conversion within EPS."""
    engine = ConversionEngine(default_registry)
    rows = engine.convert_all(source_unit="feet", source_amount=1.0)
    by_unit = {row.target_unit: row.target_amount for row in rows}

    assert_close(by_unit["meter"], 1.0 / FEET_RATIO)
