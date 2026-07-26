# Transform: PostgreSQL Design to Runnable Runtime Scaffold

## Status

- Transform status: approved for exploratory execution
- Source layer: `domain-data-dictionary-postgresql-design`
- Source revision: `f1308e8`, plus the architect's 2026-07-26 clarification recorded in the source design
- Source effectiveness: draft and not effective
- Target layer: `domain-data-dictionary-postgresql-runtime`
- Target effectiveness: must remain draft and not effective

## Purpose

Produce a runnable local infrastructure and API scaffold that realizes the approved PostgreSQL technical design without inventing the catalog physical schema or product capability API.

## Required Human Inputs

- Flyway Open Source is the SQL migration runner.
- FastAPI/Uvicorn and async Psycopg 3 form the API runtime scaffold.
- The uv project root is the root of the runnable subproject, not the repository root.
- One local shared database login is acceptable.
- Default host ports are PostgreSQL `25432` and API `28000`.

## Artifact Boundary

The target layer is `layers/domain-data-dictionary-postgresql-runtime/`. Its `artifacts/` directory is the complete runnable subproject root and owns:

- `pyproject.toml`, `uv.lock`, and `.python-version`;
- Python packages and tests;
- `Dockerfile`, `compose.yaml`, `.env.example`, and ignore files;
- the Flyway project and empty product-migration directory; and
- the PostgreSQL initialization-shadow directory.

No executable projection at repository root is produced. The target README and evidence documents describe status and validation but do not become independent authorities for runtime behavior.

## Inputs

- approved PostgreSQL technical design and development checklist in the source layer;
- `CAT-LOG/domain-data-dictionary@1` at revision `f71a279` as a provisional upstream contract;
- pinned local PostgreSQL image `dawsonlp/postgres-batteries-inc:18.4`;
- current official dependency and container-image evidence refreshed at execution time; and
- the preserved user-owned `supporting_documents/` working-tree directory, which is outside transform scope.

## Procedure

1. Create the target layer and runnable artifact root.
2. Create the root uv project using Python 3.14 and the approved dependency boundaries.
3. Implement only liveness, database readiness, settings, pool lifecycle, and transaction-boundary scaffolding.
4. Create a non-root API image build from the locked uv environment.
5. Create Flyway configuration without product DDL.
6. Create Compose services `postgres`, `migrate`, and `api` with the approved health and completion dependencies.
7. Shadow the database image's baked initialization scripts and override its AGE preload.
8. Verify the Python project and then the isolated Compose runtime.
9. Record evidence and update the source checklist only for demonstrated results.

## Expected Outputs

- `layers/domain-data-dictionary-postgresql-runtime/README.md`
- runnable subproject under `layers/domain-data-dictionary-postgresql-runtime/artifacts/`
- `layers/domain-data-dictionary-postgresql-runtime/evidence/scaffold-verification.md`

## Preservation Constraints

- Create no catalog product table, column, constraint, index, extension, or seed data before accepted `CAT-PHY` authority exists.
- Create no product capability endpoint beyond operational liveness and readiness.
- Keep migrations SQL-authored and outside the API lifecycle.
- Preserve PostgreSQL named volumes during normal execution.
- Do not touch `supporting_documents/` or unrelated user changes.
- Keep all target artifacts inside the named runtime layer.

## Validation Conditions

- [ ] Every target path is owned by this transform and lies inside the target layer.
- [ ] Locked Python 3.14 sync, lint, types, and tests pass.
- [ ] Compose configuration validates with a supplied local password.
- [ ] The API image builds reproducibly and runs as a non-root user.
- [ ] PostgreSQL health precedes Flyway success, which precedes API startup.
- [ ] Fresh initialization contains no baked sample objects or unrequested extensions.
- [ ] API liveness is database-independent and readiness reflects database and migration state.
- [ ] A normal recreate preserves named-volume data.
- [ ] No product DDL or product API behavior exists.

## Retry Guidance

Runtime packaging, Compose, Flyway, health, or connection-pool failures return to this transform or its source design. A missing catalog concept or database representation returns to the logical model or the future `CAT-PHY` transform. Regenerate the target artifact set from the corrected source rather than repairing an unexplained downstream divergence.
