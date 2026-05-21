"""Unit registry — meters_per_unit hub (1 meter = 3.28084 feet, 1 meter = 1.09361 yard)."""

from __future__ import annotations

from entity.errors import DomainError

# factors: units per 1 meter (1 meter = 3.28084 feet; 1 meter = 1.09361 yard)
DEFAULT_METERS_PER_UNIT: dict[str, float] = {
    "meter": 1.0,
    "feet": 3.28084,
    "yard": 1.09361,
}


class UnitRegistry:
    """Maps unit_id to meters_per_unit (positive finite)."""

    def __init__(self, units: dict[str, float] | None = None) -> None:
        self._units: dict[str, float] = dict(units or DEFAULT_METERS_PER_UNIT)

    def get_meters_per_unit(self, unit_id: str) -> float:
        if unit_id not in self._units:
            raise DomainError("UNKNOWN_UNIT", f"Unknown unit: {unit_id}")
        return self._units[unit_id]

    def register(self, unit_id: str, meters_per_unit: float) -> None:
        if unit_id in self._units:
            raise DomainError("DUPLICATE_UNIT", f"Duplicate unit: {unit_id}")
        if not (meters_per_unit > 0) or meters_per_unit != meters_per_unit:
            raise DomainError("INVALID_RATIO", f"Invalid ratio: {meters_per_unit}")
        self._units[unit_id] = meters_per_unit

    def register_from_ref(self, unit_id: str, ratio: float, ref_unit: str) -> None:
        """1 unit_id = ratio ref_unit → factor via meter hub."""
        ref_factor = self.get_meters_per_unit(ref_unit)
        # 1 new = ratio ref; ref per meter = ref_factor → new per meter = ref_factor / ratio
        self.register(unit_id, ref_factor / ratio)

    def unit_ids(self) -> list[str]:
        return list(self._units.keys())

    def all_meters_per_unit(self) -> dict[str, float]:
        return dict(self._units)
