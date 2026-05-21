"""Boundary error codes and stderr message templates (PRD F-02, F-05)."""

from __future__ import annotations

# --- Error codes (single source) ---
MALFORMED_INPUT = "MALFORMED_INPUT"
NON_NUMERIC = "NON_NUMERIC"
NEGATIVE_VALUE = "NEGATIVE_VALUE"
UNKNOWN_UNIT = "UNKNOWN_UNIT"
INPUT_TOO_LONG = "INPUT_TOO_LONG"
INVALID_UNIT_ID = "INVALID_UNIT_ID"
NON_FINITE_VALUE = "NON_FINITE_VALUE"
CONFIG_LOAD_FAILED = "CONFIG_LOAD_FAILED"
SCHEMA_INVALID = "SCHEMA_INVALID"
FILE_NOT_FOUND = "FILE_NOT_FOUND"
PARSE_ERROR = "PARSE_ERROR"

EXIT_CODE_2_CODES: frozenset[str] = frozenset(
    {
        CONFIG_LOAD_FAILED,
        SCHEMA_INVALID,
        FILE_NOT_FOUND,
        PARSE_ERROR,
    }
)

# --- Fixed messages ---
MSG_MALFORMED_INPUT = "Invalid format. Use unit:value (ex: meter:2.5)"
MSG_INPUT_TOO_LONG = "Input exceeds 256 characters"
MSG_NON_FINITE_VALUE = "Value must be finite"
MSG_INVALID_REGISTER_FORMAT = "Invalid register format"

# --- ValueError text markers (legacy parse path without InputValidationError) ---
MARKER_INVALID_FORMAT = "Invalid format"
MARKER_INVALID_NUMBER = "Invalid number"
MARKER_NON_NEGATIVE = "non-negative"
MARKER_UNKNOWN_UNIT = "Unknown unit"


def message_non_numeric(amount_text: str) -> str:
    return f"Invalid number: {amount_text}"


def message_negative_value(amount_text: str) -> str:
    return f"Value must be non-negative: {amount_text}"


def message_unknown_unit(unit_id: str) -> str:
    return f"Unknown unit: {unit_id}"


def message_invalid_unit_id(unit_id: str) -> str:
    return f"Invalid unit id: {unit_id}"


def message_for_code(code: str, context: dict[str, str]) -> str:
    """Map PRD error code + context to stderr message body."""
    if code == MALFORMED_INPUT:
        return MSG_MALFORMED_INPUT
    if code == NON_NUMERIC:
        return message_non_numeric(context.get("amount_text", ""))
    if code == NEGATIVE_VALUE:
        return message_negative_value(context.get("amount_text", ""))
    if code == UNKNOWN_UNIT:
        return message_unknown_unit(context.get("unit_id", ""))
    if code == INPUT_TOO_LONG:
        return MSG_INPUT_TOO_LONG
    return code


def code_for_value_error_message(msg: str) -> str:
    """Infer PRD code from ValueError message text."""
    if MARKER_INVALID_FORMAT in msg:
        return MALFORMED_INPUT
    if MARKER_INVALID_NUMBER in msg:
        return NON_NUMERIC
    if MARKER_NON_NEGATIVE in msg:
        return NEGATIVE_VALUE
    if MARKER_UNKNOWN_UNIT in msg:
        return UNKNOWN_UNIT
    return MALFORMED_INPUT


def present_value_error_message(msg: str) -> str:
    """Map ValueError message text to user-facing stderr body."""
    if MARKER_INVALID_FORMAT in msg:
        return MSG_MALFORMED_INPUT
    return msg
