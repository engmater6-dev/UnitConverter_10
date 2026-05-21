"""Orchestrate CLI line: parse → register or convert → format (Control Track)."""

from __future__ import annotations

from boundary.cli_input_parser import CliInputParser, ConvertCommand, RegisterCommand
from boundary.error_presenter import ErrorPresenter
from boundary.output_formatter import OutputFormatter
from control.convert_use_case import ConvertUseCase
from control.register_use_case import RegisterUseCase
from entity.errors import DomainError


class RunLineUseCase:
    def __init__(
        self,
        parser: CliInputParser,
        convert: ConvertUseCase,
        register: RegisterUseCase,
        formatter: OutputFormatter,
        errors: ErrorPresenter,
    ) -> None:
        self._parser = parser
        self._convert = convert
        self._register = register
        self._formatter = formatter
        self._errors = errors

    def execute(self, line: str) -> tuple[int, str, str]:
        """Returns (exit_code, stdout, stderr)."""
        try:
            cmd = self._parser.parse(line)
            if isinstance(cmd, RegisterCommand):
                self._register.register_unit(cmd.unit_id, cmd.ratio, cmd.ref_unit)
                return 0, "", ""
            results = self._convert.convert_all(cmd.unit_id, cmd.amount)
            stdout = self._formatter.format_table(results)
            return 0, stdout, ""
        except Exception as exc:
            code = self._errors.code_for(exc)
            message = self._errors.present(exc)
            exit_code = self._errors.exit_code(exc)
            if isinstance(exc, DomainError):
                stderr = f"{code}: {message}"
            else:
                stderr = message
            return exit_code, "", stderr
