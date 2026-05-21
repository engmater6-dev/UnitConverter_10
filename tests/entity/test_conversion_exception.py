"""예외 — DomainError codes."""

from __future__ import annotations

import pytest

from entity.errors import DomainError


def test_convert_negative_meter_raises_negative_value(engine) -> None:
    # Given: NEG-01 policy
    # When: convert meter -1.0 → feet
    # Then: NEGATIVE_VALUE
    with pytest.raises(DomainError) as exc:
        engine.convert("meter", -1.0, "feet")
    assert exc.value.code == "NEGATIVE_VALUE"


def test_convert_unknown_unit_raises_unknown_unit(engine) -> None:
    # Given: parsec not registered
    # When: convert parsec 1.0 → meter
    with pytest.raises(DomainError) as exc:
        engine.convert("parsec", 1.0, "meter")
    assert exc.value.code == "UNKNOWN_UNIT"


def test_convert_nan_raises_non_finite(engine) -> None:
    # Given: non-finite amount
    # When: convert meter nan → feet
    with pytest.raises(DomainError) as exc:
        engine.convert("meter", float("nan"), "feet")
    assert exc.value.code == "NON_FINITE_VALUE"


def test_convert_inf_raises_non_finite(engine) -> None:
    # Given: infinite amount
    # When: convert meter inf → yard
    with pytest.raises(DomainError) as exc:
        engine.convert("meter", float("inf"), "yard")
    assert exc.value.code == "NON_FINITE_VALUE"


def test_convert_all_negative_raises_before_convert(engine) -> None:
    # Given: negative source amount
    # When: convert_all meter -0.1
    with pytest.raises(DomainError) as exc:
        engine.convert_all("meter", -0.1)
    assert exc.value.code == "NEGATIVE_VALUE"
