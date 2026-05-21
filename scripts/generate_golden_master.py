#!/usr/bin/env python3
"""
Generate or refresh tests/golden_master_expected.txt from current UnitConverter CLI output.

Capture: io.StringIO + redirect_stdout (default) or --subprocess.

Usage (from repo root):
  python scripts/generate_golden_master.py
  python scripts/generate_golden_master.py --check
  python scripts/generate_golden_master.py --subprocess
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UTIL_PATH = ROOT / "tests" / "golden_master_util.py"
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location("golden_master_util", UTIL_PATH)
assert _spec and _spec.loader
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)


def main() -> int:
    parser = argparse.ArgumentParser(description="Golden Master baseline generator")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=gm.GOLDEN_PATH,
        help="Output path (default: tests/golden_master_expected.txt)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if output would differ from existing baseline (no write)",
    )
    parser.add_argument(
        "--subprocess",
        action="store_true",
        help="Capture via subprocess instead of redirect_stdout",
    )
    args = parser.parse_args()

    def capture(line: str) -> str:
        return gm.capture_stdout(line, use_subprocess=args.subprocess)

    actual = gm.build_golden_blob(capture=capture)

    if args.check:
        if not args.output.is_file():
            print(f"Missing baseline: {args.output}", file=sys.stderr)
            return 1
        expected = args.output.read_text(encoding="utf-8")
        if actual != expected:
            print("Golden master would change; run without --check to refresh.", file=sys.stderr)
            return 1
        print(f"OK: {args.output} matches current output")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(actual, encoding="utf-8", newline="\n")
    print(f"Wrote {args.output}")
    print("Next: git add tests/golden_master_expected.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
