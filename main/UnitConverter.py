"""Legacy CLI entry — delegates to BCE boundary layer (no inline conversion)."""

from __future__ import annotations

from boundary.app import UnitConverterApp


def main() -> None:
    line = input("Insert value for converting (ex: meter:2.5): ")
    app = UnitConverterApp()
    exit_code, stdout, stderr = app.run_line(line)
    if stdout:
        print(stdout)
    if stderr:
        import sys

        print(stderr, file=sys.stderr)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
