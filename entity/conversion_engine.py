"""Conversion engine — meter hub only (no feet↔yard direct constants)."""

from __future__ import annotations

from dataclasses import dataclass

from entity.errors import DomainError
from entity.unit_registry import UnitRegistry

# 1 meter = 3.28084 feet; 1 meter = 1.09361 yard (via registry)


@dataclass(frozen=True)
class ConversionResult:
    source_unit: str
    source_amount: float
    target_unit: str
    target_amount: float


class ConversionEngine:
    """Converts amounts using registry meters_per_unit only."""

    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    @staticmethod
    def _validate_amount(amount: float) -> None:
        if amount != amount or amount in (float("inf"), float("-inf")):
            raise DomainError("NON_FINITE_VALUE", "Value must be finite")
        if amount < 0:
            raise DomainError("NEGATIVE_VALUE", f"Value must be non-negative: {amount}")

    def convert(self, source_unit: str, amount: float, target_unit: str) -> float:
        """
        Hub via meter: amount_in_meter = amount / factor(source);
        target = amount_in_meter * factor(target).
        factor(feet)=3.28084 means 1 meter = 3.28084 feet; factor(meter)=1.0.
        """
        self._validate_amount(amount)
        factor_src = self._registry.get_meters_per_unit(source_unit)
        factor_tgt = self._registry.get_meters_per_unit(target_unit)
        amount_in_meter = amount / factor_src
        return amount_in_meter * factor_tgt

    def convert_all(
        self,
        source_unit: str,
        amount: float | None = None,
        *,
        source_amount: float | None = None,
    ) -> list[ConversionResult]:
        value = source_amount if source_amount is not None else amount
        if value is None:
            raise TypeError("convert_all requires amount or source_amount")
        self._validate_amount(value)
        self._registry.get_meters_per_unit(source_unit)
        results: list[ConversionResult] = []
        for target_unit in self._registry.unit_ids():
            target_amount = self.convert(source_unit, value, target_unit)
            results.append(
                ConversionResult(
                    source_unit=source_unit,
                    source_amount=value,
                    target_unit=target_unit,
                    target_amount=target_amount,
                )
            )
        return results
