"""Authoritative Conceptual Business Glossary and Term Catalog for GroundTruth."""

import re
from typing import Any, Dict, List, Optional

from groundtruth.conceptual.models import (
    RECOGNIZED_PROPERTY_CONCEPTS,
    BusinessTerm,
    DataElementConcept,
    PropertyConcept,
)


class DuplicateTermError(Exception):
    """Raised when registering a business term that already exists (CONCEPTUAL_001)."""
    def __init__(self, message: str, term_slug: str):
        super().__init__(message)
        self.term_slug = term_slug
        self.domain_error_code = "CONCEPTUAL_001"


class InvalidPropertyConceptError(Exception):
    """Raised when a property concept does not match recognized categories (CONCEPTUAL_002)."""
    def __init__(self, message: str, property_name: str):
        super().__init__(message)
        self.property_name = property_name
        self.domain_error_code = "CONCEPTUAL_002"


class ConceptualCatalog:
    """In-memory and persisted repository for conceptual terms and property taxonomies."""

    def __init__(self):
        self._terms: Dict[str, BusinessTerm] = {}
        self._properties: Dict[str, PropertyConcept] = {}
        self._data_element_concepts: Dict[str, DataElementConcept] = {}

        # Initialize default property concepts from standard taxonomy
        for prop_name, desc in RECOGNIZED_PROPERTY_CONCEPTS.items():
            self._properties[prop_name.lower().replace(" ", "-")] = PropertyConcept(
                name=prop_name,
                description=desc,
            )

    def register_term(self, term: BusinessTerm) -> BusinessTerm:
        """Register a conceptual business term satisfying req://conceptual/register-business-term."""
        # Precondition 1: Term slug must be lowercase alphanumeric with hyphens/underscores
        if not re.match(r"^[a-z0-9_-]+$", term.slug):
            raise ValueError(f"Term slug '{term.slug}' must be lowercase alphanumeric with hyphens or underscores")

        # Precondition 2: Definition must not be empty (> 10 chars)
        if len(term.definition.strip()) < 10:
            raise ValueError(f"Term definition for '{term.slug}' must be at least 10 characters long")

        # Check for duplication (Failure Mode CONCEPTUAL_001)
        if term.slug in self._terms:
            raise DuplicateTermError(
                f"Business term '{term.slug}' already exists in conceptual catalog",
                term_slug=term.slug,
            )

        self._terms[term.slug] = term
        return term

    def define_property(self, prop: PropertyConcept) -> PropertyConcept:
        """Define a reusable property concept satisfying req://conceptual/define-property-concept."""
        # Precondition 1: Recognized category
        if prop.name not in RECOGNIZED_PROPERTY_CONCEPTS:
            raise InvalidPropertyConceptError(
                f"Property concept '{prop.name}' is not recognized. Allowed: {list(RECOGNIZED_PROPERTY_CONCEPTS.keys())}",
                property_name=prop.name,
            )

        # Precondition 2: Conceptual domain declared
        if not prop.domain or len(prop.domain.strip()) == 0:
            raise ValueError("Conceptual domain must be declared for property concept")

        slug = prop.slug or prop.name.lower().replace(" ", "-")
        self._properties[slug] = prop
        return prop

    def get_term(self, slug_or_uri: str) -> Optional[BusinessTerm]:
        """Retrieve business term by slug or canonical URI."""
        slug = slug_or_uri.replace("data://conceptual/", "").strip("/")
        return self._terms.get(slug)

    def get_property(self, name_or_slug: str) -> Optional[PropertyConcept]:
        """Retrieve property concept by name or slug."""
        slug = name_or_slug.lower().replace(" ", "-").replace("data://conceptual/properties/", "")
        return self._properties.get(slug)

    def bind_data_element_concept(self, object_class_slug: str, property_concept_name: str, definition: str = "") -> DataElementConcept:
        """Create and register an ISO/IEC 11179 Data Element Concept."""
        term = self.get_term(object_class_slug)
        if not term:
            raise ValueError(f"Object class term '{object_class_slug}' not found in conceptual catalog")

        prop = self.get_property(property_concept_name)
        if not prop:
            prop = self.define_property(PropertyConcept(name=property_concept_name))

        dec = DataElementConcept(
            object_class_slug=object_class_slug,
            property_concept_name=prop.name,
            definition=definition or f"{prop.name} of {term.name}",
            domain=term.domain,
        )
        self._data_element_concepts[dec.uri] = dec
        return dec

    def list_terms(self) -> List[BusinessTerm]:
        return list(self._terms.values())

    def list_properties(self) -> List[PropertyConcept]:
        return list(self._properties.values())

