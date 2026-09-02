"""Unit test verifying that GroundTruth can self-dogfood its own metamodel and domain models."""

from pathlib import Path
import pytest
from groundtruth import (
    BusinessTerm,
    DataType,
    GroundTruthCatalog,
    LogicalAttribute,
    LogicalEntity,
    PostgresProjectionEngine,
)


def test_dogfood_catalog_loading():
    repo_root = Path(__file__).resolve().parent.parent
    catalog = GroundTruthCatalog.load(repo_root)

    # 1. Verify Level 1: M2 GroundTruth Metamodel entities loaded
    meta_entities = catalog.logical.list_entities(domain="groundtruth_meta")
    meta_entity_names = {e.name for e in meta_entities}
    assert "Term" in meta_entity_names
    assert "Entity" in meta_entity_names
    assert "Attribute" in meta_entity_names

    # 2. Verify Level 2: M1 E-Commerce domain entities loaded
    ecom_entities = catalog.logical.list_entities(domain="ecommerce")
    ecom_entity_names = {e.name for e in ecom_entities}
    assert "Customer" in ecom_entity_names
    assert "Product" in ecom_entity_names
    assert "Order" in ecom_entity_names
    assert "OrderItem" in ecom_entity_names
    assert "Payment" in ecom_entity_names

    # 3. Verify DDL generation for M2 and M1
    m2_ddl = PostgresProjectionEngine.generate_schema_ddl(meta_entities, schema="groundtruth_meta")
    assert "CREATE TABLE IF NOT EXISTS groundtruth_meta.entity" in m2_ddl
    assert "CREATE TABLE IF NOT EXISTS groundtruth_meta.attribute" in m2_ddl

    m1_ddl = PostgresProjectionEngine.generate_schema_ddl(ecom_entities, schema="ecommerce")
    assert "CREATE TABLE IF NOT EXISTS ecommerce.customer" in m1_ddl
    assert "CREATE TABLE IF NOT EXISTS ecommerce.order" in m1_ddl
    assert "CREATE TABLE IF NOT EXISTS ecommerce.payment" in m1_ddl
