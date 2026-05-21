"""Pydantic models for units configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class UnitEntry(BaseModel):
    id: str
    meters_per_unit: float = Field(gt=0)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not value or not value[0].islower():
            raise ValueError("Invalid unit id")
        return value


class UnitsConfig(BaseModel):
    schema_version: int
    base_unit: str
    units: list[UnitEntry]

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: int) -> int:
        if value != 1:
            raise ValueError("schema_version must be 1")
        return value
