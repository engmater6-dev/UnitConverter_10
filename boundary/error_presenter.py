"""Map errors to stderr contract."""

from __future__ import annotations

import sys
from typing import TextIO

from boundary import error_codes as ec
from boundary.cli_input_parser import InputValidationError
from entity.errors import DomainError


class ErrorPresenter:
    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream: TextIO = stream if stream is not None else sys.stderr

    def exit_code(self, error: Exception) -> int:
        if isinstance(error, DomainError) and error.code in ec.EXIT_CODE_2_CODES:
            return 2
        return 1

    def present(self, error: Exception | str, **context: str) -> str | int:
        if isinstance(error, str):
            message = ec.message_for_code(error, context)
            print(f"code: {error}", file=self._stream)
            print(f"message: {message}", file=self._stream)
            return 1
        return self._present_exception(error)

    def _present_exception(self, error: Exception) -> str:
        if isinstance(error, DomainError):
            return error.args[0] if len(error.args) == 1 else str(error)
        if isinstance(error, ValueError):
            return ec.present_value_error_message(str(error))
        if isinstance(error, TypeError):
            return str(error)
        return str(error)

    def code_for(self, error: Exception) -> str:
        if isinstance(error, DomainError):
            return error.code
        if isinstance(error, InputValidationError):
            return error.code
        if isinstance(error, ValueError):
            return ec.code_for_value_error_message(str(error))
        if isinstance(error, TypeError):
            return ec.MALFORMED_INPUT
        return ec.MALFORMED_INPUT
