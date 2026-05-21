"""Map errors to stderr contract."""

from __future__ import annotations

import sys
from typing import IO, TextIO

from entity.errors import DomainError


class ErrorPresenter:
    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream: TextIO = stream if stream is not None else sys.stderr

    def exit_code(self, error: Exception) -> int:
        if isinstance(error, DomainError) and error.code in (
            "CONFIG_LOAD_FAILED",
            "SCHEMA_INVALID",
            "FILE_NOT_FOUND",
            "PARSE_ERROR",
        ):
            return 2
        return 1

    def present(self, error: Exception | str, **context: str) -> str | int:
        if isinstance(error, str):
            message = self._message_for_code(error, context)
            print(f"code: {error}", file=self._stream)
            print(f"message: {message}", file=self._stream)
            return 1
        return self._present_exception(error)

    def _present_exception(self, error: Exception) -> str:
        if isinstance(error, DomainError):
            return error.args[0] if len(error.args) == 1 else str(error)
        if isinstance(error, ValueError):
            msg = str(error)
            if "Invalid format" in msg:
                return "Invalid format. Use unit:value (ex: meter:2.5)"
            if "Invalid number" in msg:
                return msg
            if "non-negative" in msg:
                return msg
            return msg
        if isinstance(error, TypeError):
            return str(error)
        return str(error)

    @staticmethod
    def _message_for_code(code: str, context: dict[str, str]) -> str:
        if code == "MALFORMED_INPUT":
            return "Invalid format. Use unit:value (ex: meter:2.5)"
        if code == "NON_NUMERIC":
            return f"Invalid number: {context.get('amount_text', '')}"
        if code == "NEGATIVE_VALUE":
            amount_text = context.get("amount_text", "")
            return f"Value must be non-negative: {amount_text}"
        if code == "UNKNOWN_UNIT":
            return f"Unknown unit: {context.get('unit_id', '')}"
        if code == "INPUT_TOO_LONG":
            return "Input exceeds 256 characters"
        return code

    def code_for(self, error: Exception) -> str:
        if isinstance(error, DomainError):
            return error.code
        from boundary.cli_input_parser import InputValidationError

        if isinstance(error, InputValidationError):
            return error.code
        if isinstance(error, ValueError):
            msg = str(error)
            if "Invalid format" in msg:
                return "MALFORMED_INPUT"
            if "Invalid number" in msg:
                return "NON_NUMERIC"
            if "non-negative" in msg:
                return "NEGATIVE_VALUE"
            if "Unknown unit" in msg:
                return "UNKNOWN_UNIT"
        if isinstance(error, TypeError):
            return "MALFORMED_INPUT"
        return "MALFORMED_INPUT"
