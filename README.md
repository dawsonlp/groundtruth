# GroundTruth 🌐

> **The Single Source of Truth for Information & Data Semantics in the Tripartite Federation**

**GroundTruth** manages what data *is*, what it *means*, and how it *persists*, establishing an authoritative domain data dictionary and catalog kernel. In the **Tripartite Semantic Federation**, GroundTruth represents the **Information Domain** ("What Data Exists & Means"), partnering with **CodeMesh** ("How It Computes") and **Northstar** ("Why & What Is Permitted").

---

## The Tripartite Semantic Federation

```
                          ┌─────────────────────────────────────────────────────────┐
                          │               INTENT & GOVERNANCE DOMAIN                │
                          │                       (Northstar)                       │
                          │                (Why & What Is Permitted)                │
                          │                                                         │
                          │   • Requirements (Functional / Non-Functional)          │
                          │   • Architectural Decision Records (ADRs)               │
                          │   • Constraints & Executable Guardrails                 │
                          │   • Policies (Security, Privacy, Compliance, SLOs)      │
                          └───────────────▲─────────────────────────▲───────────────┘
                                          │                         │
                            GOVERNS /     │                         │ CONSTRAINS /
                            SATISFIES     │                         │ VALIDATES
                                          │                         │
┌─────────────────────────────────────────┴─────────────┐     ┌─────┴───────────────────────────────────┐
│                 COMPUTATION DOMAIN                    │     │           INFORMATION DOMAIN            │
│                     (CodeMesh)                        │     │              (GroundTruth)              │
│                  (How It Computes)                    │     │       (What Data Exists & Means)        │
│                                                       │     │                                         │
│   • Canonical Symbol IDs (csi://)                     │     │   • Conceptual Models (Business Terms)  │
│   • Symbol Contracts (Signatures, Types, Docstrings)  │ ─── │   • Logical Data Models (Entities, Attrs│
│   • AST Implementations, Call Graphs, Invariants      │     │   • Physical Data Objects (Tables, DDL) │
│   • Zero-Diff Slices & File Projections               │     │   • Schema Evolution, Lineage & Keys    │
└───────────────────────────────────────────────────────┘     └─────────────────────────────────────────┘
                               READS / WRITES / CREATES / VALIDATES / SERIALIZES
```

| Authority | Focus | Canonical URI Schemes |
| :--- | :--- | :--- |
| **GroundTruth** | The structure, business meaning, relationships, integrity rules, and physical schemas of persistent and transient data. | `data://conceptual/...`<br>`data://logical/...`<br>`data://physical/...` |
| **CodeMesh** | How computation is structured, executed, tested, and materialized into physical source code. | `csi://<package>/<namespace>/<Symbol>[.<member>]` |
| **Northstar** | Why the software exists, business goals, regulatory constraints, architectural decisions, and executable guardrails. | `req://...`<br>`decision://...`<br>`constraint://...`<br>`policy://...`<br>`quality://...` |

---

## Canonical Addressing Grammar (`data://`)

GroundTruth exposes deterministic, immutable URIs across the DAMA information architecture hierarchy:

### 1. Conceptual Domain Concepts (`data://conceptual/`)
* **Format**: `data://conceptual/<domain>/<BusinessConcept>`
* **Examples**:
  * `data://conceptual/sales/Customer`
  * `data://conceptual/billing/Invoice`

### 2. Logical Data Entities & Attributes (`data://logical/`)
* **Format**: `data://logical/<domain>/<Entity>[.<Attribute>]`
* **Examples**:
  * `data://logical/sales/Order`
  * `data://logical/sales/Order.total_amount`
  * `data://logical/sales/Order.line_items`

### 3. Physical Storage & Wire Schemas (`data://physical/`)
* **Format**: `data://physical/<system-type>/<cluster-or-db>/<schema-or-topic>/<object>[.<field>]`
* **Examples**:
  * `data://physical/postgres/primary_db/public/orders.total_cents`
  * `data://physical/kafka/production_broker/orders.v1/order_placed.proto#OrderPlacedPayload`

