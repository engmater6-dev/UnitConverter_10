"""Bonus RED — decaying_unit dynamic registration (implementation forbidden)."""

from __future__ import annotations

import pytest

import decaying_unit
from tests.helpers import assert_approx

CUBIT_RATIO = 0.4572
METER_TO_FEET = 3.28084
EXPECTED_CUBIT_TO_METER = 0.4572
EXPECTED_METER_TO_CUBIT = 1.0 / CUBIT_RATIO
EXPECTED_CUBIT_TO_FEET = CUBIT_RATIO * METER_TO_FEET


def _run_bt_01() -> None:
    decaying_unit.registerUnit("cubit", CUBIT_RATIO)
    result = decaying_unit.convert("cubit", 1.0, "meter")
    assert_approx(result, EXPECTED_CUBIT_TO_METER, tol=1e-5)


def _run_bt_02() -> None:
    decaying_unit.registerUnit("cubit", CUBIT_RATIO)
    result = decaying_unit.convert("meter", 1.0, "cubit")
    assert_approx(result, EXPECTED_METER_TO_CUBIT, tol=1e-5)


def _run_bt_03() -> None:
    decaying_unit.registerUnit("cubit", CUBIT_RATIO)
    result = decaying_unit.convert("cubit", 1.0, "feet")
    assert_approx(result, EXPECTED_CUBIT_TO_FEET, tol=1e-5)


def _run_bt_04() -> None:
    with pytest.raises((ValueError, TypeError)):
        decaying_unit.registerUnit("bad_unit", -1.0)


def _run_bt_05() -> None:
    decaying_unit.registerUnit("cubit", CUBIT_RATIO)
    results = decaying_unit.convertAll("cubit", 1.0)
    assert set(results.keys()) == {"meter", "feet", "yard", "cubit"}
    assert_approx(results["meter"], EXPECTED_CUBIT_TO_METER, tol=1e-5)
    assert_approx(results["cubit"], 1.0, tol=1e-5)
    assert_approx(results["feet"], EXPECTED_CUBIT_TO_FEET, tol=1e-5)


def _run_bt_06() -> None:
    before = decaying_unit.convert("meter", 1.0, "feet")
    assert_approx(before, METER_TO_FEET, tol=1e-5)
    decaying_unit.registerUnit("cubit", CUBIT_RATIO)
    after = decaying_unit.convert("meter", 1.0, "feet")
    assert_approx(after, METER_TO_FEET, tol=1e-5)


_BT_RUNNERS = {
    "BT-01": _run_bt_01,
    "BT-02": _run_bt_02,
    "BT-03": _run_bt_03,
    "BT-04": _run_bt_04,
    "BT-05": _run_bt_05,
    "BT-06": _run_bt_06,
}


@pytest.mark.bonus
@pytest.mark.parametrize("case_id", list(_BT_RUNNERS.keys()))
def test_decaying_unit_conversion(case_id: str) -> None:
    """BT-01~BT-06: registerUnit + convert / convertAll bonus feature."""
    _BT_RUNNERS[case_id]()
