# Cross-Domain Traceability Matrix 🔗

> **Bidirectional traceability connecting Intent (`req://`), Decisions (`decision://`), Invariants (`constraint://`), Data (`data://`), and Code (`csi://`).**

---

| Capability | Bounded Context | Governing ADRs | Active Invariants | Satisfying Code Symbols (CodeMesh) |
| :--- | :--- | :--- | :--- | :--- |
| **[Generate Deterministic Physical DDL Projection](capabilities/physical/generate-ddl-projection.md)** | `physical` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/deterministic-ddl-purity` | `csi://groundtruth/physical/postgres.PostgresProjectionEngine.to_create_table_ddl` |
| **[Register Conceptual Business Term](capabilities/conceptual/register-business-term.md)** | `conceptual` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/mandatory-business-definition` | `csi://groundtruth/conceptual/catalog.ConceptualCatalog.register_term` |
| **[Define Reusable Property Concept](capabilities/conceptual/define-property-concept.md)** | `conceptual` | `decision://groundtruth/adr-0001-require-mof-conformance-for-the-governing-model-definition`<br>`decision://groundtruth/adr-0002-dama-aligned-4-tier-data-modeling-architecture` | `constraint://groundtruth/mandatory-business-definition` | `csi://groundtruth/conceptual/catalog.ConceptualCatalog.define_property` |
| **[Trace Column-Level Data Provenance](capabilities/lineage/trace-column-provenance.md)** | `lineage` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | — | `csi://groundtruth/lineage/graph.LineageGraph.trace_column` |
| **[Verify Finite State Machine Transition](capabilities/logical/verify-state-transition.md)** | `logical` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/state-machine-validity` | `csi://groundtruth/logical/engine.LogicalSchemaEngine.verify_state_transition` |
| **[Define Logical Entity Schema](capabilities/logical/define-entity-schema.md)** | `logical` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | — | `csi://groundtruth/logical/engine.LogicalSchemaEngine.define_entity` |
| **[Enforce Data Privacy Classification](capabilities/governance/enforce-privacy-tagging.md)** | `governance` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/mandatory-pii-classification` | `csi://groundtruth/governance/classifier.PrivacyClassifier.enforce_privacy_tagging` |
