"""Unit tests for GroundTruth Physical Projection Tier."""

import pytest
from groundtruth.core.types import DataType
from groundtruth.logical.entities import LogicalAttribute, LogicalEntity, Relation
from groundtruth.physical.postgres import PostgresProjectionEngine


def test_postgres_create_table_ddl():
    entity = LogicalEntity(
        domain="sales",
        name="Order",
        conceptual_term_ref="data://conceptual/order",
        description="A customer sales order record.",
        attributes=[
            LogicalAttribute(name="order_id", data_type=DataType.uuid(), is_primary_key=True),
            LogicalAttribute(name="customer_id", data_type=DataType.uuid(), is_nullable=False),
            LogicalAttribute(name="total_amount", data_type=DataType.decimal(12, 2), is_nullable=False),
            LogicalAttribute(name="order_code", data_type=DataType.string(50), is_unique=True),
            LogicalAttribute(name="created_at", data_type=DataType.timestamp(), is_nullable=False),
        ],
        relations=[
            Relation(
                name="order_customer_fk",
                target_entity_uri="data://logical/sales/Customer",
                source_attribute="customer_id",
                target_attribute="customer_id",
            )
        ],
    )

    ddl = PostgresProjectionEngine.to_create_table_ddl(entity, schema="sales")

    assert "CREATE TABLE IF NOT EXISTS sales.order (" in ddl
    assert "order_id UUID NOT NULL" in ddl
    assert "CONSTRAINT pk_order PRIMARY KEY (order_id)" in ddl
    assert "CONSTRAINT fk_order_customer_id FOREIGN KEY (customer_id) REFERENCES sales.customer (customer_id)" in ddl
    assert "CREATE UNIQUE INDEX IF NOT EXISTS uq_order_order_code ON sales.order (order_code);" in ddl
    assert "COMMENT ON TABLE sales.order IS 'A customer sales order record.';" in ddl
