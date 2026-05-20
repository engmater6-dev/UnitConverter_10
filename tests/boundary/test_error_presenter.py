"""RED: ErrorPresenter stderr code/message/exit (PRD F-02, F-05, M-07)."""

from __future__ import annotations

import re
import sys

import pytest

from boundary.error_presenter import ErrorPresenter


@pytest.mark.parametrize(
    ("code", "context", "expected_message"),
    [
        (
            "MALFORMED_INPUT",
            {},
            "Invalid format. Use unit:value (ex: meter:2.5)",
        ),
        (
            "NON_NUMERIC",
            {"amount_text": "2.5.3"},
            "Invalid number: 2.5.3",
        ),
        (
            "NEGATIVE_VALUE",
            {"amount_text": "-1"},
            "Value must be non-negative: -1",
        ),
        (
            "UNKNOWN_UNIT",
            {"unit_id": "cubit"},
            "Unknown unit: cubit",
        ),
        (
            "INPUT_TOO_LONG",
            {},
            "Input exceeds 256 characters",
        ),
    ],
)
def test_present_input_errors_stderr_contract_and_exit_one(
    capsys: pytest.CaptureFixture[str],
    code: str,
    context: dict[str, str],
    expected_message: str,
) -> None:
    presenter = ErrorPresenter(stream=sys.stderr)
    exit_code = presenter.present(code, **context)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert re.search(rf"code:\s*{re.escape(code)}", captured.err)
    assert f"message: {expected_message}" in captured.err
