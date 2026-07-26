# PostgreSQL Runtime Scaffold Verification

## Status

- Verification status: scaffold verification passed
- Runtime effectiveness: no
- Source design revision: `ba65ccf`
- Transform revision: `623ee6e`
- Verification date: 2026-07-26

## Image Evidence

- PostgreSQL: local `dawsonlp/postgres-batteries-inc:18.4`; image identity previously inspected as `sha256:8f403d0f3ed0ec5520a8b32c75bb81852cb6a63f1da4f3d9b7ecc646dda88a53`
- Flyway: `flyway/flyway:13.0.0@sha256:db6195c21e90872063ff257ec38edcb8d3c77259b25a7a8fee67189511079511`
- Python: `python:3.14.6-slim-trixie@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6`
- uv: `ghcr.io/astral-sh/uv:0.11.29@sha256:eb2843a1e56fd9e30c7276ce1a52cba86e64c7b385f5e3279a0e08e02dd058fc`

All three external image references resolved as multi-platform indexes containing Linux arm64 and amd64 manifests when inspected on 2026-07-26.

## Python Project Results

- `uv lock --check`: passed; 40 packages resolved under CPython 3.14.6.
- `uv sync --locked`: passed using a subproject-local cache.
- `uv run ruff check .`: passed.
- `uv run mypy src tests`: passed in strict mode for seven source files.
- Unit suite: six passed; the two opt-in database tests were skipped as designed.
- Live database integration suite: two passed against PostgreSQL on host port 25432, proving pool lifecycle, Flyway readiness, commit, and rollback behavior.
- Psycopg runtime: version 3.3.4, binary implementation.

The first sandboxed integration attempt could not open a loopback socket and failed with `Operation not permitted`. The same locked tests passed outside that sandbox restriction; this was an execution-environment restriction, not an application failure.

## Container and Compose Results

- `docker compose config -q`: passed with an ephemeral supplied password.
- API image build: passed from the locked project.
- Local API image identity: `sha256:c69cb25dbad84ef8ea5ef6bfdff4adef7cedbcfd2381f1ccc2e26cc4013a426d`.
- API container identity: UID 10001, user `domaincatalog`.
- Container runtime: Python 3.14.6 and Psycopg 3.3.4 binary.
- Image inspection found no database password or local `.env`; only runtime tool and Python environment settings were embedded.
- Starting the image without `PGPASSWORD` exited nonzero with a Pydantic `Field required` error.

The initial Flyway run exposed an obsolete configuration placement: Flyway 13 rejects `schemas` in the `[flyway]` TOML namespace. The redundant setting was removed because PostgreSQL's existing `public` schema is the only scaffold schema. The corrected run passed.

Observed startup order:

1. PostgreSQL became healthy.
2. Flyway 13.0.0 validated zero migrations, created `public.flyway_schema_history`, and exited zero.
3. The API started and became healthy.

Flyway rerun and explicit `validate` both passed with no migration necessary. The empty migration warning is expected and preserves the physical-model gate.

## Failure and Recovery Results

A temporary versioned migration created a probe table and then divided by zero. Flyway reported that the migration failed and its changes were successfully rolled back. Verification showed:

- migration service exited 1;
- API remained in `Created` and did not start;
- `public.failed_migration_probe` did not exist; and
- after removal of the temporary test file, migration and API startup returned to healthy state.

The temporary migration was removed and is not part of the artifact set.

## Persistence Results

A temporary persistence table and record were created in the isolated database. The PostgreSQL container was force-recreated without removing its named volume. The record remained readable after recreation and was then removed.

A normal `docker compose down` removed containers and the network but retained `domaincatalog_verify_postgres_data`. The stack was restarted from that volume and returned to healthy state.

## Final Database Inventory

The final running database reported:

```text
extension:plpgsql
schema:public
table:public.flyway_schema_history
```

There are no sample tables, AGE catalog or graph, TIGER schema or helpers, optional extensions, persistence probes, failed-migration probes, product tables, or `BDM-DATA`.

## Final Runtime State

- Compose project: `domaincatalog_verify`
- PostgreSQL: healthy on host port 25432
- Flyway: exited 0
- API: healthy on host port 28000
- `/health/live`: `{"status": "live"}`
- `/health/ready`: `{"status": "ready"}`
- Named volume: retained as the requested local instance

The password used for this local verification was supplied only to process environments and was not written to the repository. A developer must create an ignored `.env` before recreating the project without an explicit environment value.

## Deferred Validation

The following cannot pass until their owning artifacts exist:

- `CAT-PHY` comparison and product migration replay;
- round-trip reconstruction of the six logical authorities; and
- product capability API verification.

These omissions do not invalidate the operational scaffold, but they keep the runtime layer non-effective.
