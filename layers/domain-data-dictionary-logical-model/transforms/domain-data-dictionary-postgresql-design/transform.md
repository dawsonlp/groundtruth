# Transform: Logical Catalog Model to PostgreSQL Implementation Design

## Status

- Transform status: draft
- Transform execution: complete
- Validation status: incomplete
- Source layer: `domain-data-dictionary-logical-model`
- Source revision: `f71a279`
- Source status: draft and not effective
- Target layer: `domain-data-dictionary-postgresql-design`
- Target status: draft and not effective

## Purpose

Refine the technology-neutral Domain Data Dictionary logical model into an engineer-reviewable design for a local PostgreSQL implementation and its first API process without yet producing database DDL, application code, or a running environment.

## Inputs

- `layers/domain-data-dictionary-logical-model/artifacts/logical-design.md` at revision `f71a279`
- `layers/domain-data-dictionary-logical-model/artifacts/logical-data-model.md` at revision `f71a279`
- Model C component design at revision `5a0993d`
- Local image `dawsonlp/postgres-batteries-inc:18.4`, inspected 2026-07-26
- The image source README, Dockerfile, and Compose example under `/Users/dawsonlp/repos/docker_images/postgres-batteries-inc`
- Current official documentation cited in [migration-tool-assessment.md](migration-tool-assessment.md)

## Human Decisions Preserved

- Use the user's batteries-included PostgreSQL image for the local database.
- Organize the local runtime with Docker Compose because additional services will be added.
- Run the API in a container separate from PostgreSQL.
- Use SQL-authored database migrations, with Flyway as the initial candidate and at least one alternative assessed.
- Use Python 3.14, Psycopg 3, uv, and `pyproject.toml` for the API.
- Conduct and review a design session before implementation.

## Decisions Made by This Transform

- Create a PostgreSQL-specific design layer before the runnable implementation layer.
- Start with three Compose services: `postgres`, one-shot `migrate`, and `api`.
- Pin PostgreSQL to `dawsonlp/postgres-batteries-inc:18.4` and mount its named data volume at `/var/lib/postgresql`.
- Shadow the image's baked initialization scripts and override its AGE-preloading command so extensions and demonstration objects are activated only by accepted migrations.
- Select Flyway Open Source `13.0.0` as the migration runner; retain Sqitch as the serious alternative.
- Keep migrations outside both the PostgreSQL image initialization directory and the API process.
- Select FastAPI and Uvicorn for the first HTTP container while deferring all product capability endpoints.
- Use asynchronous Psycopg 3 with `psycopg_pool`, explicit pool lifecycle, and application-owned transactions.
- Place one uv-managed Python project at the repository root, use a `src/` package layout, and commit `uv.lock`.
- Define local-only credential handling and explicitly defer production role separation and secret management.
- Create no PostgreSQL table, column, key, index, extension activation, API resource, or executable configuration in this transform.

## Expected Outputs

- `layers/domain-data-dictionary-postgresql-design/artifacts/technical-design.md`
- `layers/domain-data-dictionary-postgresql-design/artifacts/development-checklist.md`

## Validation Conditions

- [x] The actual local PostgreSQL image tag, architecture, entrypoint, command, port, data mount, health check, and baked initialization scripts were inspected.
- [x] Flyway, Sqitch, and dbmate were compared against the SQL-first and governance requirements.
- [x] Compose startup, migration, API, persistence, health, and failure boundaries are specified.
- [x] Python, uv, Psycopg, connection-pool, packaging, and container constraints are specified.
- [x] The engineer checklist is ordered and gated on design approval.
- [x] No runtime files, migration SQL, schema objects, API behavior, or containers were created.
- [ ] The product owner accepts or revises the migration-tool decision.
- [ ] The product owner accepts or revises the Compose and Python service design.
- [ ] The PostgreSQL physical data model maps all six authoritative logical entities and passes architectural review.
- [ ] The API capability contract is designed before business endpoints are implemented.

## Retry Guidance

If implementation exposes a database or service-design failure, assign it to the earliest owning layer. Repository shape and datatype failures return to `CAT-LOG` or its PostgreSQL physical-model transform; Compose, migration-runner, or API-runtime failures return to this design transform. Do not repair a missing logical concept with an undocumented SQL column or API-only field.
