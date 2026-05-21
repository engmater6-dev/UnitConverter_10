"""TRACK B — Domain / Logic RED skeleton."""

import pytest

from tests.helpers import assert_approx


class TestEntityRed:
    def test_tc_b_01_convert_meter_to_feet_within_1e5(self, engine) -> None:
        # Given: 1 meter = 3.28084 feet (PRD §3.3)
        # When: convert meter 2.5 → feet
        result = engine.convert("meter", 2.5, "feet")
        # Then: 2.5 × 3.28084 ≈ 8.20210 (tol 1e-5)
        assert_approx(result, 8.20210, tol=1e-5)

    def test_tc_b_02_convert_meter_to_yard_within_1e5(self) -> None:
        pytest.fail("RED")

    def test_tc_b_03_convert_feet_to_meter_reverse_within_1e5(self) -> None:
        pytest.fail("RED")

    def test_tc_b_04_convert_all_meter_returns_all_registered_units(self) -> None:
        pytest.fail("RED")

    def test_tc_b_05_register_unit_cubit_then_convert_to_meter(self) -> None:
        pytest.fail("RED")

    def test_tc_b_06_load_config_valid_path_applies_ratios(self) -> None:
        pytest.fail("RED")

    def test_tc_b_07_load_config_missing_path_keeps_defaults(self) -> None:
        pytest.fail("RED")
