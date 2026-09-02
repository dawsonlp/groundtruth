# GroundTruth: System Design & Domain Architecture Specification

> **Authority**: Northstar Intent & Governance Control Plane (`http://localhost:9480`)  
> **Status**: APPROVED ARCHITECTURE SPECIFICATION  
> **Date**: 2026-09-02  
> **Governing ADRs**:
> - [ADR 0001: Require MOF Conformance for the Governing Model Definition](../../adrs/0001-require-mof-conformance-for-the-governing-model-definition.md)
> - [ADR 0002: DAMA-Aligned 4-Tier Data Modeling Architecture](../../adrs/0002-dama-aligned-4-tier-data-modeling-architecture.md)

---

## 1. Executive Summary & Core Mission

**GroundTruth** is the **Information & Data Authority** for the Tripartite Semantic Federation. It provides the authoritative, mathematically grounded standard for what data exists, what it means, its lifecycle state machines, its physical projections, and its governance policies.

While **CodeMesh** (`csi://`) governs computation and **Northstar** (`req://`, `decision://`, `constraint://`) governs intent, **GroundTruth** (`data://`) governs the data domain:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TRIPARTITE SEMANTIC FEDERATION                                  │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ NORTHSTAR (Intent)         │ GROUNDTRUTH (Data)         │ CODEMESH (Code)              │
│ req://, decision://        │ data://                    │ csi://                       │
│ "Why & What is Permitted"  │ "What Exists & What it Means"│ "How It Computes & Mutates"│
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

---

## 2. Meta-Modeling Levels (OMG MOF 2.5.1 Conformance)

Following **ADR 0001**, GroundTruth strictly organizes data modeling into four meta-levels:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          OMG MOF 2.5.1 META-MODELING STACK                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [M3: META-METAMODEL] (OMG MOF 2.5.1 / CMOF)                                           │
│  • Self-describing foundation defining Package, Class, Property, Association, Type.   │
│                                                                                        │
│  [M2: METAMODEL] (GroundTruth DAMA-Aligned Model Definition)                           │
│  • Defines the grammar of GroundTruth: ObjectClass, PropertyConcept, LogicalEntity,   │
│    LogicalAttribute, Relation, FiniteStateMachine, PostgresProjection, LineageGraph.  │
│                                                                                        │
│  [M1: SUBJECT DOMAIN MODEL] (e.g. Fintech Domain, E-Commerce Domain)                   │
│  • Models a specific customer business domain: Customer, Order, Payment, Transaction.  │
│                                                                                        │
│  [M0: RUNTIME INSTANCE DATA] (PostgreSQL tables, database rows, JSON payloads)          │
│  • Actual operational values: {"order_id": "ord_123", "amount_cents": 4500}.           │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Four-Tier Data Architecture (DAMA-DMBOK Conformance)

Following **ADR 0002**, GroundTruth organizes the $M_1$ domain into 4 distinct, decoupled tiers:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        GROUNDTRUTH 4-TIER DOMAIN PIPELINE                              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [TIER 1: CONCEPTUAL TIER] (`data://conceptual/...`)                                   │
│  • Business Glossary & Shared Semantics (ISO/IEC 11179)                                │
│  • ObjectClass + PropertyConcept ──► DataElementConcept                                │
│                                                                                        │
│  [TIER 2: LOGICAL TIER] (`data://logical/...`)                                         │
│  • DAMA-compliant Normalized Entity Schemas                                            │
│  • Typed Attributes, Primary Keys, Foreign Keys, Nullability                           │
│  • Finite State Machine Matrices (Valid Lifecycle Transitions)                         │
│                                                                                        │
│  [TIER 3: PHYSICAL TIER] (`data://physical/...`)                                       │
│  • Deterministic PostgreSQL DDL Projections (Idempotent, Sorted, Pure Functions)       │
│  • JSON Schema & Parquet Schema Projections                                            │
│  • Versioned Migration Scripts (Up/Down)                                               │
│                                                                                        │
│  [TIER 4: LINEAGE & GOVERNANCE] (`data://lineage/...`, `data://governance/...`)        │
│  • Column-level Provenance Directed Acyclic Graphs (DAGs)                              │
│  • Transform Pipeline Tracking                                                         │
│  • Privacy Classification (PII, FINANCIAL, CONFIDENTIAL, PUBLIC)                       │
│  • Executable Data Quality Rule Engines                                                │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Software Component & Module Design (`src/groundtruth/`)

