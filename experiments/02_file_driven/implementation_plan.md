# GroundTruth Implementation Plan (File / Document-Driven)

> **Execution Strategy**: Reconciling legacy layer transform artifacts with modern modular Python packaging.

---

## 1. Phase 1: Harmonize Directory Structure & Packaging
* **Task 1.1**: Migrate legacy `layers/domain-data-dictionary-postgresql-runtime/artifacts/src/domaincatalog_api` into `src/groundtruth/`.
* **Task 1.2**: Unify package dependencies in `pyproject.toml` (FastAPI, psycopg 3, Pydantic 2, SQLAlchemy/SQLGlot).

---

## 2. Phase 2: Conceptual & Semantic Kernel Implementation
* **Task 2.1**: Implement ISO/IEC 11179 semantic concepts (`ObjectClass`, `PropertyConcept`, `DataElementConcept`) extracted from `conceptual-data-model.md`.
* **Task 2.2**: Implement business glossary registration and lookup functions.

---

## 3. Phase 3: Logical Modeling & Finite State Verification
* **Task 3.1**: Implement entity schema definition with attribute types, primary keys, and foreign keys.
* **Task 3.2**: Implement state transition validator based on `logical-data-model.md`.

---

## 4. Phase 4: PostgreSQL Realization & Runtime Service
* **Task 4.1**: Implement deterministic DDL generator for PostgreSQL.
* **Task 4.2**: Integrate PostgreSQL runtime database connection pool and CRUD endpoints.

---

## 5. Phase 5: Verification & Traceability Audit
* **Task 5.1**: Write unit and integration test suite across all modules.
* **Task 5.2**: Reconcile transform evidence files in `layers/*/evidence/`.

