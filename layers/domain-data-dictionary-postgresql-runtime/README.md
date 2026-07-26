# Domain Data Dictionary PostgreSQL Runtime

## Status

- Status: exploratory runtime scaffold implemented and verified
- Effective: no
- Source layer: `domain-data-dictionary-postgresql-design`
- Source revision: `ba65ccf`
- Owning transform revision: `623ee6e`
- Runnable subproject root: `artifacts/`

## Purpose

Provide the local PostgreSQL, Flyway, and Python API scaffold specified by the approved PostgreSQL technical design. This layer tests the runtime architecture without claiming that the catalog physical schema or capability API has been designed.

## Boundaries

- `artifacts/` owns the complete uv and Compose subproject.
- The Flyway migration directory contains no product SQL until an accepted `CAT-PHY` artifact exists.
- The API exposes operational liveness and readiness only.
- This descendant remains non-effective while its source branch remains draft.

## Build and Run

See [the runnable subproject README](artifacts/README.md). Verification results are recorded in [scaffold-verification.md](evidence/scaffold-verification.md).
