"""End-to-End integration tests for GroundTruthCatalog, SQLite adapter, and REST API."""

import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
import pytest

from groundtruth import (
    BusinessTerm,
    DataType,
    FiniteStateMachine,
    GroundTruthCatalog,
    LogicalAttribute,
    LogicalEntity,
    StateTransition,
)
from groundtruth.service.app import create_app


def test_groundtruth_catalog_full_lifecycle():
    with tempfile.TemporaryDirectory() as tmp_dir:
        workspace_root = Path(tmp_dir)
        catalog = GroundTruthCatalog()

        # 1. Register Conceptual Term
        term = BusinessTerm(
            slug="order",
            name="Sales Order",
            definition="An authoritative commercial transaction for purchase of items.",
            domain="sales",
        )
        catalog.register_business_term(term)

        # 2. Define Logical Entity
        entity = LogicalEntity(
            domain="sales",
            name="Order",
            conceptual_term_ref="data://conceptual/order",
            description="Sales order entity.",
            attributes=[
                LogicalAttribute(name="order_id", data_type=DataType.uuid(), is_primary_key=True),
                LogicalAttribute(name="status", data_type=DataType.string(20), is_nullable=False),
                LogicalAttribute(name="customer_email", data_type=DataType.string(255), is_sensitive=True, tags=["PII"]),
            ],
        )
        catalog.define_logical_entity(entity)

        # 3. Register State Machine
        fsm = FiniteStateMachine(
            target_entity_uri="data://logical/sales/Order",
            attribute_name="status",
            states=["DRAFT", "PENDING", "PAID"],
            initial_state="DRAFT",
            transitions=[
                StateTransition(from_state="DRAFT", to_state="PENDING"),
                StateTransition(from_state="PENDING", to_state="PAID"),
            ],
        )
        catalog.register_state_machine(fsm)

        # 4. Verify State Machine
        assert catalog.verify_state_transition("data://logical/sales/Order", "status", "PENDING", "PAID") is True

        # 5. Generate DDL
        ddl = catalog.generate_postgres_ddl("data://logical/sales/Order")
        assert "CREATE TABLE IF NOT EXISTS public.order" in ddl

        # 6. Enforce Privacy
        cert = catalog.enforce_privacy_classification("data://logical/sales/Order")
        assert cert.is_valid is True
        assert "customer_email" in cert.pii_attributes

        # 7. Save to Git YAML files
        catalog.save(workspace_root)
        assert (workspace_root / "models" / "conceptual" / "order.yaml").exists()
        assert (workspace_root / "models" / "logical" / "sales" / "Order.yaml").exists()

        # 8. Reload from Git files
        reloaded = GroundTruthCatalog.load(workspace_root)
        assert reloaded.conceptual.get_term("order") is not None
        assert reloaded.logical.get_entity("data://logical/sales/Order") is not None

        # 9. Save to SQLite
        sqlite_path = workspace_root / ".groundtruth" / "catalog.sqlite3"
        catalog.save_sqlite(sqlite_path)
        assert sqlite_path.exists()


def test_rest_service_endpoints():
    with tempfile.TemporaryDirectory() as tmp_dir:
        app = create_app(tmp_dir)
        client = TestClient(app)

        # Health
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

        # Register Term via API
        term_payload = {
            "slug": "invoice",
            "name": "Invoice",
            "definition": "A commercial bill requesting payment.",
            "domain": "billing",
        }
        res = client.post("/api/v1/terms", json=term_payload)
        assert res.status_code == 200
        assert res.json()["slug"] == "invoice"

