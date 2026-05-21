"""Map errors to stderr contract."""

from __future__ import annotations

from entity.errors import DomainError


class ErrorPresenter:
    def exit_code(self, error: Exception) -> int:
        if isinstance(error, DomainError) and error.code in (
            "CONFIG_LOAD_FAILED",
            "SCHEMA_INVALID",
            "FILE_NOT_FOUND",
            "PARSE_ERROR",
        ):
            return 2
        return 1

    def present(self, error: Exception) -> str:
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

    def code_for(self, error: Exception) -> str:
        if isinstance(error, DomainError):
            return error.code
        if isinstance(error, ValueError):
            msg = str(error)
            if "Invalid format" in msg:
                return "MALFORMED_INPUT"
            if "Invalid number" in msg:
                return "NON_NUMERIC"
            if "non-negative" in msg:
                return "NEGATIVE_VALUE"
        if isinstance(error, TypeError):
            return "MALFORMED_INPUT"
        return "MALFORMED_INPUT"
