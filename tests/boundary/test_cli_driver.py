"""Boundary — CLI driver stdout/stderr/exit contract (UI Track)."""

from __future__ import annotations

import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pytest

from boundary.cli_driver import emit_run_result, run_cli

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MAIN_SCRIPT = _REPO_ROOT / "main" / "UnitConverter.py"


def test_emit_run_result_prints_stdout_and_exits_zero() -> None:
    with pytest.raises(SystemExit) as exc_info:
        with patch("builtins.print") as mock_print:
            emit_run_result(0, "2.5 meter = 8.2 feet", "")
    assert exc_info.value.code == 0
    mock_print.assert_called_once_with("2.5 meter = 8.2 feet")


def test_emit_run_result_prints_stderr_and_exits_one() -> None:
    with pytest.raises(SystemExit) as exc_info:
        with patch("builtins.print") as mock_print:
            emit_run_result(1, "", "Value must be non-negative: -1.0")
    assert exc_info.value.code == 1
    mock_print.assert_called_once()
    _, kwargs = mock_print.call_args
    assert kwargs.get("file") is not None
    assert mock_print.call_args[0][0] == "Value must be non-negative: -1.0"


def test_run_cli_meter_2_5_exit_zero_with_table_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        run_cli("meter:2.5")
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "2.5 meter = 8.2 feet" in captured.out
    assert "2.5 meter = 2.7 yard" in captured.out
    assert "2.5 meter = 2.5 meter" in captured.out


def test_run_cli_meter_negative_exit_one_stderr_no_stdout(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        run_cli("meter:-1.0")
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "non-negative" in captured.err


def test_legacy_main_path_exit_zero_matches_run_cli(capsys: pytest.CaptureFixture[str]) -> None:
    spec = importlib.util.spec_from_file_location("unit_converter_main", _MAIN_SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    buffer = io.StringIO()
    with patch("builtins.input", return_value="meter:2.5"):
        with redirect_stdout(buffer):
            with pytest.raises(SystemExit) as exc_info:
                module.main()
    assert exc_info.value.code == 0
    assert "2.5 meter = 8.2 feet" in buffer.getvalue()
