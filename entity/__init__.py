"""Domain layer — conversion and registry (no I/O)."""

from entity.conversion_engine import ConversionEngine
from entity.errors import DomainError
from entity.unit_registry import UnitRegistry

__all__ = ["ConversionEngine", "DomainError", "UnitRegistry"]
