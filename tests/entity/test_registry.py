"""RED: UnitRegistry default ratios and duplicate registration (PRD F-03, M-01)."""

from __future__ import annotations

import pytest

from entity.errors import DomainError
from entity.unit_registry import UnitRegistry
from tests.helpers import FEET_RATIO, METER_RATIO, YARD_RATIO, assert_close


def test_default_registry_registers_meter_feet_yard_ratios(
    default_registry: UnitRegistry,
) -> None:
    """INV-D: Background ratios meter=1.0, feet=3.28084, yard=1.09361."""
    assert_close(default_registry.get_meters_per_unit("meter"), METER_RATIO)
    assert_close(default_registry.get_meters_per_unit("feet"), FEET_RATIO)
    assert_close(default_registry.get_meters_per_unit("yard"), YARD_RATIO)


def test_register_meter_twice_raises_duplicate_unit(
    default_registry: UnitRegistry,
) -> None:
    """F-03: re-registering meter must raise DUPLICATE_UNIT."""
    with pytest.raises(DomainError) as exc_info:
        default_registry.register("meter", METER_RATIO)

    assert exc_info.value.code == "DUPLICATE_UNIT"
