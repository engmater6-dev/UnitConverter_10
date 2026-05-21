"""Boundary — CLI 파싱 예외 (ValueError / TypeError)."""

from __future__ import annotations

import pytest

from boundary.cli_input_parser import CliInputParser, RegisterCommand
from entity.errors import DomainError


@pytest.fixture
def parser() -> CliInputParser:
    return CliInputParser()


def test_parse_meter_2_5_returns_convert_command(parser) -> None:
    # Given: valid input meter:2.5 (1 m = 3.28084 ft)
    # When: parse
    cmd = parser.parse("meter:2.5")
    # Then: unit and amount
    assert cmd.unit_id == "meter"
    assert cmd.amount == 2.5


def test_parse_no_colon_raises_value_error(parser) -> None:
    # Given: malformed input without ':'
    # When: parse "meter"
    # Then: ValueError
    with pytest.raises(ValueError):
        parser.parse("meter")


def test_parse_negative_meter_raises_value_error(parser) -> None:
    # Given: meter:-1.0 violates NEG-01 at parse layer
    # When: parse
    with pytest.raises(ValueError):
        parser.parse("meter:-1.0")


def test_parse_meter_abc_raises_value_error(parser) -> None:
    # Given: non-numeric amount
    # When: parse meter:abc
    with pytest.raises(ValueError, match="Invalid number"):
        parser.parse("meter:abc")


def test_parse_invalid_unit_id_Meter_raises_domain_error(parser) -> None:
    # Given: invalid unit id case
    # When: parse Meter:1
    with pytest.raises(DomainError) as exc:
        parser.parse("Meter:1")
    assert exc.value.code == "INVALID_UNIT_ID"


def test_parse_register_command_returns_register_command(parser) -> None:
    cmd = parser.parse("register:cubit=0.4572:meter")
    assert isinstance(cmd, RegisterCommand)
    assert cmd.unit_id == "cubit"
    assert cmd.ratio == 0.4572
    assert cmd.ref_unit == "meter"


def test_parse_input_too_long_raises_domain_error(parser) -> None:
    # Given: > 256 characters
    # When: parse long line
    with pytest.raises(DomainError) as exc:
        parser.parse("m" * 260 + ":1")
    assert exc.value.code == "INPUT_TOO_LONG"
