"""Parse CLI input lines."""

from __future__ import annotations

import re
from dataclasses import dataclass

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
                "INPUT_TOO_LONG",
                "Input exceeds 256 characters",
                domain_error=DomainError("INPUT_TOO_LONG", "Input exceeds 256 characters"),
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
                "MALFORMED_INPUT",
                "Invalid format. Use unit:value (ex: meter:2.5)",
            )
        unit_id, amount_text = line.split(":", 1)
        if not _UNIT_ID_PATTERN.match(unit_id):
            self._raise_input_error(
                "INVALID_UNIT_ID",
                f"Invalid unit id: {unit_id}",
                domain_error=DomainError("INVALID_UNIT_ID", f"Invalid unit id: {unit_id}"),
            )
        try:
            amount = float(amount_text)
        except ValueError as exc:
            self._raise_input_error(
                "NON_NUMERIC",
                f"Invalid number: {amount_text}",
            )
        if amount < 0:
            self._raise_input_error(
                "NEGATIVE_VALUE",
                f"Value must be non-negative: {amount}",
            )
        if amount != amount or amount in (float("inf"), float("-inf")):
            self._raise_input_error(
                "NON_FINITE_VALUE",
                "Value must be finite",
                domain_error=DomainError("NON_FINITE_VALUE", "Value must be finite"),
            )
        if self._registry is not None:
            try:
                self._registry.get_meters_per_unit(unit_id)
            except DomainError as exc:
                if exc.code == "UNKNOWN_UNIT":
                    self._raise_input_error(
                        "UNKNOWN_UNIT",
                        f"Unknown unit: {unit_id}",
                    )
        return ConvertCommand(unit_id=unit_id, amount=amount)

    def _parse_register(self, line: str) -> RegisterCommand:
        body = line[len("register:") :]
        if "=" not in body or body.count(":") < 1:
            self._raise_input_error(
                "MALFORMED_INPUT",
                "Invalid register format",
            )
        left, ref_unit = body.rsplit(":", 1)
        unit_id, ratio_text = left.split("=", 1)
        if not _UNIT_ID_PATTERN.match(unit_id) or not _UNIT_ID_PATTERN.match(ref_unit):
            self._raise_input_error(
                "INVALID_UNIT_ID",
                f"Invalid unit id: {unit_id}",
                domain_error=DomainError("INVALID_UNIT_ID", f"Invalid unit id: {unit_id}"),
            )
        try:
            ratio = float(ratio_text)
        except ValueError as exc:
            self._raise_input_error(
                "NON_NUMERIC",
                f"Invalid number: {ratio_text}",
            )
        return RegisterCommand(unit_id=unit_id, ratio=ratio, ref_unit=ref_unit)
