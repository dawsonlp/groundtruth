# ADR 0002: DAMA-Aligned 4-Tier Data Modeling Architecture 🏛️

- **URI**: `decision://arch/adr-0002-dama-aligned-4-tier-data-modeling-architecture`
- **Status**: `ACTIVE`

## 1. Context and Problem Statement
Enterprise data modeling has historically suffered from conflating conceptual business meaning with physical database structures (e.g. creating SQL tables before defining business terms). When autonomous AI agents generate database schemas, they risk introducing inconsistent column names, unclassified PII, and ad-hoc state transitions.

Following [ADR 0001](./0001-require-mof-conformance-for-the-governing-model-definition.md), GroundTruth requires a multi-tiered data architecture to separate conceptual business semantics, logical entity schemas, physical database projections, and lineage/governance.

---

## 2. Decision Outcome
We establish that GroundTruth structures all enterprise data modeling into **4 distinct architectural tiers governed by explicit realization and transformation relationships**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        GROUNDTRUTH 4-TIER DATA ARCHITECTURE                            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [TIER 1: CONCEPTUAL DOMAIN] (data://conceptual/...)                                   │
│  • ObjectClasses, PropertyConcepts, DataElementConcepts, Business Definitions          │
│                                                                                        │
│  [TIER 2: LOGICAL DOMAIN] (data://logical/...)                                         │
│  • DAMA Entity Schemas, Typed Attributes, Constraints, Primary/Foreign Keys,           │
│    Finite State Transition Matrices                                                    │
│                                                                                        │
│  [TIER 3: PHYSICAL DOMAIN] (data://physical/...)                                        │
│  • Deterministic PostgreSQL DDL, Parquet Schemas, JSON Schema, Partitioning & Indexes  │
│                                                                                        │
│  [TIER 4: LINEAGE & GOVERNANCE] (data://lineage/..., data://governance/...)            │
│  • Column-level Provenance, Transform Pipelines, PII/GDPR Privacy Tags & Retention     │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Invariant Rules:
1. **Separation of Concerns**: Conformance $\neq$ Realization $\neq$ Transformation $\neq$ Generation.
2. **No Physical DDL without Logical Entity**: Physical DDL must be deterministically projected from a logical schema.
3. **Mandatory PII Tagging**: Any logical attribute containing sensitive personal data must carry explicit privacy classification.
4. **Finite State Machines on Lifecycle Attributes**: Status attributes must declare valid state transition matrices.

---

## 3. Consequences

### Positive Consequences
- *(None recorded)*

### Negative Consequences / Trade-offs
- *(None recorded)*
