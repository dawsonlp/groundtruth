"""Unit tests for GroundTruth Logical Tier."""

import pytest
from groundtruth.conceptual.catalog import ConceptualCatalog
from groundtruth.conceptual.models import BusinessTerm
from groundtruth.core.types import DataType
from groundtruth.logical.engine import (
    LogicalSchemaEngine,
    MissingPrimaryKeyError,
    UnmappedConceptualTermError,
)
from groundtruth.logical.entities import LogicalAttribute, LogicalEntity, Relation, RelationshipType
from groundtruth.logical.state_machine import (
    FiniteStateMachine,
    IllegalStateTransitionError,
    StateTransition,
)


def test_define_logical_entity():
    conceptual_catalog = ConceptualCatalog()
    conceptual_catalog.register_term(BusinessTerm(
        slug="customer",
        name="Customer",
        definition="An individual or company purchasing goods.",
    ))

    engine = LogicalSchemaEngine(conceptual_catalog)

    entity = LogicalEntity(
        domain="sales",
        name="Customer",
        conceptual_term_ref="data://conceptual/customer",
        attributes=[
            LogicalAttribute(name="customer_id", data_type=DataType.uuid(), is_primary_key=True),
            LogicalAttribute(name="email", data_type=DataType.string(255), is_nullable=False, is_sensitive=True, tags=["PII"]),
            LogicalAttribute(name="created_at", data_type=DataType.timestamp(), is_nullable=False),
        ],
    )

    defined = engine.define_entity(entity)
    assert defined.uri == "data://logical/sales/Customer"
    assert len(defined.primary_keys) == 1
    assert engine.get_entity("data://logical/sales/Customer") is not None


def test_missing_primary_key_rejection():
    engine = LogicalSchemaEngine()
    entity = LogicalEntity(
        domain="sales",
        name="LogEntry",
        conceptual_term_ref="data://conceptual/log",
        attributes=[
            LogicalAttribute(name="message", data_type=DataType.string()),
        ],
    )

    with pytest.raises(MissingPrimaryKeyError) as exc_info:
        engine.define_entity(entity)
    assert exc_info.value.domain_error_code == "LOGICAL_001"


def test_unmapped_conceptual_term_rejection():
    conceptual_catalog = ConceptualCatalog()
    engine = LogicalSchemaEngine(conceptual_catalog)

    entity = LogicalEntity(
        domain="sales",
        name="Invoice",
        conceptual_term_ref="data://conceptual/non-existent-term",
        attributes=[
            LogicalAttribute(name="id", data_type=DataType.uuid(), is_primary_key=True),
        ],
    )

    with pytest.raises(UnmappedConceptualTermError) as exc_info:
        engine.define_entity(entity)
    assert exc_info.value.domain_error_code == "LOGICAL_002"


def test_finite_state_machine_verification():
    engine = LogicalSchemaEngine()

    fsm = FiniteStateMachine(
        target_entity_uri="data://logical/sales/Order",
        attribute_name="status",
        states=["DRAFT", "PENDING", "PAID", "CANCELLED"],
        initial_state="DRAFT",
        transitions=[
            StateTransition(from_state="DRAFT", to_state="PENDING", trigger_action="Submit"),
            StateTransition(from_state="PENDING", to_state="PAID", trigger_action="Capture Payment"),
            StateTransition(from_state="PENDING", to_state="CANCELLED", trigger_action="Cancel"),
        ],
    )
    engine.register_state_machine(fsm)

    # Valid transition
    assert engine.verify_state_transition("data://logical/sales/Order", "status", "PENDING", "PAID") is True

    # Illegal transition: CANCELLED -> PAID
    with pytest.raises(IllegalStateTransitionError) as exc_info:
        engine.verify_state_transition("data://logical/sales/Order", "status", "CANCELLED", "PAID")
    assert exc_info.value.domain_error_code == "LOGICAL_003"

