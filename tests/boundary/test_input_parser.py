"""RED: CliInputParser input validation (PRD F-02, US-01, M-04)."""

from __future__ import annotations

import pytest

from boundary.cli_input_parser import CliInputParser, InputValidationError
from entity.unit_registry import UnitRegistry
@pytest.fixture
def parser(default_registry: UnitRegistry) -> CliInputParser:
    return CliInputParser(registry=default_registry)


def test_parse_without_colon_raises_malformed_input(parser: CliInputParser) -> None:
    with pytest.raises(InputValidationError) as exc_info:
        parser.parse("meter")

    assert exc_info.value.code == "MALFORMED_INPUT"


def test_parse_non_numeric_amount_raises_non_numeric(parser: CliInputParser) -> None:
    with pytest.raises(InputValidationError) as exc_info:
        parser.parse("meter:2.5.3")

    assert exc_info.value.code == "NON_NUMERIC"


def test_parse_negative_amount_raises_negative_value(parser: CliInputParser) -> None:
    with pytest.raises(InputValidationError) as exc_info:
        parser.parse("meter:-1")

    assert exc_info.value.code == "NEGATIVE_VALUE"


def test_parse_unknown_unit_raises_unknown_unit(parser: CliInputParser) -> None:
    with pytest.raises(InputValidationError) as exc_info:
        parser.parse("cubit:1")

    assert exc_info.value.code == "UNKNOWN_UNIT"


def test_parse_input_257_chars_raises_input_too_long(parser: CliInputParser) -> None:
    line = "meter:" + ("0" * 252)

    with pytest.raises(InputValidationError) as exc_info:
        parser.parse(line)

    assert exc_info.value.code == "INPUT_TOO_LONG"
    assert len(line) >= 257
