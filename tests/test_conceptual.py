"""Unit tests for GroundTruth Conceptual Tier."""

import pytest
from groundtruth.conceptual.catalog import (
    ConceptualCatalog,
    DuplicateTermError,
    InvalidPropertyConceptError,
)
from groundtruth.conceptual.models import BusinessTerm, PropertyConcept


def test_register_business_term():
    catalog = ConceptualCatalog()

    term = BusinessTerm(
        slug="customer-account",
        name="Customer Account",
        definition="An authoritative entity representing a registered retail customer.",
        domain="sales",
        synonyms=["Client Account", "User Profile"],
    )
    registered = catalog.register_term(term)

    assert registered.slug == "customer-account"
    assert registered.uri == "data://conceptual/customer-account"
    assert catalog.get_term("customer-account") is not None
    assert catalog.get_term("data://conceptual/customer-account") is not None


def test_duplicate_term_rejection():
    catalog = ConceptualCatalog()
    term = BusinessTerm(
        slug="order",
        name="Purchase Order",
        definition="A commercial transaction between buyer and seller.",
    )
    catalog.register_term(term)

    with pytest.raises(DuplicateTermError) as exc_info:
        catalog.register_term(term)
    assert exc_info.value.domain_error_code == "CONCEPTUAL_001"


def test_define_property_concept():
    catalog = ConceptualCatalog()

    prop = PropertyConcept(name="Occurrence Time", domain="conceptual")
    defined = catalog.define_property(prop)

    assert defined.slug == "occurrence-time"
    assert defined.uri == "data://conceptual/properties/occurrence-time"
    assert catalog.get_property("occurrence-time") is not None


def test_invalid_property_concept_rejection():
    catalog = ConceptualCatalog()
    prop = PropertyConcept(name="InvalidConceptNameXYZ", domain="conceptual")

    with pytest.raises(InvalidPropertyConceptError) as exc_info:
        catalog.define_property(prop)
    assert exc_info.value.domain_error_code == "CONCEPTUAL_002"


def test_bind_data_element_concept():
    catalog = ConceptualCatalog()
    term = BusinessTerm(
        slug="payment",
        name="Payment Record",
        definition="A financial monetary exchange transaction.",
    )
    catalog.register_term(term)

    dec = catalog.bind_data_element_concept("payment", "Occurrence Time")
    assert dec.uri == "data://conceptual/payment.occurrence-time"
    assert dec.property_concept_name == "Occurrence Time"
