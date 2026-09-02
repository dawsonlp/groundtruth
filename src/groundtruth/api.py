"""Public Facade for GroundTruth: The Information & Data Authority."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from groundtruth.adapters.git_file import GitFileDataAdapter
from groundtruth.adapters.sqlite import SQLiteDataAdapter
from groundtruth.conceptual.catalog import ConceptualCatalog
from groundtruth.conceptual.models import BusinessTerm, DataElementConcept, PropertyConcept
from groundtruth.governance.classifier import ComplianceCertificate, PrivacyClassifier
from groundtruth.lineage.graph import LineageGraph, ProvenanceEdge
from groundtruth.logical.engine import LogicalSchemaEngine
from groundtruth.logical.entities import LogicalEntity
from groundtruth.logical.state_machine import FiniteStateMachine
from groundtruth.physical.postgres import PostgresProjectionEngine


class GroundTruthCatalog:
    """Public high-level facade for managing enterprise data models across all 4 tiers."""

    def __init__(self):
        self.conceptual = ConceptualCatalog()
        self.logical = LogicalSchemaEngine(self.conceptual)
        self.lineage = LineageGraph()
        self.privacy = PrivacyClassifier()
        self.physical = PostgresProjectionEngine()

    @classmethod
    def load(cls, workspace_root: str | Path) -> "GroundTruthCatalog":
        """Load domain models from workspace files."""
        catalog = cls()
        adapter = GitFileDataAdapter(workspace_root)
        adapter.load_into(catalog.conceptual, catalog.logical)
        return catalog

    def save(self, workspace_root: str | Path) -> None:
        """Persist all domain models to Git YAML files."""
        adapter = GitFileDataAdapter(workspace_root)
        for term in self.conceptual.list_terms():
            adapter.save_term(term)
        for entity in self.logical.list_entities():
            adapter.save_entity(entity)

    def save_sqlite(self, db_path: str | Path) -> None:
        """Compile and persist entire catalog to a single-file SQLite database."""
        adapter = SQLiteDataAdapter(db_path)
        for term in self.conceptual.list_terms():
            adapter.save_term(term)
        for entity in self.logical.list_entities():
            adapter.save_entity(entity)

    # --- Tier 1: Conceptual Operations ---
    def register_business_term(self, term: BusinessTerm) -> BusinessTerm:
        """Register a conceptual term (req://conceptual/register-business-term)."""
        return self.conceptual.register_term(term)

    def define_property_concept(self, prop: PropertyConcept) -> PropertyConcept:
        """Define a reusable property concept (req://conceptual/define-property-concept)."""
        return self.conceptual.define_property(prop)

    # --- Tier 2: Logical Operations ---
    def define_logical_entity(self, entity: LogicalEntity) -> LogicalEntity:
        """Define a DAMA logical entity (req://logical/define-entity-schema)."""
        registered = self.logical.define_entity(entity)
        # Auto-register lineage vertices for all attributes
        for attr in entity.attributes:
            attr_uri = f"{entity.uri}.{attr.name}"
            self.lineage.register_vertex(attr_uri)
        return registered

    def register_state_machine(self, fsm: FiniteStateMachine) -> FiniteStateMachine:
        """Attach a lifecycle finite state machine to an entity attribute."""
        return self.logical.register_state_machine(fsm)

    def verify_state_transition(self, entity_uri: str, attribute_name: str, from_state: str, to_state: str) -> bool:
        """Verify state change validity (req://logical/verify-state-transition)."""
        return self.logical.verify_state_transition(entity_uri, attribute_name, from_state, to_state)

    # --- Tier 3: Physical Operations ---
    def generate_postgres_ddl(self, entity_or_domain: str | LogicalEntity, schema: str = "public") -> str:
        """Generate deterministic PostgreSQL DDL (req://physical/generate-ddl-projection)."""
        if isinstance(entity_or_domain, LogicalEntity):
            return self.physical.to_create_table_ddl(entity_or_domain, schema)

        # Look up by URI
        entity = self.logical.get_entity(entity_or_domain)
        if entity:
            return self.physical.to_create_table_ddl(entity, schema)

        # Look up by domain
        entities = self.logical.list_entities(domain=entity_or_domain)
        if entities:
            return self.physical.generate_schema_ddl(entities, schema)

        raise ValueError(f"Entity or domain '{entity_or_domain}' not found in logical catalog")

    # --- Tier 4: Lineage & Governance Operations ---
    def add_lineage_edge(self, source_uri: str, target_uri: str, transform_name: str = "direct_copy", expression: str = "") -> ProvenanceEdge:
        """Register a transformation link between attributes."""
        return self.lineage.add_lineage(source_uri, target_uri, transform_name, expression)

    def trace_column_provenance(self, attribute_uri: str) -> Dict[str, Any]:
        """Trace column-level provenance (req://lineage/trace-column-provenance)."""
        return self.lineage.trace_column(attribute_uri)

    def enforce_privacy_classification(self, entity_uri: str) -> ComplianceCertificate:
        """Enforce privacy classification and generate audit certificate (req://governance/enforce-privacy-tagging)."""
        entity = self.logical.get_entity(entity_uri)
        if not entity:
            raise ValueError(f"Entity '{entity_uri}' not found in logical catalog")
        return self.privacy.enforce_privacy_tagging(entity)
