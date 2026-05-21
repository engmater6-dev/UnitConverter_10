"""Parse CLI input lines."""

from __future__ import annotations

import re
from dataclasses import dataclass

from boundary import error_codes as ec
from entity.errors import DomainError
from entity.unit_registry import UnitRegistry

_UNIT_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,31}$")
_MAX_INPUT_LEN = 256


class InputValidationError(ValueError):
    """Boundary input validation — carries PRD error code (F-02)."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class ConvertCommand:
    unit_id: str
    amount: float


@dataclass(frozen=True)
class RegisterCommand:
    unit_id: str
    ratio: float
    ref_unit: str


class CliInputParser:
    def __init__(self, registry: UnitRegistry | None = None) -> None:
        self._registry = registry

    def parse(self, line: str) -> ConvertCommand | RegisterCommand:
        if len(line) > _MAX_INPUT_LEN:
            self._raise_input_error(
                ec.INPUT_TOO_LONG,
                ec.MSG_INPUT_TOO_LONG,
                domain_error=DomainError(ec.INPUT_TOO_LONG, ec.MSG_INPUT_TOO_LONG),
            )
        if line.startswith("register:"):
            return self._parse_register(line)
        return self._parse_convert(line)

    def _raise_input_error(
        self,
        code: str,
        message: str,
        *,
        domain_error: DomainError | None = None,
    ) -> None:
        if self._registry is not None:
            raise InputValidationError(code, message)
        if domain_error is not None:
            raise domain_error
        raise ValueError(message)

    def _parse_convert(self, line: str) -> ConvertCommand:
        if ":" not in line:
            self._raise_input_error(
                ec.MALFORMED_INPUT,
                ec.MSG_MALFORMED_INPUT,
            )
        unit_id, amount_text = line.split(":", 1)
        if not _UNIT_ID_PATTERN.match(unit_id):
            self._raise_input_error(
                ec.INVALID_UNIT_ID,
                ec.message_invalid_unit_id(unit_id),
                domain_error=DomainError(
                    ec.INVALID_UNIT_ID, ec.message_invalid_unit_id(unit_id)
                ),
            )
        try:
            amount = float(amount_text)
        except ValueError as exc:
            self._raise_input_error(
                ec.NON_NUMERIC,
                ec.message_non_numeric(amount_text),
            )
        if amount < 0:
            self._raise_input_error(
                ec.NEGATIVE_VALUE,
                ec.message_negative_value(str(amount)),
            )
        if amount != amount or amount in (float("inf"), float("-inf")):
            self._raise_input_error(
                ec.NON_FINITE_VALUE,
                ec.MSG_NON_FINITE_VALUE,
                domain_error=DomainError(ec.NON_FINITE_VALUE, ec.MSG_NON_FINITE_VALUE),
            )
        if self._registry is not None:
            try:
                self._registry.get_meters_per_unit(unit_id)
            except DomainError as exc:
                if exc.code == "UNKNOWN_UNIT":
                    self._raise_input_error(
                        ec.UNKNOWN_UNIT,
                        ec.message_unknown_unit(unit_id),
                    )
        return ConvertCommand(unit_id=unit_id, amount=amount)

    def _parse_register(self, line: str) -> RegisterCommand:
        body = line[len("register:") :]
        if "=" not in body or body.count(":") < 1:
            self._raise_input_error(
                ec.MALFORMED_INPUT,
                ec.MSG_INVALID_REGISTER_FORMAT,
            )
        left, ref_unit = body.rsplit(":", 1)
        unit_id, ratio_text = left.split("=", 1)
        if not _UNIT_ID_PATTERN.match(unit_id) or not _UNIT_ID_PATTERN.match(ref_unit):
            self._raise_input_error(
                ec.INVALID_UNIT_ID,
                ec.message_invalid_unit_id(unit_id),
                domain_error=DomainError(
                    ec.INVALID_UNIT_ID, ec.message_invalid_unit_id(unit_id)
                ),
            )
        try:
            ratio = float(ratio_text)
        except ValueError as exc:
            self._raise_input_error(
                ec.NON_NUMERIC,
                ec.message_non_numeric(ratio_text),
            )
        return RegisterCommand(unit_id=unit_id, ratio=ratio, ref_unit=ref_unit)
