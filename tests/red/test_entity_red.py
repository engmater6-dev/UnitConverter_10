"""TRACK B — Domain / Logic RED skeleton."""

import pytest

from entity.conversion_engine import ConversionEngine
from entity.unit_registry import UnitRegistry
from tests.helpers import assert_approx


class TestEntityRed:
    def test_tc_b_01_convert_meter_to_feet_within_1e5(self, engine) -> None:
        # Given: 1 meter = 3.28084 feet (PRD §3.3)
        # When: convert meter 2.5 → feet
        result = engine.convert("meter", 2.5, "feet")
        # Then: 2.5 × 3.28084 ≈ 8.20210 (tol 1e-5)
        assert_approx(result, 8.20210, tol=1e-5)

    def test_tc_b_02_convert_meter_to_yard_within_1e5(self, engine) -> None:
        # Given: 1 meter = 1.09361 yard (PRD §3.3)
        # When: convert meter 1.0 → yard
        result = engine.convert("meter", 1.0, "yard")
        # Then: 1.0 × 1.09361 = 1.09361 (tol 1e-5)
        assert_approx(result, 1.09361, tol=1e-5)

    def test_tc_b_03_convert_feet_to_meter_reverse_within_1e5(self, engine) -> None:
        # Given: 1 meter = 3.28084 feet → 1 feet = 1/3.28084 meter
        # When: convert feet 1.0 → meter (역변환)
        result = engine.convert("feet", 1.0, "meter")
        # Then: 1.0 / 3.28084 ≈ 0.30480 (tol 1e-5)
        assert_approx(result, 0.30480, tol=1e-5)

    def test_tc_b_04_convert_all_meter_returns_all_registered_units(self, engine) -> None:
        # Given: registry meter, feet (3.28084), yard (1.09361)
        # When: convert_all meter 1.0
        results = engine.convert_all("meter", 1.0)
        # Then: 3 targets with hub ratios
        assert len(results) == 3
        by_unit = {r.target_unit: r.target_amount for r in results}
        assert_approx(by_unit["feet"], 3.28084, tol=1e-5)
        assert_approx(by_unit["yard"], 1.09361, tol=1e-5)
        assert_approx(by_unit["meter"], 1.0, tol=1e-9)

    def test_tc_b_05_register_unit_cubit_then_convert_to_meter(self) -> None:
        # Given: 1 cubit = 0.4572 meter
        registry = UnitRegistry()
        registry.register_from_ref("cubit", 0.4572, "meter")
        engine = ConversionEngine(registry)
        # When: convert cubit 10 → meter
        result = engine.convert("cubit", 10.0, "meter")
        # Then: 10 × 0.4572 = 4.572
        assert_approx(result, 4.572, tol=1e-5)

    def test_tc_b_06_load_config_valid_path_applies_ratios(self) -> None:
        pytest.fail("RED")

    def test_tc_b_07_load_config_missing_path_keeps_defaults(self) -> None:
        pytest.fail("RED")
