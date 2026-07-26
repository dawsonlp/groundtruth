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

Copy `.env.example` to `.env` and set a local password. `.env` is ignored by Git.

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

Only `/health/live` and `/health/ready` are implemented. The Flyway migration directory intentionally contains no SQL. Product schema and capability endpoints require their own accepted upstream artifacts.
