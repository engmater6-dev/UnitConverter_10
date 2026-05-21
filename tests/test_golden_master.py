"""Regression — Golden Master (Approval) for UnitConverter stdout."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_UTIL_PATH = Path(__file__).resolve().parent / "golden_master_util.py"
_spec = importlib.util.spec_from_file_location("golden_master_util", _UTIL_PATH)
assert _spec and _spec.loader
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)


def _approve(scenario: str) -> None:
    captured = gm.capture_stdout(scenario)
    try:
        gm.approve_section(scenario, captured, auto_create=True)
    except FileNotFoundError as exc:
        pytest.fail(str(exc))


@pytest.mark.golden_master
def test_golden_master_meter_2_5() -> None:
    """GM-TC-01: meter:2.5 stdout == baseline [meter:2.5] section."""
    _approve("meter:2.5")


@pytest.mark.golden_master
def test_golden_master_feet_1_0() -> None:
    """GM-TC-02: feet:1.0 stdout == baseline [feet:1.0] section."""
    _approve("feet:1.0")


@pytest.mark.golden_master
def test_golden_master_yard_1_0() -> None:
    """GM-TC-03: yard:1.0 stdout == baseline [yard:1.0] section."""
    _approve("yard:1.0")


@pytest.mark.golden_master
def test_golden_master_meter_0_0() -> None:
    """GM-TC-04: meter:0.0 stdout == baseline [meter:0.0] section."""
    _approve("meter:0.0")
