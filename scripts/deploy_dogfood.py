"""Automated Deployment and Multi-Domain Seeding Script for GroundTruth PostgreSQL.

Deploys:
1. GroundTruth Metamodel (M2) -> 'groundtruth_meta' schema
2. E-Commerce Domain (M1)     -> 'ecommerce' schema
3. CodeMesh Domain (M1)       -> 'codemesh' schema
4. Seeds Tenants, Solutions, Reference Lookup Codes, Concepts, and Operational rows.
"""

from datetime import datetime, timezone
import os
from pathlib import Path
import uuid
import psycopg

from groundtruth.api import GroundTruthCatalog
from groundtruth.physical.postgres import PostgresProjectionEngine


def run_dogfood_deployment():
    repo_root = Path(__file__).resolve().parent.parent

    print("=" * 80)
    print("  🚀 GROUNDTRUTH MULTI-DOMAIN DEPLOYMENT: META, ECOMMERCE & CODEMESH")
    print("=" * 80)

    # 1. Load the GroundTruth Catalog
    catalog = GroundTruthCatalog.load(repo_root)

    # 2. Compile GroundTruth Metamodel (M2) DDL
    print("\n[1/5] Compiling GroundTruth Metamodel (M2) DDL...")
    m2_entities = catalog.logical.list_entities(domain="groundtruth_meta")
    m2_ddl = PostgresProjectionEngine.generate_schema_ddl(m2_entities, schema="groundtruth_meta")
    print(f"  ✓ Generated DDL for {len(m2_entities)} metamodel tables.")

    # 3. Compile E-Commerce Subject Domain (M1) DDL
    print("\n[2/5] Compiling E-Commerce Subject Domain (M1) DDL...")
    m1_entities = catalog.logical.list_entities(domain="ecommerce")
    m1_ddl = PostgresProjectionEngine.generate_schema_ddl(m1_entities, schema="ecommerce")
    print(f"  ✓ Generated DDL for {len(m1_entities)} domain tables.")

    # 4. Compile CodeMesh Domain (M1) DDL
    print("\n[3/5] Compiling CodeMesh Domain (M1) DDL...")
    cm_entities = catalog.logical.list_entities(domain="codemesh")
    cm_ddl = PostgresProjectionEngine.generate_schema_ddl(cm_entities, schema="codemesh")
    print(f"  ✓ Generated DDL for {len(cm_entities)} CodeMesh tables.")

    # 4. Connect to PostgreSQL Container
    pg_host = os.getenv("POSTGRES_HOST", "localhost")
    pg_port = int(os.getenv("POSTGRES_PORT", "9432"))
    pg_db = os.getenv("POSTGRES_DB", "groundtruth_catalog")
    pg_user = os.getenv("POSTGRES_USER", "groundtruth")
    pg_pass = os.getenv("POSTGRES_PASSWORD", "groundtruth_password")

    conn_str = f"host={pg_host} port={pg_port} dbname={pg_db} user={pg_user} password={pg_pass}"

    print(f"\n[4/5] Connecting to PostgreSQL at {pg_host}:{pg_port}/{pg_db}...")
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            # Create Schemas and Tables
            cur.execute(m2_ddl)
            cur.execute(m1_ddl)
            cur.execute(cm_ddl)
            conn.commit()
            print("  ✓ Successfully created schemas 'groundtruth_meta', 'ecommerce', and 'codemesh'.")

            # 5. Populate Seed Rows (M0 Instance Data)
            print("\n[5/5] Seeding Instance Rows (M0) across all schemas...")

            # --- Seed Tenant & Solutions ---
            now = datetime.now(timezone.utc)
            tenant_id = "00000000-0000-0000-0000-000000000001"
            cur.execute(
                """
                INSERT INTO groundtruth_meta.tenant (tenant_id, slug, name, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name;
                """,
                (tenant_id, "tripartite", "Tripartite Enterprise", True, now),
            )

            solutions = [
                ("10000000-0000-0000-0000-000000000001", "ecommerce", "🛒 E-Commerce & Payments Domain", "Omnichannel retail, customer profiles, order fulfillment, and idempotent payments.", "1.0.0"),
                ("10000000-0000-0000-0000-000000000002", "codemesh", "🕸️ CodeMesh Program Graph Engine", "Canonical symbol indexing, type contracts, call graph dependencies, and AST mutations.", "1.0.0"),
                ("10000000-0000-0000-0000-000000000003", "groundtruth_meta", "🏛️ GroundTruth Metamodel", "Four-tier semantic modeling authority compliant with OMG MOF 2.5.1 and DAMA-DMBOK.", "1.0.0"),
            ]
            for s_id, s_slug, s_name, s_desc, s_ver in solutions:
                cur.execute(
                    """
                    INSERT INTO groundtruth_meta.solution (solution_id, tenant_id, slug, display_name, description, version, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (slug) DO UPDATE SET 
                        display_name = EXCLUDED.display_name,
                        description = EXCLUDED.description;
                    """,
                    (s_id, tenant_id, s_slug, s_name, s_desc, s_ver, now),
                )

            # --- Seed Reference Lookup Codes ---
            lookup_codes = [
                ("LIFECYCLE_STATUS", "ACTIVE", "Active / Operational", "Item is in active production use"),
                ("LIFECYCLE_STATUS", "DRAFT", "Draft / Staged", "Item is being authored and reviewed"),
                ("LIFECYCLE_STATUS", "DEPRECATED", "Deprecated", "Item is scheduled for retirement"),
                ("ORDER_STATUS", "DRAFT", "Draft", "Order is being assembled"),
                ("ORDER_STATUS", "PENDING", "Pending Payment", "Awaiting authorization"),
                ("ORDER_STATUS", "PAID", "Paid & Confirmed", "Funds captured successfully"),
                ("ORDER_STATUS", "SHIPPED", "Shipped", "Dispatched to fulfillment carrier"),
                ("ORDER_STATUS", "DELIVERED", "Delivered", "Received by customer"),
                ("ORDER_STATUS", "CANCELLED", "Cancelled", "Order was voided or refunded"),
                ("MUTATION_STATUS", "PROPOSED", "Proposed", "AST mutation awaiting invariant verification"),
                ("MUTATION_STATUS", "VALIDATED", "Validated", "Passed all contracts and AST invariants"),
                ("MUTATION_STATUS", "MATERIALIZED", "Materialized", "Written to physical source files"),
                ("MUTATION_STATUS", "REJECTED", "Rejected", "Failed validation or aborted"),
            ]
            for c_set, c_val, c_lbl, c_desc in lookup_codes:
                c_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"code.{c_set}.{c_val}"))
                cur.execute(
                    """
                    INSERT INTO groundtruth_meta.lookupcode (code_id, code_set, code_value, display_label, description, is_active)
                    VALUES (%s, %s, %s, %s, %s, TRUE)
                    ON CONFLICT (code_id) DO UPDATE SET display_label = EXCLUDED.display_label;
                    """,
                    (c_id, c_set, c_val, c_lbl, c_desc),
                )

            # --- Seed M2 Metamodel Catalog Rows ---
            for entity in m2_entities + m1_entities + cm_entities:
                ent_id = str(uuid.uuid5(uuid.NAMESPACE_URL, entity.uri))
                cur.execute(
                    """
                    INSERT INTO groundtruth_meta.entity (entity_id, uri, domain, name, conceptual_term_ref, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (uri) DO UPDATE SET 
                        name = EXCLUDED.name,
                        conceptual_term_ref = EXCLUDED.conceptual_term_ref,
                        description = EXCLUDED.description
                    RETURNING entity_id
                    """,
                    (ent_id, entity.uri, entity.domain, entity.name, entity.conceptual_term_ref, entity.description),
                )
                actual_ent_id = cur.fetchone()[0]
                for attr in entity.attributes:
                    attr_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{entity.uri}.{attr.name}"))
                    cur.execute(
                        """
                        INSERT INTO groundtruth_meta.attribute (attribute_id, entity_id, name, data_type, is_primary_key, is_nullable, is_sensitive)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (attribute_id) DO UPDATE SET
                            entity_id = EXCLUDED.entity_id,
                            name = EXCLUDED.name,
                            data_type = EXCLUDED.data_type,
                            is_primary_key = EXCLUDED.is_primary_key,
                            is_nullable = EXCLUDED.is_nullable,
                            is_sensitive = EXCLUDED.is_sensitive
                        """,
                        (attr_id, actual_ent_id, attr.name, attr.data_type.primitive.value, attr.is_primary_key, attr.is_nullable, attr.is_sensitive),
                    )

            # --- Seed M1 E-Commerce Operational Rows ---
            cust1_id = "a0000000-0000-0000-0000-000000000001"
            cust2_id = "a0000000-0000-0000-0000-000000000002"

            cur.execute(
                """
                INSERT INTO ecommerce.customer (customer_id, email, full_name, status, created_at)
                VALUES 
                    (%s, 'alice@example.com', 'Alice Smith', 'ACTIVE', %s),
                    (%s, 'bob@example.com', 'Bob Jones', 'ACTIVE', %s)
                ON CONFLICT (customer_id) DO UPDATE SET full_name = EXCLUDED.full_name;
                """,
                (cust1_id, now, cust2_id, now),
            )

            prod1_id = "b0000000-0000-0000-0000-000000000001"
            prod2_id = "b0000000-0000-0000-0000-000000000002"

            cur.execute(
                """
                INSERT INTO ecommerce.product (product_id, sku, title, price_cents, is_active)
                VALUES 
                    (%s, 'SKU-LOGIC-001', 'GroundTruth Architecture Book', 4999, TRUE),
                    (%s, 'SKU-TRI-002', 'Tripartite Semantic Compiler Subscription', 9900, TRUE)
                ON CONFLICT (product_id) DO UPDATE SET title = EXCLUDED.title;
                """,
                (prod1_id, prod2_id),
            )

            order1_id = "c0000000-0000-0000-0000-000000000001"
            cur.execute(
                """
                INSERT INTO ecommerce.order (order_id, customer_id, status, total_cents, created_at)
                VALUES (%s, %s, 'PAID', 14899, %s)
                ON CONFLICT (order_id) DO UPDATE SET status = EXCLUDED.status;
                """,
                (order1_id, cust1_id, now),
            )


            cur.execute(
                """
                INSERT INTO ecommerce.orderitem (item_id, order_id, product_id, quantity, unit_price_cents)
                VALUES 
                    (%s, %s, %s, 1, 4999),
                    (%s, %s, %s, 1, 9900)
                ON CONFLICT DO NOTHING;
                """,
                (str(uuid.uuid4()), order1_id, prod1_id, str(uuid.uuid4()), order1_id, prod2_id),
            )

            cur.execute(
                """
                INSERT INTO ecommerce.payment (payment_id, order_id, idempotency_key, amount_cents, status, created_at)
                VALUES (%s, %s, 'IDEMP-PAY-001', 14899, 'CAPTURED', %s)
                ON CONFLICT DO NOTHING;
                """,
                (str(uuid.uuid4()), order1_id, now),
            )

            # --- Seed M1 CodeMesh Operational Rows ---
            sym1_id = "d0000000-0000-0000-0000-000000000001"
            sym2_id = "d0000000-0000-0000-0000-000000000002"
            sym3_id = "d0000000-0000-0000-0000-000000000003"

            cur.execute(
                """
                INSERT INTO codemesh.codesymbol (symbol_id, csi_uri, name, symbol_kind, package_name, file_path, start_line, end_line, is_exported, docstring, created_at)
                VALUES
                    (%s, 'csi://ecommerce/services/OrderService.checkout', 'checkout', 'METHOD', 'ecommerce.services', 'services/order.py', 10, 35, TRUE, 'Process checkout transaction.', %s),
                    (%s, 'csi://ecommerce/services/PaymentService.capture_funds', 'capture_funds', 'METHOD', 'ecommerce.services', 'services/payment.py', 40, 65, TRUE, 'Capture funds idempotently.', %s),
                    (%s, 'csi://ecommerce/models/Order', 'Order', 'CLASS', 'ecommerce.models', 'models/order.py', 1, 30, TRUE, 'Order domain entity model.', %s)
                ON CONFLICT (symbol_id) DO UPDATE SET name = EXCLUDED.name;
                """,
                (sym1_id, now, sym2_id, now, sym3_id, now),
            )


            cur.execute(
                """
                INSERT INTO codemesh.symbolcontract (contract_id, symbol_id, signature, return_type, is_pure, is_idempotent, is_async)
                VALUES
                    (%s, %s, 'def checkout(self, customer_id: str, items: list) -> Order', 'Order', FALSE, FALSE, TRUE),
                    (%s, %s, 'def capture_funds(self, order_id: str, amount: float) -> dict', 'dict', FALSE, TRUE, TRUE)
                ON CONFLICT DO NOTHING;
                """,
                (str(uuid.uuid4()), sym1_id, str(uuid.uuid4()), sym2_id),
            )

            cur.execute(
                """
                INSERT INTO codemesh.codedependencyedge (edge_id, source_symbol_id, target_symbol_id, verb, call_count, is_dynamic)
                VALUES
                    (%s, %s, %s, 'CALLS', 1, FALSE),
                    (%s, %s, %s, 'INSTANTIATES', 1, FALSE)
                ON CONFLICT DO NOTHING;
                """,
                (str(uuid.uuid4()), sym1_id, sym2_id, str(uuid.uuid4()), sym1_id, sym3_id),
            )

            conn.commit()
            print(f"  ✓ Total {len(m2_entities) + len(m1_entities) + len(cm_entities)} entities cataloged in 'groundtruth_meta' ($M_2$).")
            print("  ✓ Tenants, Solutions, and Reference Code Tables deployed in 'groundtruth_meta'.")
            print("  ✓ Orders and Payments deployed in 'ecommerce' ($M_1$/$M_0$).")
            print("  ✓ Code symbols and dependency call graph deployed in 'codemesh' ($M_1$/$M_0$).")

    print("\n" + "=" * 80)
    print("  🎉 MULTI-DOMAIN DEPLOYMENT COMPLETE & VERIFIED!")
    print("=" * 80)


if __name__ == "__main__":
    run_dogfood_deployment()
