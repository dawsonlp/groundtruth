"""DAMA-Compliant Logical Entity Schemas and Attribute Models for GroundTruth."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from groundtruth.core.models import DataProvenance, LifecycleState
from groundtruth.core.types import DataType, PrimitiveType


class RelationshipType(str, Enum):
    """Cardinality and relationship types."""
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_ONE = "MANY_TO_ONE"
    MANY_TO_MANY = "MANY_TO_MANY"


@dataclass
class Relation:
    """A relational foreign key association between two logical entities."""
    name: str
    target_entity_uri: str
    source_attribute: str
    target_attribute: str
    relationship_type: RelationshipType = RelationshipType.MANY_TO_ONE
    is_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "target_entity_uri": self.target_entity_uri,
            "source_attribute": self.source_attribute,
            "target_attribute": self.target_attribute,
            "relationship_type": self.relationship_type.value,
            "is_required": self.is_required,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Relation":
        return cls(
            name=data["name"],
            target_entity_uri=data["target_entity_uri"],
            source_attribute=data["source_attribute"],
            target_attribute=data["target_attribute"],
            relationship_type=RelationshipType(data.get("relationship_type", "MANY_TO_ONE")),
            is_required=data.get("is_required", True),
        )


@dataclass
class LogicalAttribute:
    """A typed logical attribute within a DAMA entity schema."""
    name: str
    data_type: DataType
    is_primary_key: bool = False
    is_nullable: bool = True
    is_unique: bool = False
    is_sensitive: bool = False
    tags: List[str] = field(default_factory=list)
    description: str = ""
    conceptual_property_ref: Optional[str] = None
    default_value: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "data_type": self.data_type.to_dict(),
            "is_primary_key": self.is_primary_key,
            "is_nullable": self.is_nullable,
            "is_unique": self.is_unique,
            "is_sensitive": self.is_sensitive,
            "tags": self.tags,
            "description": self.description,
            "conceptual_property_ref": self.conceptual_property_ref,
            "default_value": self.default_value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogicalAttribute":
        return cls(
            name=data["name"],
            data_type=DataType.from_dict(data["data_type"]),
            is_primary_key=data.get("is_primary_key", False),
            is_nullable=data.get("is_nullable", True),
            is_unique=data.get("is_unique", False),
            is_sensitive=data.get("is_sensitive", False),
            tags=data.get("tags", []),
            description=data.get("description", ""),
            conceptual_property_ref=data.get("conceptual_property_ref"),
            default_value=data.get("default_value"),
        )


@dataclass
class LogicalEntity:
    """A DAMA-compliant logical entity definition."""
    domain: str
    name: str
    attributes: List[LogicalAttribute]
    conceptual_term_ref: str
    description: str = ""
    relations: List[Relation] = field(default_factory=list)
    lifecycle: LifecycleState = LifecycleState.ACTIVE
    provenance: DataProvenance = field(default_factory=DataProvenance)

    @property
    def uri(self) -> str:
        return f"data://logical/{self.domain}/{self.name}"

    @property
    def primary_keys(self) -> List[LogicalAttribute]:
        return [a for a in self.attributes if a.is_primary_key]

    def get_attribute(self, name: str) -> Optional[LogicalAttribute]:
        for attr in self.attributes:
            if attr.name.lower() == name.lower():
                return attr
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "domain": self.domain,
            "name": self.name,
            "conceptual_term_ref": self.conceptual_term_ref,
            "description": self.description,
            "attributes": [a.to_dict() for a in self.attributes],
            "relations": [r.to_dict() for r in self.relations],
            "lifecycle": self.lifecycle.value,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogicalEntity":
        return cls(
            domain=data["domain"],
            name=data["name"],
            conceptual_term_ref=data["conceptual_term_ref"],
            description=data.get("description", ""),
            attributes=[LogicalAttribute.from_dict(a) for a in data.get("attributes", [])],
            relations=[Relation.from_dict(r) for r in data.get("relations", [])],
            lifecycle=LifecycleState(data.get("lifecycle", "ACTIVE")),
            provenance=DataProvenance.from_dict(data.get("provenance", {})),
        )
