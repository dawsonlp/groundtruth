# Domain Data Dictionary PostgreSQL Technical Design

## Document Status

- Status: approved for exploratory runtime implementation
- Effective: no
- Source logical model: `CAT-LOG/domain-data-dictionary@1` at revision `f71a279`
- Owning transform: `domain-data-dictionary-logical-model/transforms/domain-data-dictionary-postgresql-design`
- Design date: 2026-07-26
- Runtime creation: authorized through the source-colocated `domain-data-dictionary-postgresql-runtime` transform

## 1. Purpose

Define the buildable local runtime structure for the first PostgreSQL realization of the Domain Data Dictionary: persistent PostgreSQL, independently executed SQL migrations, and a separately containerized Python API. Preserve the Model C authority boundary and create a stable base for later services without preempting the PostgreSQL physical data model or capability API contract.

## 2. Scope

This design decides:

- initial Docker Compose service topology and dependency behavior;
- database image, volume, network, health, and local port constraints;
- migration tool, migration ownership, history, validation, and recovery policy;
- Python version, uv project structure, initial runtime dependencies, container build, and Psycopg connection lifecycle;
- configuration and local-secret boundaries;
- implementation verification and completion evidence.

It does not decide:

- PostgreSQL tables, columns, constraints, indexes, partitions, or enabled extensions;
- the physical realization of the six `CAT-LOG` authoritative entities;
- product API resources, commands, queries, messages, authorization, or error contracts;
- production hosting, high availability, backups, TLS, secret management, or deployment automation; or
- additional services beyond reserving a Compose-compatible boundary for them.

## 3. Inputs Consulted

### Governing project inputs

- Model C component design at revision `5a0993d`
- conceptual data model at revision `f311eac`
- logical design and logical data model at revision `f71a279`
- root build/update instructions and the flat-layer ADR
- product-owner technology directions recorded by the owning transform

No product layer is effective. The design is an exploratory descendant, and approval of this document would not by itself accept the upstream conceptual or logical models.

### Observed local context

- Local image: `dawsonlp/postgres-batteries-inc:18.4`
- Image identity inspected: `sha256:8f403d0f3ed0ec5520a8b32c75bb81852cb6a63f1da4f3d9b7ecc646dda88a53`
- Local image architecture: arm64; the image source declares arm64 and amd64 builds, which implementation verification must confirm on the registry
- Database port: `5432/tcp`
- Persistent mount: `/var/lib/postgresql`
- Entrypoint: standard PostgreSQL `docker-entrypoint.sh`
- Default command: PostgreSQL with `shared_preload_libraries=age`
- Built-in health check: `pg_isready`
- Included capabilities: PostGIS, pgvector, Apache AGE, pgRouting, and contrib extensions
- Baked initialization behavior: on a fresh volume the image otherwise enables all included extensions, changes search paths, creates TIGER helpers, four sample tables and indexes, and an AGE sample graph
- Installed host runtime: Python 3.14.6; uv 0.11.21
- No running container was observed during the design session; other local projects reserve host PostgreSQL ports 15432, 15433, and 35432

### Current primary documentation

