"""Unit tests for GroundTruth Lineage and Governance Tier."""

import pytest
from groundtruth.core.types import DataType
from groundtruth.governance.classifier import (
    PrivacyClassifier,
    UnclassifiedSensitiveDataError,
)
from groundtruth.lineage.graph import LineageGraph, UnknownAttributeError
from groundtruth.logical.entities import LogicalAttribute, LogicalEntity


def test_lineage_graph_traversal():
    graph = LineageGraph()

    # Define lineage: raw_orders.amount -> stg_orders.total -> fct_sales.revenue
    src = "data://logical/raw/orders.amount"
    mid = "data://logical/stg/orders.total"
    dst = "data://logical/analytics/fct_sales.revenue"

    graph.add_lineage(src, mid, transform_name="cast_numeric")
    graph.add_lineage(mid, dst, transform_name="sum_aggregate")

    trace = graph.trace_column(mid)
    assert trace["target_attribute_uri"] == mid
    assert src in trace["upstream_sources"]
    assert dst in trace["downstream_targets"]


def test_lineage_unknown_attribute_rejection():
    graph = LineageGraph()
    with pytest.raises(UnknownAttributeError) as exc_info:
        graph.trace_column("data://logical/unknown/table.col")
    assert exc_info.value.domain_error_code == "LINEAGE_001"


def test_privacy_classification_enforcement():
    entity = LogicalEntity(
        domain="customers",
        name="User",
        conceptual_term_ref="data://conceptual/user",
        attributes=[
            LogicalAttribute(name="id", data_type=DataType.uuid(), is_primary_key=True),
            LogicalAttribute(name="email", data_type=DataType.string(255), is_sensitive=True, tags=["PII"]),
            LogicalAttribute(name="username", data_type=DataType.string(100), tags=["PUBLIC"]),
        ],
    )

    cert = PrivacyClassifier.enforce_privacy_tagging(entity)
    assert cert.is_valid is True
    assert "email" in cert.pii_attributes
    assert "email" in cert.masking_rules


def test_unclassified_sensitive_attribute_rejection():
    entity = LogicalEntity(
        domain="customers",
        name="User",
        conceptual_term_ref="data://conceptual/user",
        attributes=[
            LogicalAttribute(name="id", data_type=DataType.uuid(), is_primary_key=True),
            LogicalAttribute(name="ssn", data_type=DataType.string(11), is_sensitive=True, tags=[]),  # Missing tag!
        ],
    )

    with pytest.raises(UnclassifiedSensitiveDataError) as exc_info:
        PrivacyClassifier.enforce_privacy_tagging(entity)
    assert exc_info.value.domain_error_code == "GOVERNANCE_001"
