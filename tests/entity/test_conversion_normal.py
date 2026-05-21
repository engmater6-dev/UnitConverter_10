"""정상 변환 — 1 meter = 3.28084 feet, 1 meter = 1.09361 yard."""

from __future__ import annotations

from tests.helpers import assert_approx


def test_convert_meter_to_feet_2_5_returns_8_20210(engine) -> None:
    # Given: 1 meter = 3.28084 feet
    # When: convert meter 2.5 → feet
    result = engine.convert("meter", 2.5, "feet")
    # Then: 2.5 × 3.28084 = 8.2021
    assert_approx(result, 8.20210, tol=1e-5)


def test_convert_meter_to_yard_1_0_returns_1_09361(engine) -> None:
    # Given: 1 meter = 1.09361 yard
    # When: convert meter 1.0 → yard
    result = engine.convert("meter", 1.0, "yard")
    # Then: 1.0 × 1.09361 = 1.09361
    assert_approx(result, 1.09361, tol=1e-5)


def test_convert_feet_to_meter_1_0_returns_0_30480(engine) -> None:
    # Given: 1 meter = 3.28084 feet → 1 feet = 1/3.28084 meter
    # When: convert feet 1.0 → meter (역변환)
    result = engine.convert("feet", 1.0, "meter")
    # Then: 1.0 / 3.28084 ≈ 0.30480
    assert_approx(result, 0.30480, tol=1e-5)


def test_convert_meter_to_meter_2_5_returns_2_5(engine) -> None:
    # Given: 1 meter = 1.0 meter
    # When: convert meter 2.5 → meter
    result = engine.convert("meter", 2.5, "meter")
    # Then: identity
    assert_approx(result, 2.5, tol=1e-9)


def test_convert_all_meter_1_0_returns_three_units(engine) -> None:
    # Given: registry meter, feet (3.28084), yard (1.09361)
    # When: convert_all meter 1.0
    results = engine.convert_all("meter", 1.0)
    # Then: 3 targets with hub ratios
    assert len(results) == 3
    by_unit = {r.target_unit: r.target_amount for r in results}
    assert_approx(by_unit["feet"], 3.28084, tol=1e-5)
    assert_approx(by_unit["yard"], 1.09361, tol=1e-5)
    assert_approx(by_unit["meter"], 1.0, tol=1e-9)
