"""Golden Master capture and approve helpers (not production code)."""

from __future__ import annotations

import difflib
import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

_REPO_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_PATH = _REPO_ROOT / "tests" / "golden_master_expected.txt"
_MAIN_SCRIPT = _REPO_ROOT / "main" / "UnitConverter.py"
SCENARIOS: tuple[str, ...] = ("meter:2.5", "feet:1.0", "yard:1.0", "meter:0.0")
SECTION_SEPARATOR = "---"


def capture_stdout_redirect(line: str) -> str:
    """Capture CLI stdout via io.StringIO + contextlib.redirect_stdout."""
    spec = importlib.util.spec_from_file_location("unit_converter_main", _MAIN_SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    buffer = io.StringIO()
    with patch("builtins.input", return_value=line):
        with redirect_stdout(buffer):
            try:
                module.main()
            except SystemExit:
                pass
    return buffer.getvalue().rstrip("\n")


def capture_stdout_subprocess(line: str) -> str:
    """Capture CLI stdout via subprocess.run(capture_output=True)."""
    result = subprocess.run(
        [sys.executable, str(_MAIN_SCRIPT)],
        input=f"{line}\n",
        capture_output=True,
        text=True,
        cwd=str(_REPO_ROOT),
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"subprocess exit {result.returncode}: stderr={result.stderr!r}"
        )
    return result.stdout.rstrip("\n")


def capture_stdout(line: str, *, use_subprocess: bool = False) -> str:
    """Default: redirect_stdout; optional subprocess capture."""
    if use_subprocess:
        return capture_stdout_subprocess(line)
    return capture_stdout_redirect(line)


def parse_sections(text: str) -> dict[str, str]:
    """Parse baseline file into scenario -> output body (lines under [scenario])."""
    sections: dict[str, str] = {}
    for block in text.split(f"\n{SECTION_SEPARATOR}\n"):
        block = block.strip("\n")
        if not block:
            continue
        lines = block.splitlines()
        header = lines[0]
        if not (header.startswith("[") and header.endswith("]")):
            continue
        key = header[1:-1]
        body = "\n".join(lines[1:])
        sections[key] = body
    return sections


def build_golden_blob(capture: str | None = None) -> str:
    """Build full baseline text for all scenarios."""
    capture_fn = capture or capture_stdout
    blocks: list[str] = []
    for scenario in SCENARIOS:
        output = capture_fn(scenario)
        blocks.append(f"[{scenario}]\n{output}")
    return f"\n{SECTION_SEPARATOR}\n".join(blocks) + "\n"


def write_golden_file(path: Path | None = None) -> Path:
    target = path or GOLDEN_PATH
    target.write_text(build_golden_blob(), encoding="utf-8", newline="\n")
    return target


def load_expected_file(path: Path | None = None) -> str:
    """Approve: create baseline if missing, else return file contents."""
    target = path or GOLDEN_PATH
    if not target.is_file():
        write_golden_file(target)
        raise FileNotFoundError(
            f"Golden master created at {target}. "
            "Review the file, then git add and re-run pytest."
        )
    return target.read_text(encoding="utf-8")


def format_diff(expected: str, actual: str) -> str:
    """Unified diff: --- expected / +++ actual / @@ hunk headers @@."""
    lines = difflib.unified_diff(
        expected.splitlines(),
        actual.splitlines(),
        fromfile="expected",
        tofile="actual",
        lineterm="",
    )
    return "\n".join(lines)


def approve_section(
    scenario: str,
    captured: str,
    *,
    expected_path: Path | None = None,
    auto_create: bool = True,
) -> None:
    """
    Compare captured stdout to the [scenario] section in the baseline file.

    Raises FileNotFoundError after auto-create (re-run after review).
    Raises AssertionError with line diff on mismatch.
    """
    path = expected_path or GOLDEN_PATH
    if not path.is_file():
        if not auto_create:
            raise FileNotFoundError(f"Golden master missing: {path}")
        write_golden_file(path)
        raise FileNotFoundError(
            f"Golden master created at {path}. "
            "Review the file, then git add and re-run pytest."
        )

    baseline = path.read_text(encoding="utf-8")
    sections = parse_sections(baseline)
    if scenario not in sections:
        raise KeyError(f"Section [{scenario}] not found in {path}")

    expected = sections[scenario]
    actual = captured.rstrip("\n")
    if expected == actual:
        return

    raise AssertionError(
        f"Golden master mismatch for [{scenario}]:\n{format_diff(expected, actual)}"
    )
