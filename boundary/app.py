"""Application entry — wire boundary, control, entity."""

from __future__ import annotations

from boundary.cli_input_parser import CliInputParser
from boundary.error_presenter import ErrorPresenter
from boundary.output_formatter import OutputFormatter
from control.convert_use_case import ConvertUseCase
from control.register_use_case import RegisterUseCase
from control.run_line_use_case import RunLineUseCase
from data.config_loader import load_units_config
from entity.unit_registry import UnitRegistry


class UnitConverterApp:
    def __init__(self, config_path: str | None = None) -> None:
        units = load_units_config(config_path)
        self._registry = UnitRegistry(units)
        parser = CliInputParser()
        convert = ConvertUseCase(self._registry)
        register = RegisterUseCase(self._registry)
        formatter = OutputFormatter()
        errors = ErrorPresenter()
        self._run_line = RunLineUseCase(parser, convert, register, formatter, errors)

    def run_line(self, line: str) -> tuple[int, str, str]:
        """Returns (exit_code, stdout, stderr)."""
        return self._run_line.execute(line)


def main() -> None:
    from boundary.cli_driver import run_cli

    run_cli()


if __name__ == "__main__":
    main()