- [Flyway Docker](https://documentation.red-gate.com/flyway/reference/usage/flyway-docker), [versioned migrations](https://documentation.red-gate.com/fd/versioned-migrations-273973333.html), and [validation](https://documentation.red-gate.com/flyway/reference/commands/validate)
- [Python 3.14.6 slim image](https://hub.docker.com/_/python/)
- [uv projects and lockfiles](https://docs.astral.sh/uv/guides/projects/) and [uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [Psycopg installation/support](https://www.psycopg.org/psycopg3/docs/basic/install.html) and [connection pools](https://www.psycopg.org/psycopg3/docs/advanced/pool.html)
- [FastAPI container guidance](https://fastapi.tiangolo.com/deployment/docker/)

## 4. Design Decisions

### 4.1 Initial service topology

```text
developer or client
        |
        | host port 28000 by default
        v
      api  --------------------+
        |                      |
        | postgres:5432        | readiness
        v                      |
    postgres <------- migrate -+
        |
        v
named volume: postgres_data
```

| Service | Lifecycle | Image/build | Responsibility |
| --- | --- | --- | --- |
| `postgres` | Long-running | `dawsonlp/postgres-batteries-inc:18.4` | Own the local PostgreSQL process and durable named volume; expose installed capabilities without auto-activating them |
| `migrate` | One-shot, restart `no` | `flyway/flyway:13.0.0` | Apply available versioned SQL after PostgreSQL is healthy and record migration history |
| `api` | Long-running | Project Dockerfile based on `python:3.14.6-slim-trixie` | Expose health initially and later the approved capability contract; own the Psycopg pool |

Compose must not set `container_name`; project-scoped names avoid collisions and preserve future scaling. The three services use one internal Compose network. Only `api` and, for local developer access, `postgres` publish host ports. `migrate` publishes none.

Default host ports are configurable and use a recognizable `2xxxx` local-development block while preserving each service's familiar port suffix:

- PostgreSQL: `${DOMAINCATALOG_POSTGRES_PORT:-25432}:5432`
- API: `${DOMAINCATALOG_API_PORT:-28000}:8000`

### 4.2 Startup and failure ordering

1. `postgres` starts and must become healthy for the configured database and user.
2. `migrate` starts only after `postgres` is healthy.
3. `migrate` exits zero only after all available migrations apply successfully.
4. `api` starts only after `migrate` completes successfully.
5. A migration failure prevents API startup and remains visible as a failed one-shot service.
6. The API never runs migrations during process startup.

Database reachability and schema readiness are different facts. Compose health proves reachability; Flyway completion proves that the available migration sequence ran. API readiness additionally proves that its pool can query the database and that the expected schema history is present.

### 4.3 PostgreSQL process and persistence

- Pin the `18.4` image tag; do not use `18` or `latest` even when they currently resolve to the same image.
- Mount a Compose named volume at `/var/lib/postgresql`, the required PostgreSQL 18 image boundary.
- Override the image command with plain `postgres`; the image's default AGE preload is not justified by the current physical model.
- Bind-mount `infra/postgres/initdb/` read-only over `/docker-entrypoint-initdb.d`. That committed directory contains documentation only and no executable `.sql` or `.sh` file. The mount deliberately shadows the image's demonstration initialization scripts.
- Enable extensions only through reviewed versioned migrations and only when `CAT-PHY` requires them.
- Do not put product bootstrap or evolving migrations into the shadow directory; the entrypoint directory is a first-volume mechanism, not a repeatable migration history.
- Use the image's `pg_isready` health mechanism, parameterized for the selected database and user.
- Normal shutdown and recreation preserve the named volume. No normal build, test, or update command removes it.

### 4.4 Migration authority

Flyway Open Source 13.0.0 is selected. The detailed comparison is recorded with the source transform.

Planned repository layout:

```text
infra/
├── postgres/
│   └── initdb/
│       └── README.md
└── flyway/
    ├── flyway.toml
    └── migrations/
        └── V<UTC timestamp>__<description>.sql
```

The entire Flyway project is mounted read-only into the migration container. Non-secret defaults—migration location, history-table name, schema selection, clean-disabled policy—belong in `flyway.toml`. JDBC URL, user, and password come from the runtime environment and are not committed.

Migration rules:

- SQL files are the schema-change authority; neither Python nor an ORM generates migrations.
- Use timestamp versions in UTC to reduce conflicts among humans and agents.
- Use versioned migrations only for the first implementation. Add repeatable migrations only after a demonstrated need and an explicit review of their reapplication semantics.
- Never edit or delete an applied versioned migration in shared history. Add another migration.
- Let Flyway execute each PostgreSQL-compatible migration transactionally. A non-transactional script requires explicit local configuration and rationale.
- Use fully qualified object names once the physical schema names are accepted.
- Do not hide unexpected state with broad `IF EXISTS` or `IF NOT EXISTS` clauses. A migration should fail when its preconditions are false unless idempotence is the intended, tested behavior.
- Run Flyway validation before release and against every persistent development database.
- Do not use `repair` as routine drift suppression, and keep `clean` unavailable outside deliberately disposable test databases.

The first product migration is blocked until the PostgreSQL physical data model assigns tables, types, identifiers, references, constraints, and indexes to all six logical authorities. This design authorizes migration infrastructure, not speculative DDL.

### 4.5 Recovery

- Disposable local recovery: stop the stack, deliberately remove only the named Domain Catalog volume, and replay all migrations from empty state. Volume deletion is never implicit.
- Durable recovery: restore data from an identified backup and roll forward with immutable migrations. Backup automation is outside this local design.
- Failed transactional migration: correct the unapplied migration before sharing it, or add a corrective version if any durable environment recorded it.
- Failed non-transactional migration: investigate actual database state and record a recovery decision before any manual history change.
- Migration history is deployment evidence, not proof that the catalog satisfies logical round-trip or application behavior.

### 4.6 Python and uv project

Use one Python project at the root of the runnable runtime artifact subproject for the first service. The subproject root is `layers/domain-data-dictionary-postgresql-runtime/artifacts/`; it is not the repository root. Additional Python processes may share the package until a real dependency or ownership boundary justifies a uv workspace or separate project.

Planned layout:

```text
pyproject.toml
uv.lock
.python-version
src/
└── domaincatalog_api/
tests/
Dockerfile
compose.yaml
```

Project constraints:

- `.python-version`: `3.14`
- `requires-python`: `>=3.14,<3.15`
- Runtime dependency ranges:
  - `fastapi>=0.139,<0.140`
  - `uvicorn[standard]>=0.51,<0.52`
  - `psycopg[binary]>=3.3,<3.4`
  - `psycopg-pool>=3.3,<3.4`
  - `pydantic-settings>=2.14,<3`
- Initial resolved versions verified during design: FastAPI 0.139.2, Uvicorn 0.51.0, Psycopg 3.3.4, psycopg-pool 3.3.1, and pydantic-settings 2.14.2.
- Development dependency group: pytest, pytest-asyncio, HTTPX, Ruff, and mypy. Exact versions are locked at implementation time.
- Commit `uv.lock`; do not maintain a parallel hand-edited `requirements.txt`.
- CI and container builds use `uv sync --locked`. Dependency upgrades explicitly update and review the lockfile.

### 4.7 API container build

- Base image: `python:3.14.6-slim-trixie`.
- Copy uv from a version-pinned official `ghcr.io/astral-sh/uv` image. The engineer must verify the current immutable digest immediately before implementation; the latest independently confirmed release during this session was 0.11.29.
- Separate dependency installation from source copying so dependency layers remain cacheable.
- Build from the committed lockfile with development dependencies excluded.
- Do not copy the host `.venv`, `.env`, Git data, tests, caches, or supporting documents into the runtime image.
- Run as an unprivileged user and expose container port 8000.
- Use one Uvicorn process in local Compose. Worker count and horizontal scaling are deployment concerns.

FastAPI is selected as an HTTP transport and OpenAPI generator, not as the owner of catalog semantics. Only these operational endpoints are authorized in the scaffold:

- `/health/live`: process is running; it does not require PostgreSQL.
- `/health/ready`: pool is open, a trivial query succeeds, and expected migration state is present.

Product endpoints remain blocked on the capability API design.

### 4.8 Psycopg access

- Use Psycopg 3 directly; do not add SQLAlchemy or an ORM without a demonstrated need.
- Use `AsyncConnectionPool` with `open=False`, open it explicitly in the FastAPI lifespan, wait for initial readiness, and close it on shutdown. This follows the current Psycopg pool contract.
- Make minimum size, maximum size, acquisition timeout, and connection lifetime configurable. Choose measured defaults during implementation tests rather than treating the library defaults as product requirements.
- A request or command obtains a connection through a context manager and owns a clear transaction boundary. Normal exit commits; exception exit rolls back.
- Use bound parameters for values and Psycopg composable SQL for identifiers. Never interpolate untrusted content into SQL text.
- Capability modules call repository interfaces; route handlers do not spread SQL across the transport layer.
- Readiness failure makes the container unhealthy but does not terminate it automatically; the pool may recover when PostgreSQL returns.

### 4.9 Configuration and local secrets

Commit `.env.example`, never `.env`. Compose must fail clearly when the database password is absent. Use the standard local values:

- `POSTGRES_DB` default `domaincatalog`
- `POSTGRES_USER` default `domaincatalog`
- `POSTGRES_PASSWORD` required, no committed default
- `DOMAINCATALOG_POSTGRES_PORT` default `25432`
- `DOMAINCATALOG_API_PORT` default `28000`

The API uses libpq-compatible discrete settings (`PGHOST=postgres`, `PGPORT=5432`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`) to avoid connection-URL encoding errors. Flyway uses the matching internal JDBC address and credentials through `FLYWAY_URL`, `FLYWAY_USER`, and `FLYWAY_PASSWORD`.

One local development login may own migrations and API connections for the first scaffold. That concession is local-only. Before any shared or production-like deployment, separate migration ownership from least-privilege API access and select a real secret-delivery mechanism.

### 4.10 Operational evidence

All services log to stdout/stderr. The first build adds no metrics, tracing, reverse proxy, or log collector. Verification must retain:

- Compose configuration validation;
- exact image tags and resolved image identities;
- Flyway validation and migration results;
- PostgreSQL and API health results;
- empty-database replay results;
- migration re-run no-op result;
- test results; and
- schema inventory used to compare the implementation with `CAT-PHY`.

## 5. Interfaces and Dependencies

| Consumer | Provider | Contract |
| --- | --- | --- |
| `migrate` | `postgres` | PostgreSQL wire protocol on internal `postgres:5432`; starts after database health |
| `api` | `migrate` | Compose completion dependency; API does not start on non-zero migration exit |
| `api` | `postgres` | Psycopg 3 connection pool over internal PostgreSQL; runtime transaction boundary |
| developer tools | `postgres` | Optional host port 25432; not a product interface |
| clients | `api` | Host port 28000; only health endpoints until capability design is accepted |

Direct PostgreSQL access remains administrative and diagnostic. It does not become a second product API.

## 6. Verification Design

The implementation is not complete until it proves:

1. `docker compose config` is valid without exposing a committed password;
2. every image is pinned and available for both development architecture and CI architecture;
3. a fresh volume becomes healthy and accepts the full migration sequence;
4. fresh initialization contains none of the image's `sample_*` tables, `sample_graph`, TIGER helper functions, or unrequested extensions;
5. a second migration run makes no schema changes;
6. `flyway validate` detects a deliberately changed applied migration in an isolated test;
7. migration failure prevents API startup;
8. API liveness remains independent of the database and readiness reflects database/schema availability;
9. database data survives normal container recreation;
10. `uv lock --check`, locked sync, lint, types, and tests pass under Python 3.14;
11. the API image runs unprivileged and contains no development or secret files; and
12. later schema tests reconstruct all six `CAT-LOG` authorities without an undocumented escape field.

## 7. Decisions Explicitly Deferred

- PostgreSQL physical schema and activated extensions
- Separate migration-owner and API-login provisioning outside local development
- FastAPI capability resources and authorization
- Production Compose or orchestrator topology
- TLS, secret manager, backup schedule, point-in-time recovery, replication, and high availability
- Connection-pool sizes and performance targets
- Metrics, tracing, and log aggregation
- Additional worker, importer, exporter, deployment, or observation services
- CI provider and release process

## 8. Open Questions

1. Should provenance be able to target typed `ModelFamily` and `ResponsibleAgent` records, requiring a logical-model revision before physical design?
2. Does the first `CAT-PHY` need any included extension, or should it begin with PostgreSQL core only?
3. Should the API subproject become a uv workspace if a second Python service arrives?

## 9. Accepted Product-Owner Decisions

On 2026-07-26, the product owner accepted:

- Flyway Open Source as the SQL migration runner;
- the `postgres` → `migrate` → `api` Compose dependency topology;
- FastAPI/Uvicorn with async Psycopg pooling for the scaffold;
- a uv project rooted at the runnable subproject;
- the local-only shared database login concession; and
- the recognizable `2xxxx` local port block: PostgreSQL `25432` and API `28000`.

## 10. Recommended Next Step

Execute the source-colocated `domain-data-dictionary-postgresql-runtime` transform and the development checklist only through the infrastructure and health scaffold. In parallel, create the source-owned PostgreSQL physical-model transform; do not author the first product migration until that model is accepted sufficiently to drive DDL.

## 11. Approval Status

Approved for exploratory implementation. This approval does not make the design or its draft upstream sources effective.

## 12. Architect Review

Approved by the human architect on 2026-07-26. The approval applies to the technical design as written, including the accepted product-owner decisions in section 9. It does not make the draft upstream product layers effective.

## 13. Senior Implementation Engineer Review

### Review basis

Reviewed on 2026-07-26 against the approved technical design, the Model C component boundary, the conceptual build constraints, the logical PostgreSQL contract, project `AGENTS.md`, and the flat-layer-graph ADR.

### Findings

- The database, migration, API, configuration, persistence, startup, failure, and verification behavior is concrete enough to implement without guessing at critical runtime semantics.
- The design keeps product DDL and capability behavior outside the scaffold and therefore preserves the owning physical-model and API-design boundaries.
- The design leaves appropriate engineering discretion for pool sizing, internal module decomposition, test implementation, and later service separation.
- `IR-001` — blocking: the design places `pyproject.toml`, `src/`, `Dockerfile`, and `compose.yaml` at repository root, but the governing flat-layer layout says each product refinement is represented by a sibling layer and requires a source-colocated outbound transform before a child layer is created. The design layer currently has neither an outbound transform nor a named runnable target layer. Coding at repository root now would create an unnamed downstream refinement whose authority, regeneration boundary, and stale-descendant behavior are unclear.

### Required change

Before runtime files are created, the architect must select and record one coherent artifact boundary:

1. create a named sibling runtime layer and place the uv project and executable artifacts inside that layer; or
2. create a named sibling runtime layer whose source-colocated transform explicitly owns a repository-root executable projection, including an exhaustive manifest of projected files and regeneration rules.

The first option fits the flat-layer ADR more directly but revises the accepted root uv location. The second preserves a root uv project but introduces a split physical boundary that must be justified and kept mechanically explicit.

### Resolution

The human architect resolved `IR-001` on 2026-07-26: “root uv project” means the root of the runnable subproject. The named target is `domain-data-dictionary-postgresql-runtime`, its uv and executable artifact root is `layers/domain-data-dictionary-postgresql-runtime/artifacts/`, and the source-colocated transform is held under this design layer. No repository-root executable projection is authorized.

### Questions

- Is “root uv project” a stronger constraint than keeping all implementation artifacts physically within the runnable layer directory?
- If root placement is retained, which files are authoritative layer artifacts and which are generated projections?

### Review disposition

Accepted after resolution of `IR-001`. No blocking implementation finding remains.

## 14. Product Owner Review

Approved the decisions recorded in section 9 on 2026-07-26.

## 15. Sign-Off

### Author

- Signer: Codex
- Signer type: agent
- Role: technical design author
- Review perspective: systems engineering technical design
- Disposition: submitted for review
- Date: 2026-07-26

### Review Entries

- Reviewer: product owner (human)
- Date: 2026-07-26
- Disposition: approved the migration runner, service topology, API stack, root uv project, local shared database login, and local port block
- Remaining scope: none from product-owner review

- Reviewer: project architect (human)
- Date: 2026-07-26
- Disposition: approved the technical design
- Remaining scope: implementation-engineering review

- Reviewer: Codex
- Signer type: agent
- Role: senior implementation engineer
- Date: 2026-07-26
- Disposition: accepted after architect resolution
- Finding resolution: `IR-001` resolved by making the named runtime layer's `artifacts/` directory the uv subproject root

### Product Owner Sign-Off

- Signer: product owner (human)
- Status: approved decisions in section 9 on 2026-07-26

### Workflow Status

- Current status: approved for exploratory runtime implementation
