# Domain Data Dictionary PostgreSQL Design

## Status

- Status: architecture approved; implementation blocked on artifact-boundary finding `IR-001`
- Effective: no
- Selected refinement branch: `product-conception` → `data-modeling-definition` → `domain-data-dictionary-component` → `domain-data-dictionary-conceptual-model` → `domain-data-dictionary-logical-model` → `domain-data-dictionary-postgresql-design`
- Source layer: `domain-data-dictionary-logical-model`
- Source revision: `f71a279`
- Owning transform: [domain-data-dictionary-postgresql-design](../domain-data-dictionary-logical-model/transforms/domain-data-dictionary-postgresql-design/transform.md)

## Artifacts

- [Technical design](artifacts/technical-design.md)
- [Engineer development checklist](artifacts/development-checklist.md)
- [Migration-tool assessment](../domain-data-dictionary-logical-model/transforms/domain-data-dictionary-postgresql-design/migration-tool-assessment.md)

This layer designs the local PostgreSQL, migration, and API runtime. It does not contain the PostgreSQL physical schema, executable Compose files, migration SQL, or API implementation. Those are downstream products of an accepted design and physical model.

The design selects the pinned local PostgreSQL 18.4 image, Flyway Open Source as a one-shot SQL migration service, and a separately built Python 3.14/FastAPI service using uv and Psycopg 3. The product owner approved the design decisions and the architect approved the technical design on 2026-07-26. It remains non-effective, and implementation is blocked until review finding `IR-001` resolves whether the runnable sibling layer contains the uv project or explicitly owns a repository-root projection.