---

## Documentation & Specifications

* 📚 **[Documentation Portal](docs/README.md)**: Index and reading paths.
* 📄 **[Data Authority Requirements Specification](docs/specifications/data_authority_requirements_spec.md)**: Comprehensive specification covering DAMA 3-tier hierarchy preservation, schema evolution, privacy/classification tagging, and invariant declarations.
* 📄 **[URI Addressing Grammar](docs/specifications/uri_addressing_grammar.md)**: Formal EBNF grammar and normalization rules for `data://` URIs.
* 🌐 **[Tripartite Integration Guide](docs/federation/tripartite_integration.md)**: Cross-ontology linking with CodeMesh (`csi://`) and Northstar (`req://`, `decision://`).
* 🏛️ **[Architectural Decision Records](adr/)**: Foundational decisions on MOF/CMOF metamodel conformance and flat layer graphs.

---

## Product Refinement Architecture

This project organizes product refinement as a flat layer graph conforming to OMG Complete MOF (CMOF) and DAMA standards:

```text
layers/
├── product-conception/
│   ├── artifacts/
│   │   └── product-investigation.md
│   └── transforms/
│       └── data-modeling-definition/
│           ├── transform.md
│           ├── standards-assessment.md
│           ├── cmof-fit-assessment.md
│           └── worked-example.md
├── data-modeling-definition/
│   ├── artifacts/
│   │   └── data-modeling-language.md
│   └── transforms/
│       └── domain-data-dictionary-component/
│           └── transform.md
├── domain-data-dictionary-component/
│   ├── README.md
│   ├── artifacts/
│   │   └── component-design.md
│   └── transforms/
│       └── domain-data-dictionary-conceptual-model/
│           └── transform.md
├── domain-data-dictionary-conceptual-model/
│   ├── README.md
│   ├── artifacts/
│   │   ├── build-design.md
│   │   └── conceptual-data-model.md
│   └── transforms/
│       └── domain-data-dictionary-logical-model/
│           └── transform.md
├── domain-data-dictionary-logical-model/
│   ├── README.md
│   ├── artifacts/
│   │   ├── logical-design.md
│   │   └── logical-data-model.md
│   └── transforms/
│       ├── domain-data-dictionary-postgresql-design/
│       │   ├── transform.md
│       │   └── migration-tool-assessment.md
│       └── domain-data-dictionary-capability-api-architecture/
│           └── transform.md
├── domain-data-dictionary-postgresql-design/
│   ├── README.md
│   ├── artifacts/
│   │   ├── technical-design.md
│   │   └── development-checklist.md
│   └── transforms/
│       └── domain-data-dictionary-postgresql-runtime/
│           └── transform.md
├── domain-data-dictionary-postgresql-runtime/
│   ├── README.md
│   ├── artifacts/
│   │   ├── pyproject.toml
│   │   ├── compose.yaml
│   │   ├── Dockerfile
│   │   ├── src/
│   │   ├── tests/
│   │   └── infra/
│   └── evidence/
│       ├── scaffold-verification.md
│       └── postgresql-realization-verification.md
└── domain-data-dictionary-capability-api-architecture/
    ├── README.md
    └── artifacts/
        └── architecture.md
```

### Layer Status & Refinements
- `artifacts/` contains the product as expressed at each refinement level.
- `transforms/` contains specifications for producing sibling layers under `layers/`.
- The logical layer (`CAT-LOG`) establishes a hybrid catalog kernel: typed authority for governance records, reflective authority for CMOF/DML model objects, and derived typed capability projections.
- The PostgreSQL implementation branch provides physical realization in PostgreSQL 18.4 with Flyway migrations and FastAPI service runtime under `layers/domain-data-dictionary-postgresql-runtime/artifacts/`.
