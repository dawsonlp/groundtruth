# Transform: PostgreSQL Design to Runnable Runtime Scaffold

## Status

- Transform status: approved
- Transform execution: PostgreSQL structural realization complete
- Validation status: migration, traceability, deployed inventory, and representative structural round-trip passed; definition-aware and normative-model validations remain incomplete
- Source layer: `domain-data-dictionary-postgresql-design`
- Source revision: `f10afc7`
- Source effectiveness: draft and not effective
- Target layer: `domain-data-dictionary-postgresql-runtime`
- Target effectiveness: must remain draft and not effective

## Purpose

Produce and evolve the runnable local infrastructure, PostgreSQL realization, and API scaffold from the approved technical design. Derive migration SQL from `CAT-LOG` without inventing product semantics or a capability API.

## Required Human Inputs

- Flyway Open Source is the SQL migration runner.
- FastAPI/Uvicorn and async Psycopg 3 form the API runtime scaffold.
- The uv project root is the root of the runnable subproject, not the repository root.
- One local shared database login is acceptable.
- Default host ports are PostgreSQL `25432` and API `28000`.
- `CAT-LOG` directly governs the PostgreSQL realization; migration SQL is executable physical authority and does not wait on a separately approved physical model.

## Artifact Boundary

The target layer is `layers/domain-data-dictionary-postgresql-runtime/`. Its `artifacts/` directory is the complete runnable subproject root and owns:

- `pyproject.toml`, `uv.lock`, and `.python-version`;
- Python packages and tests;
- `Dockerfile`, `compose.yaml`, `.env.example`, and ignore files;
- the Flyway project, product migrations, and derived realization manifest;
- the PostgreSQL initialization-shadow directory.

No executable projection at repository root is produced. The target README and evidence documents describe status and validation but do not become independent authorities for runtime behavior.

## Inputs

- approved PostgreSQL technical design and development checklist in the source layer;
- `CAT-LOG/domain-data-dictionary@1` at revision `5728636` as the provisional semantic source;
- pinned local PostgreSQL image `dawsonlp/postgres-batteries-inc:18.4`;
- current official dependency and container-image evidence refreshed at execution time; and
- the preserved user-owned `supporting_documents/` working-tree directory, which is outside transform scope.

## Procedure

1. Create the target layer and runnable artifact root.
2. Create the root uv project using Python 3.14 and the approved dependency boundaries.
3. Implement only liveness, database readiness, settings, pool lifecycle, and transaction-boundary scaffolding.
4. Create a non-root API image build from the locked uv environment.
5. Create Flyway configuration and retain the verified empty-migration scaffold as a baseline.
6. Derive a realization manifest from the exact `CAT-LOG` revision and author versioned PostgreSQL migration SQL as executable physical authority.
7. Create Compose services `postgres`, `migrate`, and `api` with the approved health and completion dependencies.
8. Shadow the database image's baked initialization scripts and override its AGE preload.
9. Verify the Python project, isolated Compose runtime, migration replay, deployed inventory, and representative logical round trips.
10. Record evidence and update the source checklist only for demonstrated results.

## Expected Outputs

- `layers/domain-data-dictionary-postgresql-runtime/README.md`
- runnable subproject under `layers/domain-data-dictionary-postgresql-runtime/artifacts/`
- a derived PostgreSQL realization manifest and versioned SQL migrations under the runnable subproject
- `layers/domain-data-dictionary-postgresql-runtime/evidence/scaffold-verification.md`

## Preservation Constraints

- Trace every catalog product table, column, constraint, index, function, extension, and seed datum to `CAT-LOG` or a documented operational requirement through the derived realization manifest.
- Escalate choices only under the architectural review triggers recorded in the source design.
- Create no product capability endpoint beyond operational liveness and readiness.
- Keep migrations SQL-authored and outside the API lifecycle.
- Preserve PostgreSQL named volumes during normal execution.
- Do not touch `supporting_documents/` or unrelated user changes.
- Keep all target artifacts inside the named runtime layer.

## Validation Conditions

- [x] Every target path is owned by this transform and lies inside the target layer.
- [x] Locked Python 3.14 sync, lint, types, unit tests, and database integration tests pass.
- [x] Compose configuration validates with a supplied local password.
- [x] The API image builds from the lockfile and runs as a non-root user.
- [x] PostgreSQL health precedes Flyway success, which precedes API startup.
- [x] Fresh initialization contains no baked sample objects or unrequested extensions.
- [x] API liveness is database-independent and readiness reflects database and migration state.
- [x] A normal recreate and a normal shutdown preserve named-volume data.
- [x] A failed transactional migration blocks API startup and leaves no partial table.
- [x] The verified scaffold baseline contains no product DDL or product API behavior.
- [x] Migration SQL and the derived realization manifest cover all six logical authorities and classify enforcement for `CATLOG-001` through `CATLOG-024`.
- [x] Fresh and repeat migration execution, deployed-inventory comparison, and representative structural logical round trips pass.
- [ ] Machine-loaded `CMOF-GOV` and `DML-DEF` drive definition-aware validation of applicability, multiplicity, governed type, composition, and datatype shape.
- [ ] Normative representative `CMOF-GOV`, `DML-DEF`, `CAT-CON`, and subject-model artifacts complete a lossless import/export round trip.

## Retry Guidance

Runtime packaging, Compose, Flyway, health, connection-pool, or PostgreSQL representation failures return to this transform or its source design. A missing or incoherent catalog concept returns to the logical model. Regenerate the target artifact set from the corrected source rather than repairing an unexplained downstream divergence.
