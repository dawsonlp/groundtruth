# Domain Data Dictionary PostgreSQL Runtime

## Status

- Status: exploratory runtime scaffold verified; PostgreSQL realization pending
- Effective: no
- Source layer: `domain-data-dictionary-postgresql-design`
- Source revision: `f10afc7`
- Owning transform: [domain-data-dictionary-postgresql-runtime](../domain-data-dictionary-postgresql-design/transforms/domain-data-dictionary-postgresql-runtime/transform.md)
- Runnable subproject root: `artifacts/`

## Purpose

Provide the local PostgreSQL, Flyway, and Python API runtime specified by the approved PostgreSQL technical design. The operational scaffold is verified; its next refinement is migration SQL derived directly from `CAT-LOG`, accompanied by traceability and deployed-inventory evidence. The capability API remains undesigned.

## Boundaries

- `artifacts/` owns the complete uv and Compose subproject.
- The current Flyway directory is the verified empty-schema baseline. Product SQL is now the next transform work and must trace to `CAT-LOG` through the derived realization manifest.
- The API exposes operational liveness and readiness only.
- This descendant remains non-effective while its source branch remains draft.

## Build and Run

See [the runnable subproject README](artifacts/README.md). Verification results are recorded in [scaffold-verification.md](evidence/scaffold-verification.md).
