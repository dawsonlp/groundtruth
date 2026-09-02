# ADR 0001: MOF and DAMA-DMBOK Meta-Model Conformance for Enterprise Data Modeling

* **Status**: ACCEPTED
* **Date**: 2026-09-02
* **Deciders**: Larry Dawson, GroundTruth Core Team
* **Consulted**: Tripartite Semantic Federation Architects
* **Governing Document**: [Tripartite ADR 0001](../../adrs/0001-first-principles-information-dependencies-for-ontology-design.md)

---

## 1. Context and Problem Statement

Enterprise data modeling has historically suffered from conflating conceptual business meaning with physical database structures (e.g. creating SQL tables before defining business terms). When autonomous AI agents generate database schemas, they risk introducing inconsistent column names, unclassified PII, and ad-hoc state transitions.

GroundTruth requires a formal, multi-tiered meta-model standard to separate conceptual business terms, logical entity schemas, and physical database projections.

---

## 2. Decision Outcome

We establish that **GroundTruth strictly conforms to the OMG Meta-Object Facility (MOF) 4-layer architecture and DAMA-DMBOK data management principles**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        GROUNDTRUTH 4-TIER DATA ARCHITECTURE                            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [TIER 1: CONCEPTUAL DOMAIN] (data://conceptual/...)                                   │
│  • Business Glossary, Terms, Definitions, Taxonomy & Synonyms                          │
│                                                                                        │
│  [TIER 2: LOGICAL DOMAIN] (data://logical/...)                                         │
│  • DAMA Entity Models, Typed Attributes, Constraints, Primary/Foreign Keys, State Graphs│
│                                                                                        │
│  [TIER 3: PHYSICAL DOMAIN] (data://physical/...)                                        │
│  • Deterministic PostgreSQL DDL, Parquet Schemas, JSON Schema, Partitioning & Indexes  │
│                                                                                        │
│  [TIER 4: LINEAGE & GOVERNANCE] (data://lineage/..., data://governance/...)            │
│  • Column-level Provenance, Transform Pipelines, PII/GDPR Privacy Tags & Retention     │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Core Invariant Rules:
1. **No Physical DDL without Logical Entity**: A table cannot exist without being compiled from a logical entity.
2. **Mandatory PII Tagging**: Any logical attribute containing sensitive personal data must carry explicit privacy classification.
3. **Finite State Machines on Lifecycle Attributes**: Status attributes must declare valid state transition matrices.

---

## 3. Consequences

### Positive
* **Mathematical Precision**: Clean separation between human business meaning and physical SQL storage.
* **Lossless AI Compilation**: AI agents generate database DDL deterministically from logical models.
* **Zero PII Leakage**: Automated classification prevents unmasked personal data exposure.

### Negative / Trade-offs
* Requires defining conceptual terms before generating quick exploratory SQL prototypes.

