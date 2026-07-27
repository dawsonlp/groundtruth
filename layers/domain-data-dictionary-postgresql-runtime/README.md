# Domain Data Dictionary PostgreSQL Runtime

## Status

- Status: exploratory PostgreSQL structural realization implemented and verified
- Effective: no
- Source layer: `domain-data-dictionary-postgresql-design`
- Source revision: `7d7c1e2`
- Owning transform: [domain-data-dictionary-postgresql-runtime](../domain-data-dictionary-postgresql-design/transforms/domain-data-dictionary-postgresql-runtime/transform.md)
- Runnable subproject root: `artifacts/`

## Purpose

Provide the local PostgreSQL, Flyway, and Python API runtime specified by the approved PostgreSQL technical design. Migration SQL derived directly from `CAT-LOG` now realizes the six logical authorities, accompanied by a derived traceability manifest, deployed-inventory evidence, and structural round-trip tests. The capability API and definition-aware CMOF/DML validation remain incomplete.

## Boundaries

- `artifacts/` owns the complete uv and Compose subproject.
- The Flyway migration is executable physical authority and traces to `CAT-LOG` through the [realization manifest](artifacts/infra/postgres/realization-manifest.md).
- The API exposes operational liveness and readiness only.
- This descendant remains non-effective while its source branch remains draft.

## Build and Run

See [the runnable subproject README](artifacts/README.md). Verification results are recorded in [scaffold-verification.md](evidence/scaffold-verification.md) and [postgresql-realization-verification.md](evidence/postgresql-realization-verification.md).
