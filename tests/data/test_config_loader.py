"""설정 로드 — JSON/YAML 정상·실패."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from data.config_loader import ConfigLoader, load_units_config
from entity.errors import DomainError

# 1 meter = 3.28084 feet; 1 meter = 1.09361 yard


def test_load_config_valid_json_returns_ratios(tmp_path: Path) -> None:
    # Given: valid units.json
    config = {
        "schema_version": 1,
        "base_unit": "meter",
        "units": [
            {"id": "meter", "meters_per_unit": 1.0},
            {"id": "feet", "meters_per_unit": 3.28084},
            {"id": "yard", "meters_per_unit": 1.09361},
        ],
    }
    path = tmp_path / "units.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    # When: load
    units = load_units_config(path)
    # Then: ratios match
    assert units["feet"] == 3.28084
    assert units["yard"] == 1.09361


def test_load_config_missing_path_returns_defaults() -> None:
    # Given: missing file path
    # When: load nonexistent
    units = load_units_config(Path("/nonexistent/units.json"))
    # Then: default 3.28084 / 1.09361
    assert units["feet"] == 3.28084
    assert units["yard"] == 1.09361


def test_load_config_invalid_schema_raises_schema_invalid(tmp_path: Path) -> None:
    # Given: wrong schema_version
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"schema_version": 2, "base_unit": "meter", "units": []}))
    loader = ConfigLoader()
    # When / Then
    with pytest.raises(DomainError) as exc:
        loader.load(path)
    assert exc.value.code == "SCHEMA_INVALID"


def test_load_config_valid_yaml_returns_ratios(tmp_path: Path) -> None:
    # Given: YAML config
    data = {
        "schema_version": 1,
        "base_unit": "meter",
        "units": [
            {"id": "meter", "meters_per_unit": 1.0},
            {"id": "feet", "meters_per_unit": 3.28084},
            {"id": "yard", "meters_per_unit": 1.09361},
        ],
    }
    path = tmp_path / "units.yaml"
    path.write_text(yaml.dump(data), encoding="utf-8")
    # When: load
    units = ConfigLoader().load(path)
    # Then
    assert units["feet"] == 3.28084


def test_load_config_invalid_json_raises_parse_error(tmp_path: Path) -> None:
    # Given: broken JSON
    path = tmp_path / "broken.json"
    path.write_text("{ not json", encoding="utf-8")
    loader = ConfigLoader()
    # When / Then
    with pytest.raises(DomainError) as exc:
        loader.load(path)
    assert exc.value.code == "PARSE_ERROR"
