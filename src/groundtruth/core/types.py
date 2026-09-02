"""Canonical data type definitions and physical SQL mappings for GroundTruth."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class PrimitiveType(str, Enum):
    """Canonical abstract primitive data types."""
    STRING = "STRING"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    DECIMAL = "DECIMAL"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    UUID = "UUID"
    JSON = "JSON"
    BINARY = "BINARY"


@dataclass(frozen=True)
class DataType:
    """Represents a typed attribute specification with precision, scale, and constraints."""
    primitive: PrimitiveType
    precision: Optional[int] = None
    scale: Optional[int] = None
    max_length: Optional[int] = None

    def to_postgres_sql(self) -> str:
        """Map abstract primitive to standard PostgreSQL DDL column type."""
        if self.primitive == PrimitiveType.STRING:
            return f"VARCHAR({self.max_length})" if self.max_length else "TEXT"
        elif self.primitive == PrimitiveType.INTEGER:
            return "INTEGER"
        elif self.primitive == PrimitiveType.BIGINT:
            return "BIGINT"
        elif self.primitive == PrimitiveType.DECIMAL:
            if self.precision and self.scale:
                return f"NUMERIC({self.precision}, {self.scale})"
            return "NUMERIC"
        elif self.primitive == PrimitiveType.FLOAT:
            return "DOUBLE PRECISION"
        elif self.primitive == PrimitiveType.BOOLEAN:
            return "BOOLEAN"
        elif self.primitive == PrimitiveType.TIMESTAMP:
            return "TIMESTAMPTZ"
        elif self.primitive == PrimitiveType.DATE:
            return "DATE"
        elif self.primitive == PrimitiveType.UUID:
            return "UUID"
        elif self.primitive == PrimitiveType.JSON:
            return "JSONB"
        elif self.primitive == PrimitiveType.BINARY:
            return "BYTEA"
        return "TEXT"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primitive": self.primitive.value,
            "precision": self.precision,
            "scale": self.scale,
            "max_length": self.max_length,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any] | str) -> "DataType":
        if isinstance(data, str):
            try:
                prim = PrimitiveType(data.upper())
                return cls(primitive=prim)
            except ValueError:
                return cls(primitive=PrimitiveType.STRING)
        return cls(
            primitive=PrimitiveType(data.get("primitive", "STRING").upper()),
            precision=data.get("precision"),
            scale=data.get("scale"),
            max_length=data.get("max_length"),
        )

    # Convenience factories
    @classmethod
    def string(cls, max_length: Optional[int] = None) -> "DataType":
        return cls(primitive=PrimitiveType.STRING, max_length=max_length)

    @classmethod
    def integer(cls) -> "DataType":
        return cls(primitive=PrimitiveType.INTEGER)

    @classmethod
    def bigint(cls) -> "DataType":
        return cls(primitive=PrimitiveType.BIGINT)

    @classmethod
    def decimal(cls, precision: int = 18, scale: int = 4) -> "DataType":
        return cls(primitive=PrimitiveType.DECIMAL, precision=precision, scale=scale)

    @classmethod
    def boolean(cls) -> "DataType":
        return cls(primitive=PrimitiveType.BOOLEAN)

    @classmethod
    def timestamp(cls) -> "DataType":
        return cls(primitive=PrimitiveType.TIMESTAMP)

    @classmethod
    def uuid(cls) -> "DataType":
        return cls(primitive=PrimitiveType.UUID)

    @classmethod
    def json(cls) -> "DataType":
        return cls(primitive=PrimitiveType.JSON)
