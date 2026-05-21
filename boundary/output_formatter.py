"""Format conversion output (table)."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from entity.conversion_engine import ConversionResult


class OutputFormatter:
    def format_table(self, results: list[ConversionResult]) -> str:
        lines = []
        for row in results:
            target_amount = self._round_display(row.target_amount, places=1)
            lines.append(
                f"{row.source_amount} {row.source_unit} = "
                f"{target_amount} {row.target_unit}"
            )
        return "\n".join(lines)

    @staticmethod
    def _round_display(value: float, places: int) -> float:
        quantize = Decimal("1").scaleb(-places)
        return float(Decimal(str(value)).quantize(quantize, rounding=ROUND_HALF_UP))
