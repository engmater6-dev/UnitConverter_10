"""TRACK A — UI / Boundary RED skeleton."""

import pytest

from boundary.cli_input_parser import CliInputParser


class TestBoundaryRed:
    def test_tc_a_01_meter_2_5_happy_path_returns_conversion(self) -> None:
        pytest.fail("RED")

    def test_tc_a_02_no_colon_raises_value_or_type_error(self) -> None:
        # Given: malformed input without ':'
        # When: parse "meter"
        # Then: ValueError or TypeError
        parser = CliInputParser()
        with pytest.raises((ValueError, TypeError)):
            parser.parse("meter")

    def test_tc_a_03_negative_meter_raises_value_or_type_error(self) -> None:
        # Given: meter:-1.0 violates NEG-01 at parse layer
        # When: parse negative amount
        # Then: ValueError or TypeError
        parser = CliInputParser()
        with pytest.raises((ValueError, TypeError)):
            parser.parse("meter:-1.0")

    def test_tc_a_04_unknown_unit_parsec_raises_value_or_type_error(self) -> None:
        pytest.fail("RED")

    def test_tc_a_05_non_numeric_meter_abc_raises_value_or_type_error(self) -> None:
        pytest.fail("RED")

    def test_tc_a_06_output_preserves_source_unit_and_amount(self) -> None:
        pytest.fail("RED")

    def test_tc_a_07_zero_value_boundary_handling(self) -> None:
        pytest.fail("RED")
