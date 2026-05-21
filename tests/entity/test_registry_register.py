"""동적 등록 — registerUnit 후 변환."""

from __future__ import annotations

import pytest

from entity.conversion_engine import ConversionEngine
from entity.errors import DomainError
from entity.unit_registry import UnitRegistry
from tests.helpers import assert_approx


def test_register_cubit_then_convert_to_meter() -> None:
    # Given: 1 cubit = 0.4572 meter
    registry = UnitRegistry()
    registry.register_from_ref("cubit", 0.4572, "meter")
    engine = ConversionEngine(registry)
    # When: convert cubit 10 → meter
    result = engine.convert("cubit", 10.0, "meter")
    # Then: 10 × 0.4572 = 4.572
    assert_approx(result, 4.572, tol=1e-5)


def test_register_cubit_convert_all_includes_cubit() -> None:
    # Given: cubit registered (1 cubit = 0.4572 m)
    registry = UnitRegistry()
    registry.register_from_ref("cubit", 0.4572, "meter")
    engine = ConversionEngine(registry)
    # When: convert_all meter 1.0
    results = engine.convert_all("meter", 1.0)
    # Then: 4 units including cubit
    assert len(results) == 4
    units = {r.target_unit for r in results}
    assert "cubit" in units


def test_register_duplicate_meter_raises_duplicate() -> None:
    # Given: meter already in registry
    registry = UnitRegistry()
    # When: register meter again
    with pytest.raises(DomainError) as exc:
        registry.register("meter", 1.0)
    assert exc.value.code == "DUPLICATE_UNIT"


def test_register_invalid_ratio_zero_raises() -> None:
    # Given: invalid ratio 0
    registry = UnitRegistry()
    with pytest.raises(DomainError) as exc:
        registry.register("bad", 0.0)
    assert exc.value.code == "INVALID_RATIO"


def test_register_unknown_ref_raises_unknown_unit() -> None:
    # Given: ref unit parsec unknown
    registry = UnitRegistry()
    with pytest.raises(DomainError) as exc:
        registry.register_from_ref("cubit", 0.4572, "parsec")
    assert exc.value.code == "UNKNOWN_UNIT"
