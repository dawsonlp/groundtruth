"""Automated deployment and dogfooding script for GroundTruth in PostgreSQL."""

import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
import psycopg

# Ensure groundtruth package is importable
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from groundtruth import (
    BusinessTerm,
    DataType,
    FiniteStateMachine,
    GroundTruthCatalog,
    LogicalAttribute,
    LogicalEntity,
    PostgresProjectionEngine,
    Relation,
    StateTransition,
)


def run_dogfood_deployment(
    pg_host: str = "localhost",
    pg_port: int = 9432,
    pg_db: str = "groundtruth_catalog",
    pg_user: str = "groundtruth",
    pg_pass: str = "groundtruth_password",
):
    print("=" * 80)
    print("  🚀 GROUNDTRUTH SELF-DOGFOODING & POSTGRESQL DEPLOYMENT")
    print("=" * 80)

    catalog = GroundTruthCatalog.load(repo_root)

    # Register State Machines
    order_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/ecommerce/Order",
        attribute_name="status",
        states=["DRAFT", "PENDING", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"],
        initial_state="DRAFT",
        transitions=[
            StateTransition("DRAFT", "PENDING", trigger_action="Submit for Payment"),
            StateTransition("PENDING", "PAID", trigger_action="Capture Payment"),
            StateTransition("PENDING", "CANCELLED", trigger_action="Cancel by Customer"),
            StateTransition("PAID", "SHIPPED", trigger_action="Fulfill & Dispatch"),
            StateTransition("SHIPPED", "DELIVERED", trigger_action="Carrier Delivery"),
            StateTransition("PAID", "CANCELLED", trigger_action="Refund & Cancel"),
        ],
    )
    catalog.register_state_machine(order_fsm)

    payment_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/ecommerce/Payment",
        attribute_name="status",
        states=["INITIATED", "AUTHORIZED", "CAPTURED", "REFUNDED", "FAILED"],
        initial_state="INITIATED",
        transitions=[
            StateTransition("INITIATED", "AUTHORIZED", trigger_action="Card Auth Hold"),
            StateTransition("AUTHORIZED", "CAPTURED", trigger_action="Capture Settlement"),
            StateTransition("INITIATED", "FAILED", trigger_action="Decline"),
            StateTransition("CAPTURED", "REFUNDED", trigger_action="Issue Refund"),
        ],
    )
    catalog.register_state_machine(payment_fsm)

    # 1. Compile DDL for Level 1 (M2 Metamodel)
    print("\n[1/4] Compiling Level 1: GroundTruth Metamodel (M2) DDL...")
    m2_entities = catalog.logical.list_entities(domain="groundtruth_meta")
    m2_ddl = PostgresProjectionEngine.generate_schema_ddl(m2_entities, schema="groundtruth_meta")
    print(f"  ✓ Generated DDL for {len(m2_entities)} metamodel tables.")

    # 2. Compile DDL for Level 2 (M1 Domain Models)
    print("\n[2/4] Compiling Level 2: E-Commerce Subject Domain (M1) DDL...")
    m1_entities = catalog.logical.list_entities(domain="ecommerce")
    m1_ddl = PostgresProjectionEngine.generate_schema_ddl(m1_entities, schema="ecommerce")
    print(f"  ✓ Generated DDL for {len(m1_entities)} domain tables.")

    # 3. Connect to PostgreSQL and Deploy Schemas
    conn_str = f"host={pg_host} port={pg_port} dbname={pg_db} user={pg_user} password={pg_pass}"
    print(f"\n[3/4] Connecting to PostgreSQL at {pg_host}:{pg_port}/{pg_db}...")

    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            # Create Schemas & Tables
            cur.execute(m2_ddl)
            cur.execute(m1_ddl)
            conn.commit()
            print("  ✓ Successfully created schemas 'groundtruth_meta' and 'ecommerce'.")

            # 4. Populate Seed Rows (M0 Instance Data)
            print("\n[4/4] Seeding Instance Rows (M0) across both schemas...")

            # --- Seed M2 Metamodel Catalog Rows ---
            for entity in m2_entities + m1_entities:
                ent_id = str(uuid.uuid4())
                cur.execute(
                    """
                    INSERT INTO groundtruth_meta.entity (entity_id, uri, domain, name, conceptual_term_ref, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (uri) DO NOTHING
                    """,
                    (ent_id, entity.uri, entity.domain, entity.name, entity.conceptual_term_ref, entity.description),
                )
                for attr in entity.attributes:
                    cur.execute(
                        """
                        INSERT INTO groundtruth_meta.attribute (attribute_id, entity_id, name, data_type, is_primary_key, is_nullable, is_sensitive)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (str(uuid.uuid4()), ent_id, attr.name, attr.data_type.primitive.value, attr.is_primary_key, attr.is_nullable, attr.is_sensitive),
                    )

            # --- Seed M1 E-Commerce Operational Rows ---
            cust1_id = "a0000000-0000-0000-0000-000000000001"
            cust2_id = "a0000000-0000-0000-0000-000000000002"
            now = datetime.now(timezone.utc)

            cur.execute(
                """
                INSERT INTO ecommerce.customer (customer_id, email, full_name, status, created_at)
                VALUES 
                  (%s, 'alice@tripartite.io', 'Alice Wonderland', 'ACTIVE', %s),
                  (%s, 'bob@tripartite.io', 'Bob Builder', 'ACTIVE', %s)
                ON CONFLICT (email) DO NOTHING
                """,
                (cust1_id, now, cust2_id, now),
            )

            prod1_id = "b0000000-0000-0000-0000-000000000001"
            prod2_id = "b0000000-0000-0000-0000-000000000002"
            cur.execute(
                """
                INSERT INTO ecommerce.product (product_id, sku, title, price_cents, is_active)
                VALUES 
                  (%s, 'SKU-NORTHSTAR-01', 'Northstar Control Plane License', 19900, TRUE),
                  (%s, 'SKU-GROUNDTRUTH-02', 'GroundTruth Data Dictionary Pro', 24900, TRUE)
                ON CONFLICT (sku) DO NOTHING
                """,
                (prod1_id, prod2_id),
            )

            order1_id = "c0000000-0000-0000-0000-000000000001"
            cur.execute(
                """
                INSERT INTO ecommerce.order (order_id, customer_id, status, total_cents, created_at)
                VALUES (%s, %s, 'PAID', 44800, %s)
                ON CONFLICT (order_id) DO NOTHING
                """,
                (order1_id, cust1_id, now),
            )

            cur.execute(
                """
                INSERT INTO ecommerce.orderitem (item_id, order_id, product_id, quantity, unit_price_cents)
                VALUES 
                  (%s, %s, %s, 1, 19900),
                  (%s, %s, %s, 1, 24900)
                ON CONFLICT (item_id) DO NOTHING
                """,
                (str(uuid.uuid4()), order1_id, prod1_id, str(uuid.uuid4()), order1_id, prod2_id),
            )

            cur.execute(
                """
                INSERT INTO ecommerce.payment (payment_id, order_id, idempotency_key, amount_cents, status, created_at)
                VALUES (%s, %s, 'idem_pay_99887711', 44800, 'CAPTURED', %s)
                ON CONFLICT (idempotency_key) DO NOTHING
                """,
                (str(uuid.uuid4()), order1_id, now),
            )

            conn.commit()

            # Query verification counts
            cur.execute("SELECT count(*) FROM groundtruth_meta.entity")
            meta_entities_count = cur.fetchone()[0]

            cur.execute("SELECT count(*) FROM groundtruth_meta.attribute")
            meta_attrs_count = cur.fetchone()[0]

            cur.execute("SELECT count(*) FROM ecommerce.customer")
            cust_count = cur.fetchone()[0]

            cur.execute("SELECT count(*) FROM ecommerce.order")
            order_count = cur.fetchone()[0]

            cur.execute("SELECT count(*) FROM ecommerce.payment")
            payment_count = cur.fetchone()[0]

            print(f"  ✓ Seeded {meta_entities_count} entities and {meta_attrs_count} attributes in 'groundtruth_meta' ($M_2$).")
            print(f"  ✓ Seeded {cust_count} customers, {order_count} orders, and {payment_count} payments in 'ecommerce' ($M_1$/$M_0$).")

    print("\n" + "=" * 80)
    print("  🎉 DEPLOYMENT COMPLETE & DOGFOODING VERIFIED!")
    print("=" * 80)


if __name__ == "__main__":
    run_dogfood_deployment()
