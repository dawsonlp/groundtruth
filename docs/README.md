# GroundTruth Documentation Portal 🌐

Welcome to the documentation portal for **GroundTruth**, the single source of truth for **Information & Data Semantics** in the Tripartite Federation.

---

## The Tripartite Semantic Federation

```
        ┌────────────────────────────────────────────────────────┐
        │                  NORTHSTAR (Intent)                    │
        │               (Why & What Is Permitted)                │
        │         req://, decision://, constraint://             │
        └───────────────▲────────────────────────▲───────────────┘
                        │                        │
          GOVERNS /     │                        │ CONSTRAINS /
          SATISFIES     │                        │ VALIDATES
                        │                        │
┌───────────────────────┴──────┐        ┌────────┴───────────────────────┐
│     CODEMESH (Computation)   │        │     GROUNDTRUTH (Information)  │
│       (How It Computes)      │ ────── │   (What Data Exists & Means)   │
│            csi://            │        │             data://            │
└──────────────────────────────┘        └────────────────────────────────┘
```

---

## Reading Paths

### 1. Requirements & Core Specifications
* 📄 **[Data Authority Requirements Specification](specifications/data_authority_requirements_spec.md)**: Full requirements specification covering DAMA 3-tier hierarchy preservation (Conceptual $\to$ Logical $\to$ Physical), schema evolution, classification & privacy tagging, and invariant declarations.
* 📄 **[URI Addressing Grammar](specifications/uri_addressing_grammar.md)**: Formal grammar for `data://conceptual/...`, `data://logical/...`, and `data://physical/...`.
* 📄 **[Tripartite Integration Guide](federation/tripartite_integration.md)**: Cross-ontology relational verbs (`CREATES`, `READS`, `WRITES`, `VALIDATES`, `SERIALIZES`, `REPRESENTS`, `CONSTRAINED_BY`) connecting GroundTruth with **CodeMesh** and **Northstar**.

### 2. Product Refinement Layers (`layers/`)
* 🏛️ **[Product Conception](../layers/product-conception/)**: Problem investigation and initial model foundation.
* 📐 **[Data Modeling Definition](../layers/data-modeling-definition/)**: OMG MOF / CMOF and DAMA standards conformance.
* 📦 **[Domain Data Dictionary Component](../layers/domain-data-dictionary-component/)**: Component design and architecture.
* 💡 **[Conceptual Data Model](../layers/domain-data-dictionary-conceptual-model/)**: Technology-neutral business concepts and relationships.
* 🧩 **[Logical Data Model](../layers/domain-data-dictionary-logical-model/)**: Hybrid catalog kernel (`CAT-LOG`) and typed capability projections.
* 🐘 **[PostgreSQL Design & Runtime](../layers/domain-data-dictionary-postgresql-design/)**: Realization in PostgreSQL 18.4 with Flyway migrations and FastAPI runtime scaffold.
