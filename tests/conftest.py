"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from entity.conversion_engine import ConversionEngine
from entity.unit_registry import UnitRegistry
@pytest.fixture
def default_registry() -> UnitRegistry:
    """Background: meter=1.0, feet=3.28084, yard=1.09361 (PRD §3.3)."""
    return UnitRegistry()


@pytest.fixture
def engine(default_registry: UnitRegistry) -> ConversionEngine:
    return ConversionEngine(default_registry)
