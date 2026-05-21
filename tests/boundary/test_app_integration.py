"""Boundary — 앱 통합 (happy path, unknown unit, 표현 계약, zero)."""

from __future__ import annotations

import pytest

from boundary.app import UnitConverterApp
from entity.errors import DomainError
from entity.unit_registry import UnitRegistry
from control.convert_use_case import ConvertUseCase
from boundary.cli_input_parser import CliInputParser


def test_app_meter_2_5_returns_three_line_table() -> None:
    # Given: 1 meter = 3.28084 feet, 1 meter = 1.09361 yard
    app = UnitConverterApp()
    # When: run meter:2.5
    code, stdout, stderr = app.run_line("meter:2.5")
    # Then: happy path table output
    assert code == 0
    assert stderr == ""
    assert "2.5 meter = 8.2 feet" in stdout
    assert "2.5 meter = 2.7 yard" in stdout
    assert "2.5 meter = 2.5 meter" in stdout


def test_app_unknown_parsec_raises_at_convert() -> None:
    # Given: parsec not in registry
    registry = UnitRegistry()
    parser = CliInputParser()
    use_case = ConvertUseCase(registry)
    cmd = parser.parse("parsec:1.0")
    # When: convert_all
    with pytest.raises(DomainError) as exc:
        use_case.convert_all(cmd.unit_id, cmd.amount)
    assert exc.value.code == "UNKNOWN_UNIT"


def test_app_meter_negative_exit_one_no_stdout() -> None:
    # Given: meter:-1.0
    app = UnitConverterApp()
    # When: run
    code, stdout, stderr = app.run_line("meter:-1.0")
    # Then: failure
    assert code == 1
    assert stdout == ""
    assert "non-negative" in stderr


def test_app_output_preserves_lhs_2_5_meter() -> None:
    # Given: expression contract
    app = UnitConverterApp()
    # When: meter:2.5
    _, stdout, _ = app.run_line("meter:2.5")
    # Then: every line starts with 2.5 meter
    for line in stdout.splitlines():
        assert line.startswith("2.5 meter = ")


def test_app_register_cubit_then_convert() -> None:
    # Given: dynamic registration via register: command
    app = UnitConverterApp()
    code_reg, _, stderr_reg = app.run_line("register:cubit=0.4572:meter")
    assert code_reg == 0
    assert stderr_reg == ""
    code, stdout, stderr = app.run_line("cubit:10")
    assert code == 0
    assert stderr == ""
    assert "10 cubit = 4.6 meter" in stdout or "10 cubit = 4.5 meter" in stdout


def test_app_yard_zero_all_targets_zero() -> None:
    # Given: value = 0 boundary
    app = UnitConverterApp()
    # When: yard:0
    code, stdout, _ = app.run_line("yard:0")
    # Then: zeros
    assert code == 0
    assert "0 yard = 0.0 feet" in stdout or "0 yard = 0 feet" in stdout
    assert "0 yard = 0.0 yard" in stdout or "0 yard = 0 yard" in stdout
