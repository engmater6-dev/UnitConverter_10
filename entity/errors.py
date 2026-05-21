"""Domain errors with PRD error codes."""

from __future__ import annotations


class DomainError(Exception):
    """Raised when domain rules are violated."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)
