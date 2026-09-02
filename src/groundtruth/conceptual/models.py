"""ISO/IEC 11179 & DAMA Conceptual Data Models for GroundTruth."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from groundtruth.core.models import DataProvenance, LifecycleState
from groundtruth.core.uris import DataURI


RECOGNIZED_PROPERTY_CONCEPTS = {
    "Designation": "Intended designations, names, native labels",
    "Definition": "Formal statements of business meaning",
    "Purpose": "Intended purposes and business goals",
    "Scope": "Declared boundaries and coverage",
    "Classification": "Permitted semantic categories, kinds, and classifications",
    "Canonical Reference": "References to governed or external entities",
    "Version Designation": "Version and revision designations",
    "Authority": "Sources of semantic and organizational authority",
    "Lifecycle State": "Permitted lifecycle, state machine, and outcome states",
    "Evidence Fingerprint": "Evidence digests, hashes, and signatures",
    "Occurrence Time": "Points in time associated with events and activities",
    "Rationale": "Explanations, reasoning, and decision context",
    "Native Language": "Languages governing external artifact content",
    "Expression Text": "Statements interpreted by a named language and scope",
    "Lexical Representation": "Target-owned lexical representations of values",
    "Product Designation": "Product and technology designations",
    "Inventory Exception": "Items excluded or not covered by an assessment",
}


@dataclass
class BusinessTerm:
    """An authoritative conceptual business term in the enterprise glossary."""
    slug: str
    name: str
    definition: str
    domain: str = "general"
    synonyms: List[str] = field(default_factory=list)
    lifecycle: LifecycleState = LifecycleState.ACTIVE
    provenance: DataProvenance = field(default_factory=DataProvenance)

    @property
    def uri(self) -> str:
        return f"data://conceptual/{self.slug}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "slug": self.slug,
            "name": self.name,
            "definition": self.definition,
            "domain": self.domain,
            "synonyms": self.synonyms,
            "lifecycle": self.lifecycle.value,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BusinessTerm":
        return cls(
            slug=data["slug"],
            name=data.get("name", data["slug"]),
            definition=data.get("definition", ""),
            domain=data.get("domain", "general"),
            synonyms=data.get("synonyms", []),
            lifecycle=LifecycleState(data.get("lifecycle", "ACTIVE")),
            provenance=DataProvenance.from_dict(data.get("provenance", {})),
        )


@dataclass
class PropertyConcept:
    """A reusable conceptual property category (e.g. Designation, OccurrenceTime, LifecycleState)."""
    name: str
    domain: str = "conceptual"
    description: str = ""
    slug: Optional[str] = None
    provenance: DataProvenance = field(default_factory=DataProvenance)

    def __post_init__(self):
        if not self.slug:
            self.slug = self.name.lower().replace(" ", "-")

    @property
    def uri(self) -> str:
        return f"data://conceptual/properties/{self.slug}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "name": self.name,
            "domain": self.domain,
            "description": self.description or RECOGNIZED_PROPERTY_CONCEPTS.get(self.name, ""),
            "slug": self.slug,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PropertyConcept":
        return cls(
            name=data["name"],
            domain=data.get("domain", "conceptual"),
            description=data.get("description", ""),
            slug=data.get("slug"),
            provenance=DataProvenance.from_dict(data.get("provenance", {})),
        )


@dataclass
class DataElementConcept:
    """An ISO/IEC 11179 Data Element Concept: ObjectClass + PropertyConcept."""
    object_class_slug: str
    property_concept_name: str
    definition: str = ""
    domain: str = "conceptual"

    @property
    def uri(self) -> str:
        prop_slug = self.property_concept_name.lower().replace(" ", "-")
        return f"data://conceptual/{self.object_class_slug}.{prop_slug}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "object_class_slug": self.object_class_slug,
            "property_concept_name": self.property_concept_name,
            "definition": self.definition,
            "domain": self.domain,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataElementConcept":
        return cls(
            object_class_slug=data["object_class_slug"],
            property_concept_name=data["property_concept_name"],
            definition=data.get("definition", ""),
            domain=data.get("domain", "conceptual"),
        )

