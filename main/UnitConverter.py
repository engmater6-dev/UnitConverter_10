"""Legacy CLI entry — delegates to BCE boundary layer (no inline conversion)."""

from __future__ import annotations

from boundary.cli_driver import run_cli


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()
