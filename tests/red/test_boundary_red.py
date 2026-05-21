"""TRACK A — UI / Boundary RED skeleton."""

import pytest

from boundary.app import UnitConverterApp
from boundary.cli_input_parser import CliInputParser
from entity.unit_registry import UnitRegistry


class TestBoundaryRed:
    def test_tc_a_01_meter_2_5_happy_path_returns_conversion(self) -> None:
        # Given: 1 meter = 3.28084 feet, 1 meter = 1.09361 yard
        # When: run meter:2.5
        app = UnitConverterApp()
        code, stdout, stderr = app.run_line("meter:2.5")
        # Then: happy path table output
        assert code == 0
        assert stderr == ""
        assert "2.5 meter = 8.2 feet" in stdout
        assert "2.5 meter = 2.7 yard" in stdout
        assert "2.5 meter = 2.5 meter" in stdout

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
        # Given: parsec not in default registry
        # When: parse "parsec:1.0"
        # Then: ValueError or TypeError
        parser = CliInputParser(UnitRegistry())
        with pytest.raises((ValueError, TypeError)):
            parser.parse("parsec:1.0")

    def test_tc_a_05_non_numeric_meter_abc_raises_value_or_type_error(self) -> None:
        # Given: non-numeric amount
        # When: parse meter:abc
        # Then: ValueError or TypeError
        parser = CliInputParser()
        with pytest.raises((ValueError, TypeError)):
            parser.parse("meter:abc")

    def test_tc_a_06_output_preserves_source_unit_and_amount(self) -> None:
        # Given: expression contract — LHS preserves source amount·unit
        # When: meter:2.5
        app = UnitConverterApp()
        _, stdout, _ = app.run_line("meter:2.5")
        # Then: every line starts with 2.5 meter =
        for line in stdout.splitlines():
            assert line.startswith("2.5 meter = ")

    def test_tc_a_07_zero_value_boundary_handling(self) -> None:
        # Given: value = 0 boundary
        # When: yard:0
        app = UnitConverterApp()
        code, stdout, _ = app.run_line("yard:0")
        # Then: all targets zero
        assert code == 0
        for line in stdout.splitlines():
            assert line.startswith("0 yard = ")
            assert "= 0" in line or "= 0.0" in line
