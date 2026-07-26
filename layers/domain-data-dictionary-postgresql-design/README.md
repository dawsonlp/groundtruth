# Domain Data Dictionary PostgreSQL Design

## Status

- Status: approved for exploratory runtime implementation
- Effective: no
- Selected refinement branch: `product-conception` → `data-modeling-definition` → `domain-data-dictionary-component` → `domain-data-dictionary-conceptual-model` → `domain-data-dictionary-logical-model` → `domain-data-dictionary-postgresql-design`
- Source layer: `domain-data-dictionary-logical-model`
- Source revision: `5728636`
- Owning transform: [domain-data-dictionary-postgresql-design](../domain-data-dictionary-logical-model/transforms/domain-data-dictionary-postgresql-design/transform.md)

## Artifacts

- [Technical design](artifacts/technical-design.md)
- [Engineer development checklist](artifacts/development-checklist.md)
- [Migration-tool assessment](../domain-data-dictionary-logical-model/transforms/domain-data-dictionary-postgresql-design/migration-tool-assessment.md)

This layer designs the local PostgreSQL, migration, and API runtime. It does not itself contain PostgreSQL schema objects, executable Compose files, migration SQL, or API implementation. The runtime transform produces migration SQL directly from `CAT-LOG`; that SQL is executable physical authority, while its traceability manifest and deployed inventory are derived evidence rather than a separately approved physical model.

The design selects the pinned local PostgreSQL 18.4 image, Flyway Open Source as a one-shot SQL migration service, and a separately built Python 3.14/FastAPI service using uv and Psycopg 3. The architect clarified that the uv root is the root of the runnable subproject, resolving `IR-001`, and approved the realization transform's authority to make ordinary PostgreSQL physical choices. The approved outbound transform produces `domain-data-dictionary-postgresql-runtime`; the design remains non-effective because its source branch is draft.
