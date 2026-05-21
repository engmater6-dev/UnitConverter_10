"""Application entry — wire boundary, control, entity."""

from __future__ import annotations

from boundary.cli_input_parser import CliInputParser, ConvertCommand, RegisterCommand
from boundary.error_presenter import ErrorPresenter
from boundary.output_formatter import OutputFormatter
from control.convert_use_case import ConvertUseCase
from control.register_use_case import RegisterUseCase
from data.config_loader import load_units_config
from entity.errors import DomainError
from entity.unit_registry import UnitRegistry


class UnitConverterApp:
    def __init__(self, config_path: str | None = None) -> None:
        units = load_units_config(config_path)
        self._registry = UnitRegistry(units)
        self._parser = CliInputParser()
        self._convert = ConvertUseCase(self._registry)
        self._register = RegisterUseCase(self._registry)
        self._formatter = OutputFormatter()
        self._errors = ErrorPresenter()

    def run_line(self, line: str) -> tuple[int, str, str]:
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


def main() -> None:
    from boundary.cli_driver import run_cli

    run_cli()


if __name__ == "__main__":
    main()
