# GroundTruth Design Plan (File / Document-Driven)

> **Generated from**: Manual traversal and synthesis of 71 Markdown and YAML files across `groundtruth/layers/` and `groundtruth/docs/requirements/`  
> **Input Token Footprint**: ~125,482 tokens (501,928 characters across 71 files)  
> **Source Documents Traversed**:
> - `layers/domain-data-dictionary-conceptual-model/artifacts/conceptual-data-model.md`
> - `layers/domain-data-dictionary-logical-model/artifacts/logical-data-model.md`
> - `layers/domain-data-dictionary-postgresql-design/`
> - `layers/domain-data-dictionary-postgresql-runtime/`
> - `layers/domain-data-dictionary-capability-api-architecture/`
> - `docs/requirements/components/*.md`, `docs/requirements/capabilities/**/*.md`, `docs/requirements/adrs/*.md`

---

## 1. Architectural Synthesis from Multi-Layer Documents

Scanning the entire flat-file tree reveals multiple evolving naming conventions and conceptual models:
1. **Legacy Layer System (`CAT-CON`, `CAT-LOG`, `CAT-PHY`)**:
   - The repository historically used an artifact layer model where `domain-data-dictionary-conceptual-model` defines `CAT-CON/domain-data-dictionary@1` governed by `DML-DEF` (Data Modeling Definition).
   - Distinguishes catalog internal data (`CAT-DATA`) from customer business domain data (`BDM-DATA`).
   - Uses transform descriptors in `transforms/*/transform.md` to record step-by-step refinement between layers.
2. **Modern Requirements System (`component://groundtruth/*`)**:
   - Organizes the architecture into 5 Bounded Contexts: `conceptual`, `logical`, `physical`, `lineage`, `governance`.
   - Normalizes legacy concepts (`ObjectClass`, `PropertyConcept`, `DataElementConcept`) into formal Northstar `CapabilitySpec` contracts.

---

## 2. Reconciled Component & Layer Mapping

| Legacy Layer Artifact | Modern Bounded Context | Core Entities & Scope |
| :--- | :--- | :--- |
| `domain-data-dictionary-conceptual-model` | `component://groundtruth/conceptual` | `ObjectClass`, `PropertyConcept` (Designation, Definition, Scope, Classification, OccurrenceTime, LifecycleState) |
| `domain-data-dictionary-logical-model` | `component://groundtruth/logical` | `LogicalEntity`, `LogicalAttribute`, `Relation`, `FiniteStateMachine` |
| `domain-data-dictionary-postgresql-design` | `component://groundtruth/physical` | `PostgresProjection`, `TableDefinition`, `ColumnDefinition`, `MigrationScript` |
| `domain-data-dictionary-postgresql-runtime` | `src/domaincatalog_api` $\to$ `src/groundtruth` | FastAPI runtime, psycopg3 connection pool, health & metrics |

---

## 3. Cognitive Overhead & Ambiguity Identified in File Reading

During the file-driven analysis, several challenges arose:
1. **Naming Divergence**: The legacy layers refer to the product as `Domain Data Dictionary` and `Domain Catalog` (`domaincatalog_api`), whereas modern requirements use `GroundTruth`.
2. **Prose Density**: The conceptual data model alone (`conceptual-data-model.md`) is 317 lines of detailed prose exploring ISO 11179 concepts, requiring significant filtering to extract executable software contracts.
3. **Implicit Dependencies**: Relationships between transforms and realization artifacts are described in prose rather than machine-traversable relational edges, requiring manual correlation.
