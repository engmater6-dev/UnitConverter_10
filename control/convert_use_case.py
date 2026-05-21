"""Convert use case."""

from __future__ import annotations

from entity.conversion_engine import ConversionEngine, ConversionResult
from entity.unit_registry import UnitRegistry


class ConvertUseCase:
    def __init__(self, registry: UnitRegistry) -> None:
        self._engine = ConversionEngine(registry)

    def convert(
        self, source_unit: str, amount: float, target_unit: str
    ) -> float:
        return self._engine.convert(source_unit, amount, target_unit)

    def convert_all(self, source_unit: str, amount: float) -> list[ConversionResult]:
        return self._engine.convert_all(source_unit, amount)
