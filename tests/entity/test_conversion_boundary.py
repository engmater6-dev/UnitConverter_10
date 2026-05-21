"""경계값 — zero, 큰 수, 소수 정밀도."""

from __future__ import annotations

from tests.helpers import assert_approx


def test_convert_meter_zero_to_feet_returns_zero(engine) -> None:
    # Given: 1 meter = 3.28084 feet, amount = 0
    # When: convert meter 0 → feet
    result = engine.convert("meter", 0.0, "feet")
    # Then: 0
    assert result == 0.0


def test_convert_all_yard_zero_all_targets_zero(engine) -> None:
    # Given: 1 meter = 1.09361 yard
    # When: convert_all yard 0
    results = engine.convert_all("yard", 0.0)
    # Then: every target is 0
    assert all(r.target_amount == 0.0 for r in results)


def test_convert_meter_large_value_1e6_returns_finite(engine) -> None:
    # Given: 1 meter = 3.28084 feet
    # When: convert very large amount 1e6 meter → feet
    result = engine.convert("meter", 1e6, "feet")
    # Then: finite positive (overflow 없음)
    assert result == 3_280_840.0
    assert result < float("inf")


def test_convert_meter_six_decimal_precision(engine) -> None:
    # Given: 1 meter = 3.28084 feet
    # When: convert meter 1.123456 → feet
    result = engine.convert("meter", 1.123456, "feet")
    # Then: 6자리 입력 정밀도 유지 (1.123456 × 3.28084)
    expected = 1.123456 * 3.28084
    assert_approx(result, expected, tol=1e-6)


def test_convert_meter_to_yard_roundtrip_via_meter(engine) -> None:
    # Given: meter hub only
    # When: meter → yard → meter
    yard_amount = engine.convert("meter", 5.0, "yard")
    back = engine.convert("yard", yard_amount, "meter")
    # Then: roundtrip ≈ 5.0
    assert_approx(back, 5.0, tol=1e-5)
