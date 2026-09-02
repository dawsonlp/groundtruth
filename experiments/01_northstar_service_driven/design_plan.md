# GroundTruth Design Plan (Northstar Service-Driven)

> **Generated from**: Live Northstar Knowledge Graph Query (`http://localhost:9480/api/v1/closure`)  
> **Input Token Footprint**: ~2,047 tokens (8,188 characters across 7 atomic capability closures)  
> **Governing ADRs**: `decision://arch/adr-0001-require-mof-conformance`, `decision://arch/adr-0002-dama-aligned-4-tier-data-modeling-architecture`  
> **Active Invariants**: `mof-meta-level-separation`, `state-machine-validity`, `mandatory-pii-classification`, `deterministic-ddl-purity`

---

## 1. Architectural Topology & Component Boundaries

The system architecture is strictly derived from the 5 Northstar Bounded Contexts:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        GROUNDTRUTH SERVICE ARCHITECTURE                                │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Conceptual Bounded Ctx  │ 2. Logical Bounded Ctx     │ 3. Physical Bounded Ctx      │
│ • ObjectClass registry     │ • LogicalEntity schemas    │ • Deterministic DDL Engine   │
│ • PropertyConcept taxonomy │ • State Machine matrix     │ • Migration generator        │
│ • DataElementConcepts      │ • Foreign key integrity    │ • Target adapters (PG/Parquet│
├────────────────────────────┴────────────────────────────┴──────────────────────────────┤
│ 4. Lineage & Provenance    │ 5. Governance & Compliance                                │
│ • Column-level DAG graph   │ • PII/GDPR classification tag enforcement                 │
│ • Transform pipelines      │ • Executable data quality rule evaluation                 │
└────────────────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 2. Core Domain Models & Class Contracts

### 2.1 Conceptual Tier (`src/groundtruth/conceptual/`)
* **`ObjectClass`**: Represents an enterprise business entity type (e.g., `Customer`, `Order`).
* **`PropertyConcept`**: Reusable conceptual property category (`Designation`, `Definition`, `OccurrenceTime`, `LifecycleState`, `Classification`).
* **`DataElementConcept`**: Application of a `PropertyConcept` to an `ObjectClass` (`<ObjectClass>.<PropertyConcept>`).

### 2.2 Logical Tier (`src/groundtruth/logical/`)
* **`LogicalEntity`**: DAMA-compliant entity schema with typed attributes, primary key, and conceptual term reference.
* **`Attribute`**: Logical column with primitive data type (`String`, `Integer`, `Decimal`, `Timestamp`, `UUID`), nullability, and sensitivity tags.
* **`FiniteStateMachine`**: Declared legal state transitions matrix `{(from_state, to_state): transition_rule}`.

### 2.3 Physical Tier (`src/groundtruth/physical/`)
* **`PostgresProjectionEngine`**: Pure function mapping `LogicalEntity` $\to$ deterministic PostgreSQL DDL string.
* **`SchemaMigration`**: Reversible migration script generator.

### 2.4 Lineage & Governance (`src/groundtruth/lineage/`, `src/groundtruth/governance/`)
* **`LineageGraph`**: Directed acyclic graph tracing column provenance across transforms.
* **`PrivacyClassifier`**: Enforces mandatory PII classification tags on customer entities.

---

## 3. Operational Contracts & Error Handling

All operational methods map directly to Northstar `CapabilitySpec` contracts:

| Capability | Contract Precondition | Contract Guarantee | Failure Mode & Recovery |
| :--- | :--- | :--- | :--- |
| `register_business_term()` | Term slug valid, definition > 10 chars | Registered under `data://conceptual/<slug>` | `DuplicateTermError` (CONCEPTUAL_001) |
| `define_entity_schema()` | Conceptual ref exists, PK declared | Registered under `data://logical/<domain>/<name>` | `MissingPrimaryKeyError` (LOGICAL_001) |
| `verify_state_transition()` | State machine exists, state $\in$ states | Returns boolean transition validity | `IllegalStateTransitionError` (LOGICAL_003) |
| `generate_ddl_projection()` | Entity lifecycle is ACTIVE | Deterministic, sorted DDL string | `UnsupportedTypeMappingError` (PHYSICAL_001) |
| `enforce_privacy_tagging()` | Sensitive attributes classified | Generates compliance certificate | `UnclassifiedSensitiveDataError` (GOVERNANCE_001) |

