"""Load unit ratios from JSON/YAML files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from data.models import UnitsConfig
from entity.errors import DomainError
from entity.unit_registry import DEFAULT_METERS_PER_UNIT

# 1 meter = 3.28084 feet; 1 meter = 1.09361 yard (defaults when file missing)


class ConfigLoader:
    """Loads meters_per_unit map from config file or defaults."""

    def load(self, path: str | Path | None) -> dict[str, float]:
        if path is None:
            return dict(DEFAULT_METERS_PER_UNIT)
        file_path = Path(path)
        if not file_path.exists():
            return dict(DEFAULT_METERS_PER_UNIT)
        raw = self._read_raw(file_path)
        return self._parse_raw(raw)

    def _read_raw(self, file_path: Path) -> Any:
        text = file_path.read_text(encoding="utf-8")
        suffix = file_path.suffix.lower()
        if suffix in (".yaml", ".yml"):
            try:
                return yaml.safe_load(text)
            except yaml.YAMLError as exc:
                raise DomainError("PARSE_ERROR", str(exc)) from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise DomainError("PARSE_ERROR", str(exc)) from exc

    def _parse_raw(self, raw: Any) -> dict[str, float]:
        try:
            config = UnitsConfig.model_validate(raw)
        except ValidationError as exc:
            raise DomainError("SCHEMA_INVALID", str(exc)) from exc
        units = {entry.id: entry.meters_per_unit for entry in config.units}
        if "meter" not in units:
            raise DomainError("SCHEMA_INVALID", "meter unit required")
        return units


def load_units_config(path: str | Path | None = None) -> dict[str, float]:
    return ConfigLoader().load(path)
