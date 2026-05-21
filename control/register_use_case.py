"""Register unit use case."""

from __future__ import annotations

from entity.unit_registry import UnitRegistry


class RegisterUseCase:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def register_unit(self, unit_id: str, ratio: float, ref_unit: str) -> None:
        self._registry.register_from_ref(unit_id, ratio, ref_unit)
