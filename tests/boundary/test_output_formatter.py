"""RED: OutputFormatter table contract — LHS preservation, 1dp half-up (PRD F-04, M-06)."""

from __future__ import annotations

from boundary.output_formatter import OutputFormatter
from entity.conversion_engine import ConversionEngine
from entity.unit_registry import UnitRegistry


def _table_lines(registry: UnitRegistry, source_unit: str, source_amount: float) -> list[str]:
    engine = ConversionEngine(registry)
    rows = engine.convert_all(source_unit=source_unit, source_amount=source_amount)
    return OutputFormatter().format_table(
        source_unit=source_unit,
        source_amount=source_amount,
        conversions=rows,
    )


def test_format_meter_2_5_preserves_lhs_and_rounds_targets_half_up(
    default_registry: UnitRegistry,
) -> None:
    """AC-01: meter:2.5 → 8.2 feet, 2.7 yard; LHS always user input."""
    lines = _table_lines(default_registry, "meter", 2.5)
    joined = "\n".join(lines)

    assert "2.5 meter = 8.2 feet" in joined
    assert "2.5 meter = 2.7 yard" in joined
    assert all(line.startswith("2.5 meter = ") for line in lines)
    assert len(lines) == 3


def test_format_feet_3_28084_preserves_lhs_on_every_line(
    default_registry: UnitRegistry,
) -> None:
    """Gherkin #6: feet:3.28084 — LHS 3.28084 feet on all output lines."""
    lines = _table_lines(default_registry, "feet", 3.28084)

    assert len(lines) == 3
    assert all(line.startswith("3.28084 feet = ") for line in lines)
