"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from entity.unit_registry import UnitRegistry
from tests.helpers import FEET_RATIO, METER_RATIO, YARD_RATIO


@pytest.fixture
def default_registry() -> UnitRegistry:
    """Background: meter=1.0, feet=3.28084, yard=1.09361 (PRD §3.3)."""
    registry = UnitRegistry()
    registry.register("meter", METER_RATIO)
    registry.register("feet", FEET_RATIO)
    registry.register("yard", YARD_RATIO)
    return registry
