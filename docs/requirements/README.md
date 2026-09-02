# GROUNDTRUTH Requirements & Intent Specification 🧭

> **Authoritative requirements, operational contracts, and governance specification projected from Northstar.**

---

## 1. Solution Overview & Scope
- **Solution Identifier**: `groundtruth`
- **Total Components (Bounded Contexts)**: `5`
- **Total Formal Capabilities**: `7`
- **Governing Architectural Decisions (ADRs)**: `2`
- **Active Invariant Guardrails**: `5`

---

## 2. Component Inventory (Bounded Contexts)

| Component | URI | Purpose | Exported Capabilities |
| :--- | :--- | :--- | :--- |
| **[GroundTruth Logical Data Model](components/logical.md)** | `component://groundtruth/logical` | DAMA-compliant logical entity schemas, typed attribute definitions, primary/foreign key relations, and finite state transition machines. | `3` capabilities |
| **[GroundTruth Conceptual Catalog](components/conceptual.md)** | `component://groundtruth/conceptual` | Enterprise business glossary, conceptual ontology, ObjectClasses, PropertyConcepts, and DataElementConcept semantics. | `3` capabilities |
| **[GroundTruth Governance & Privacy Authority](components/governance.md)** | `component://groundtruth/governance` | Data classification enforcement, PII/GDPR privacy tags, retention policies, and executable data quality validation rules. | `2` capabilities |
| **[GroundTruth Physical Projection Engine](components/physical.md)** | `component://groundtruth/physical` | Deterministic physical DDL projection generators for PostgreSQL, Parquet, JSON Schema, and database migration scripts. | `2` capabilities |
| **[GroundTruth Lineage & Provenance Tracker](components/lineage.md)** | `component://groundtruth/lineage` | Column-level data provenance graphs, pipeline transform tracking, and audit lineage traversal. | `2` capabilities |

---

## 3. Core Capability Contracts

| Capability | Bounded Context | Preconditions | Postconditions | Failure Modes |
| :--- | :--- | :--- | :--- | :--- |
| **[Generate Deterministic Physical DDL Projection](capabilities/physical/generate-ddl-projection.md)** | `physical` | `1` checks | `1` guarantees | `1` error branches |
| **[Register Conceptual Business Term](capabilities/conceptual/register-business-term.md)** | `conceptual` | `2` checks | `1` guarantees | `1` error branches |
| **[Define Reusable Property Concept](capabilities/conceptual/define-property-concept.md)** | `conceptual` | `2` checks | `1` guarantees | `1` error branches |
| **[Trace Column-Level Data Provenance](capabilities/lineage/trace-column-provenance.md)** | `lineage` | `1` checks | `1` guarantees | `1` error branches |
| **[Verify Finite State Machine Transition](capabilities/logical/verify-state-transition.md)** | `logical` | `2` checks | `1` guarantees | `1` error branches |
| **[Define Logical Entity Schema](capabilities/logical/define-entity-schema.md)** | `logical` | `2` checks | `1` guarantees | `2` error branches |
| **[Enforce Data Privacy Classification](capabilities/governance/enforce-privacy-tagging.md)** | `governance` | `1` checks | `1` guarantees | `1` error branches |

---

## 4. Documentation Navigation
- **[Component Specifications](components/)**: Deep bounded context boundaries and dependency contracts.
- **[Operational Capability Contracts](capabilities/)**: Atomic pre/postcondition and failure mode specifications.
- **[Architectural Decisions (ADRs)](adrs/)**: Governing MADR design records and trade-offs.
- **[Executable Invariant Catalog](invariants/catalog.md)**: Active AST rules and guardrails.
- **[Traceability Matrix](traceability_matrix.md)**: Full cross-domain mapping (Intent $\to$ Data $\to$ Code).