```
src/groundtruth/
├── __init__.py                    # Top-level exports
├── api.py                         # Public GroundTruthCatalog facade
├── core/
│   ├── __init__.py
│   ├── uris.py                    # data:// URI parser and validator
│   ├── types.py                   # Canonical primitive data types (STRING, INT, UUID, etc.)
│   └── models.py                  # Base domain entity model
├── conceptual/
│   ├── __init__.py
│   ├── models.py                  # ObjectClass, PropertyConcept, DataElementConcept
│   └── catalog.py                 # Conceptual glossary & term repository
├── logical/
│   ├── __init__.py
│   ├── entities.py                # LogicalEntity, LogicalAttribute, PrimaryKey, ForeignKey
│   ├── state_machine.py           # FiniteStateMachine, StateTransition, matrix validator
│   └── engine.py                  # Logical schema compiler & validator
├── physical/
│   ├── __init__.py
│   ├── postgres.py                # Deterministic PostgreSQL DDL generator (Pure function)
│   ├── json_schema.py             # JSON Schema generator
│   └── migrations.py              # Schema migration script generator
├── lineage/
│   ├── __init__.py
│   └── graph.py                   # Column-level DAG provenance & pipeline tracker
├── governance/
│   ├── __init__.py
│   ├── classifier.py              # PII / GDPR classification & audit certifier
│   └── quality.py                 # Executable data quality rule evaluator
├── adapters/
│   ├── __init__.py
│   ├── base.py                    # DataRepository abstract port
│   ├── git_file.py                # Git-native YAML & Markdown storage adapter
│   └── sqlite.py                  # Single-file SQLite catalog adapter (.groundtruth/catalog.sqlite3)
└── service/
    ├── __init__.py
    └── app.py                     # FastAPI REST API for GroundTruth Control Plane
```

---

## 5. Operational Capability Contracts & Implementation Mapping

| Northstar Capability URI | GroundTruth Implementation Symbol | Preconditions | Guarantees |
| :--- | :--- | :--- | :--- |
| `req://conceptual/register-business-term` | `ConceptualCatalog.register_term()` | Term slug is valid; definition > 10 chars | Registered under `data://conceptual/<slug>` |
| `req://conceptual/define-property-concept` | `ConceptualCatalog.define_property()` | Property concept category recognized | Registered under `data://conceptual/properties/<slug>` |
| `req://logical/define-entity-schema` | `LogicalSchemaEngine.define_entity()` | Conceptual term exists; PK declared | Registered under `data://logical/<domain>/<name>` |
| `req://logical/verify-state-transition` | `FiniteStateMachine.verify_transition()`| State machine exists; state $\in$ states | Returns boolean transition validity |
| `req://physical/generate-ddl-projection` | `PostgresProjectionEngine.to_ddl()` | Entity lifecycle is ACTIVE | Deterministic, idempotent DDL string |
| `req://lineage/trace-column-provenance` | `LineageGraph.trace_column()` | Attribute URI exists in catalog | Returns directed acyclic provenance graph |
| `req://governance/enforce-privacy-tagging`| `PrivacyClassifier.enforce_tags()` | Sensitive attributes classified | Generates compliance audit certificate |

---

## 6. Active Invariant Guardrails

Enforced prior to code commits via Northstar AST and runtime validation:

1. **`constraint://groundtruth/mof-meta-level-separation`**:
   - Forbids mixing $M_0$ instance rows into $M_1$ domain models or $M_2$ metamodels.
2. **`constraint://groundtruth/state-machine-validity`**:
   - Forbids undeclared lifecycle state transitions (e.g. `CANCELLED` $\to$ `PAID`).
3. **`constraint://groundtruth/mandatory-pii-classification`**:
   - Requires explicit privacy classification (`tags=['PII']`) on all customer attributes.
4. **`constraint://groundtruth/deterministic-ddl-purity`**:
   - Ensures DDL generation functions are pure, sorted, and free of environmental side-effects.
5. **`constraint://groundtruth/mandatory-business-definition`**:
   - Requires plain-language business definitions on all conceptual terms.

