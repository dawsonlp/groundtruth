# Domain Catalog Runtime Scaffold

This directory is the uv project and Docker Compose project root for the exploratory Domain Catalog PostgreSQL runtime.

## Local Python Verification

```sh
uv sync --locked
uv run ruff check .
uv run mypy src tests
uv run pytest
```

## Local Compose Runtime

The project-local `.env` beside `compose.yaml` supplies the local credential and port settings. It is ignored by Git, must be mode `0600`, and must contain a cryptographically random password rather than a memorable development phrase. Do not use an account-level `.env` from the home directory.

For a new checkout, copy `.env.example` to `.env`, set a password generated with at least 256 bits of secure randomness (for example, 32 random bytes encoded as hex), and restrict the file to its owner before starting Compose.

```sh
docker compose config -q
docker compose up --build --wait
```

Default host endpoints:

- API: `http://localhost:28000`
- PostgreSQL: `localhost:25432`

The normal shutdown command preserves the named database volume:

```sh
docker compose down
```

Do not add `--volumes` unless deliberately destroying this subproject's database state.

## Current Product Boundary

The PostgreSQL catalog kernel is implemented through Flyway SQL and covers the six `CAT-LOG` authorities. Its [realization manifest](infra/postgres/realization-manifest.md) records exact mapping, database enforcement, and validation gaps. Only `/health/live` and `/health/ready` are implemented in the API; capability endpoints still require their own accepted upstream contract. Definition-aware CMOF/DML validation also remains pending upstream machine-readable definitions.
