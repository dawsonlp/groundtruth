# GroundTruth Implementation Plan (Northstar Service-Driven)

> **Execution Strategy**: Component-by-component implementation matching the 5 Northstar bounded contexts and their operational capability contracts.

---

## 1. Phase 1: Conceptual Model Core (`src/groundtruth/conceptual/`)
* **Task 1.1**: Implement `ObjectClass`, `PropertyConcept`, and `DataElementConcept` dataclasses in `src/groundtruth/conceptual/models.py`.
* **Task 1.2**: Implement `ConceptualCatalog` repository in `src/groundtruth/conceptual/catalog.py` satisfying:
  - `req://conceptual/register-business-term`
  - `req://conceptual/define-property-concept`
* **Task 1.3**: Unit tests in `tests/test_conceptual.py`.

---

## 2. Phase 2: Logical Data Modeling Engine (`src/groundtruth/logical/`)
* **Task 2.1**: Implement `LogicalEntity`, `LogicalAttribute`, `Relation`, and `FiniteStateMachine` in `src/groundtruth/logical/entities.py`.
* **Task 2.2**: Implement `LogicalSchemaEngine` satisfying:
  - `req://logical/define-entity-schema`
  - `req://logical/verify-state-transition`
  - `req://logical/validate-foreign-key-integrity`
* **Task 2.3**: Enforce invariant `constraint://groundtruth/state-machine-validity`.
* **Task 2.4**: Unit tests in `tests/test_logical.py`.

---

## 3. Phase 3: Physical Projection Engine (`src/groundtruth/physical/`)
* **Task 3.1**: Implement `PostgresProjectionEngine` in `src/groundtruth/physical/postgres.py` satisfying:
  - `req://physical/generate-ddl-projection`
  - Deterministic column sorting, primary/foreign keys, and indexes.
* **Task 3.2**: Enforce invariant `constraint://groundtruth/deterministic-ddl-purity`.
* **Task 3.3**: Unit tests in `tests/test_physical.py`.

---

## 4. Phase 4: Lineage & Governance (`src/groundtruth/lineage/`, `src/groundtruth/governance/`)
* **Task 4.1**: Implement `LineageGraph` in `src/groundtruth/lineage/graph.py` satisfying `req://lineage/trace-column-provenance`.
* **Task 4.2**: Implement `GovernanceEngine` in `src/groundtruth/governance/engine.py` satisfying:
  - `req://governance/enforce-privacy-tagging`
  - Invariant `constraint://groundtruth/mandatory-pii-classification`.
* **Task 4.3**: Unit tests in `tests/test_governance.py`.

---

## 5. Phase 5: Public API & Tripartite Integration (`src/groundtruth/api.py`)
* **Task 5.1**: Implement `GroundTruthCatalog` facade unifying all 5 tiers.
* **Task 5.2**: Register CodeMesh symbols into Northstar `.northstar/links.yaml` to satisfy all 7 capabilities.
* **Task 5.3**: Pre-commit invariant validation via `NorthstarCatalog.validate_code()`.

