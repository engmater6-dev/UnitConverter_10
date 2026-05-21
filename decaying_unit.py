"""Bonus feature — dynamic unit registration via module-level OCP registry."""

from __future__ import annotations

import math

from entity.conversion_engine import ConversionEngine
from entity.errors import DomainError
from entity.unit_registry import UnitRegistry

_registry = UnitRegistry()
_engine = ConversionEngine(_registry)


def registerUnit(unit_id: str, ratio: float) -> None:
    """Register a custom unit: 1 unit_id = ratio meter. Ratio must be > 0."""
    if not isinstance(ratio, (int, float)) or ratio <= 0 or ratio != ratio:
        raise ValueError(f"Ratio must be positive: {ratio}")
    expected_factor = 1.0 / ratio
    try:
        _registry.register_from_ref(unit_id, ratio, "meter")
    except DomainError as exc:
        if exc.code == "DUPLICATE_UNIT" and math.isclose(
            _registry.get_meters_per_unit(unit_id), expected_factor, rel_tol=0.0, abs_tol=1e-12
        ):
            return
        raise ValueError(str(exc)) from exc


def convert(source_unit: str, amount: float, target_unit: str) -> float:
    """Convert amount between units via meter hub. Signature must not change."""
    return _engine.convert(source_unit, amount, target_unit)


def convertAll(source_unit: str, amount: float) -> dict[str, float]:
    """Convert to all registered units; returns target_unit -> amount."""
    rows = _engine.convert_all(source_unit, amount)
    return {row.target_unit: row.target_amount for row in rows}
