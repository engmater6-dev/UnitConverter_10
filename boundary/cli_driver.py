"""CLI I/O adapter — stdin prompt, stdout/stderr, process exit (UI Track only)."""

from __future__ import annotations

import sys

CLI_PROMPT = "Insert value for converting (ex: meter:2.5): "


def emit_run_result(exit_code: int, stdout: str, stderr: str) -> None:
    """Write app run_line result to stdout/stderr and exit the process."""
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    raise SystemExit(exit_code)


def run_cli(
    line: str | None = None,
    *,
    config_path: str | None = None,
) -> None:
    """Read one CLI line (or use `line`), run UnitConverterApp, emit I/O, exit."""
    from boundary.app import UnitConverterApp

    input_line = line if line is not None else input(CLI_PROMPT)
    app = UnitConverterApp(config_path=config_path)
    exit_code, stdout, stderr = app.run_line(input_line)
    emit_run_result(exit_code, stdout, stderr)
