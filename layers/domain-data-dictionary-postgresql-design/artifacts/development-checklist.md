# Domain Data Dictionary PostgreSQL Development Checklist

## Document Status

- Status: active pre-implementation checklist
- Execution status: architecture approved; blocked on implementation finding `IR-001`
- Last updated: 2026-07-26
- Source technical design: `technical-design.md`, product-owner decisions approved 2026-07-26
- Source logical revision: `f71a279`
- Intended audience: implementation engineers and reviewing agents

## 1. Purpose

Translate the PostgreSQL technical design into ordered, verifiable implementation work without expanding the physical data model or API capability scope.

## 2. Scope

This checklist covers a local Compose scaffold containing PostgreSQL, Flyway, and a Python API with operational health behavior. It is the shared execution record: engineers check an item only after its completion evidence exists. It does not authorize product DDL or capability endpoints. Those enter the checklist only after their owning physical-model and API designs are accepted.

## 3. Inputs Consulted

- [PostgreSQL technical design](technical-design.md)
- `CAT-LOG/domain-data-dictionary@1` at revision `f71a279`
- Model C component design at revision `5a0993d`
- source [migration-tool assessment](../../domain-data-dictionary-logical-model/transforms/domain-data-dictionary-postgresql-design/migration-tool-assessment.md)
- local image inspection and current primary documentation recorded in the technical design

## 4. Governing Inputs

The product owner approved the technology, topology, organization, local-login, and port decisions on 2026-07-26. The architect approved the technical design on 2026-07-26. Phase 1 and later remain blocked until implementation finding `IR-001` resolves the conflict between the root uv layout and the required named runnable layer and outbound transform.

## 5. Checklist Conventions

- `[x]` means completion is supported by an artifact, review entry, command result, or other named evidence.
- `[ ]` means incomplete or not yet evidenced; it does not mean work was attempted.
- Complete items in order unless the checklist explicitly identifies an independent track.
- Record verification evidence in the repository before marking implementation or verification items complete.
- Do not mark a downstream item complete merely because its upstream design was accepted.

## 6. Sequencing Decisions

- Build and verify the runtime scaffold before adding product schema.
- Make PostgreSQL health a prerequisite for migrations and successful migrations a prerequisite for API startup.
- Establish the uv lock and container build before application behavior grows.
- Test migration failure and empty-database replay before trusting a persistent developer volume.
- Do not activate included PostgreSQL extensions until the physical model requires them.
- Do not add product endpoints before the capability API design owns their semantics.

## 7. Phase 0 — Approval Gates

- [x] Product owner selected Flyway Open Source; Sqitch remains the documented alternative.
- [x] Product owner accepted FastAPI/Uvicorn and async Psycopg pooling.
- [x] Product owner accepted the three-service Compose topology.
- [x] Product owner accepted root-level uv project organization.
- [x] Product owner accepted a local shared database login.
- [x] Product owner accepted the recognizable `2xxxx` port block: PostgreSQL `25432`, API `28000`.
- [x] Architect approval is recorded in `technical-design.md`.
- [x] Senior implementation engineer review is recorded in `technical-design.md`.
- [ ] All blocking review findings are resolved at the owning layer.

Completion evidence:

- [ ] Technical design status permits implementation.
- [x] Accepted product decisions and exact source revision are recorded before runtime files are created.

## 8. Phase 1 — Repository and Python Project Scaffold

Planned files:

- `pyproject.toml`
- `uv.lock`
- `.python-version`
- `.env.example`
- `.dockerignore`
- `Dockerfile`
- `compose.yaml`
- `src/domaincatalog_api/__init__.py`
- `src/domaincatalog_api/main.py`
- `src/domaincatalog_api/settings.py`
- `src/domaincatalog_api/database.py`
- `tests/`
- `infra/postgres/initdb/README.md`
- `infra/flyway/flyway.toml`
- `infra/flyway/migrations/`

Tasks:

- [ ] Confirm the working tree and preserve `supporting_documents/` and all unrelated user changes.
- [ ] Initialize a packaged uv project without replacing project-layer documentation.
- [ ] Set `.python-version` to `3.14` and `requires-python` to `>=3.14,<3.15`.
- [ ] Add the accepted runtime dependency ranges from the technical design.
- [ ] Add pytest, pytest-asyncio, HTTPX, Ruff, and mypy to a development dependency group.
- [ ] Generate and commit `uv.lock`; do not create a second manually maintained dependency lock.
- [ ] Configure `src/` package discovery and one API entry point.
- [ ] Ignore `.venv`, `.env`, Python caches, test caches, build artifacts, and local Compose overrides.
- [ ] Add `.dockerignore` exclusions for the same local artifacts plus `.git`, tests where not needed at runtime, project support material, and secrets.

Verification:

- [ ] `uv lock --check` passes.
- [ ] `uv sync --locked` produces a Python 3.14 environment.
- [ ] Importing Psycopg reports the binary implementation selected for the final application.
- [ ] Package import and empty test collection work from a clean environment.

## 9. Phase 2 — API Operational Scaffold

- [ ] Create FastAPI application construction without product routes.
- [ ] Implement `/health/live` without a database dependency.
- [ ] Implement settings from explicit environment variables; reject missing required database settings.
- [ ] Create `AsyncConnectionPool` with `open=False` and explicit application lifespan open/wait/close behavior.
- [ ] Implement `/health/ready` using a checked-out connection, trivial query, and expected Flyway-history/schema condition.
- [ ] Keep database access behind a repository boundary; route modules contain no durable business SQL.
- [ ] Define transaction context behavior and test commit and rollback paths.
- [ ] Ensure logs go to stdout/stderr and never print credentials or full connection strings.

Verification:

- [ ] Unit test liveness without PostgreSQL.
- [ ] Unit test settings failures and secret redaction.
- [ ] Integration test readiness success and database-unavailable failure.
- [ ] Integration test pool startup and graceful shutdown.
- [ ] Integration test transaction commit on success and rollback on exception.
- [ ] Ruff, mypy, and pytest pass through `uv run`.

## 10. Phase 3 — Reproducible API Image

- [ ] Pin `python:3.14.6-slim-trixie`.
- [ ] Re-query the official uv release and image digest immediately before implementation.
- [ ] Copy uv from the accepted immutable official image reference.
- [ ] Install locked production dependencies in a cacheable layer.
- [ ] Copy and install the application after dependency sync.
- [ ] Create and run as an unprivileged runtime user.
- [ ] Expose internal port 8000 and use the accepted Uvicorn entry point.
- [ ] Ensure no compiler, package cache, development dependency, local virtual environment, `.env`, or Git metadata remains in the final image.

Verification:

- [ ] Image builds from a clean checkout using the lockfile only.
- [ ] Image reports Python 3.14.6 and the locked Psycopg 3 version.
- [ ] Runtime process is non-root.
- [ ] Container starts with valid configuration and fails clearly with missing required configuration.
- [ ] Image inspection finds no committed secret or local `.env` content.

## 11. Phase 4 — Flyway Project and Migration Service

- [ ] Pin `flyway/flyway:13.0.0`.
- [ ] Create non-secret `flyway.toml` with versioned migration location, history behavior, and clean disabled.
- [ ] Mount the Flyway project read-only into the one-shot service.
- [ ] Supply JDBC connection settings through environment variables using the internal PostgreSQL address.
- [ ] Set restart behavior to `no` and depend on PostgreSQL health.
- [ ] Establish the UTC timestamp migration naming convention in contributor instructions.
- [ ] Leave the product migration directory empty until the PostgreSQL physical model is approved.

Physical-model gate:

- [ ] A reviewed `CAT-PHY` artifact maps all six logical authorities.
- [ ] Every planned extension, schema, table, identifier, reference, constraint, and index traces to that model.
- [ ] Only after that gate, author the initial versioned SQL migration.

Migration verification after the physical-model gate:

- [ ] A fresh database applies the entire sequence successfully.
- [ ] A second migrate invocation is a no-op.
- [ ] `flyway validate` succeeds against unchanged migrations.
- [ ] An isolated test proves validation fails when an applied migration is altered.
- [ ] An isolated transactional failure leaves no partial product objects.
- [ ] No migration depends on `/docker-entrypoint-initdb.d` having run beyond standard database initialization.

## 12. Phase 5 — Docker Compose Topology

- [ ] Define `postgres`, `migrate`, and `api` services without global `container_name` values.
- [ ] Pin all images and the API build definition.
- [ ] Mount `postgres_data` at `/var/lib/postgresql`.
- [ ] Override the PostgreSQL command with plain `postgres` so AGE is not preloaded without a physical-model requirement.
- [ ] Mount the documentation-only `infra/postgres/initdb/` directory over the image's initialization directory to suppress baked extensions and demonstration objects.
- [ ] Verify the shadow directory contains no executable `.sql` or `.sh` bootstrap content.
- [ ] Configure PostgreSQL health for the selected database and user.
- [ ] Configure `migrate` to wait for healthy PostgreSQL.
- [ ] Configure `api` to wait for successful migration completion.
- [ ] Publish configurable defaults in the accepted `2xxxx` block: PostgreSQL `25432` and API `28000`.
- [ ] Keep internal connections on `postgres:5432`; never use the host-mapped port between services.
- [ ] Add `.env.example` with names and explanations but no working password.
- [ ] Require the local password rather than supplying a committed default.
- [ ] Preserve the named volume during normal down, rebuild, and recreate operations.

Verification:

- [ ] `docker compose config -q` passes with a supplied local environment.
- [ ] No secret is present in committed Compose or configuration files.
- [ ] Startup order is observable: healthy PostgreSQL, successful migration, then healthy API.
- [ ] A fresh volume contains none of the image's sample tables, sample AGE graph, TIGER helper functions, or unrequested extensions.
- [ ] A deliberately failing migration prevents API startup.
- [ ] API liveness and readiness report the designed states.
- [ ] Normal container recreation preserves a test record.
- [ ] Compose shutdown does not remove the named volume.

## 13. Phase 6 — Clean-Room and Architecture Verification

- [ ] Run the full build on an isolated Compose project name and disposable test volume.
- [ ] Rebuild from no Python environment, no API image, and an empty database.
- [ ] Run locked dependency sync, static checks, unit tests, integration tests, Compose validation, image build, migrations, and health checks.
- [ ] Capture exact image tags and resolved digests.
- [ ] Inventory the resulting PostgreSQL schemas and objects.
- [ ] Compare that inventory with the accepted `CAT-PHY`; fail on undocumented objects other than PostgreSQL and Flyway operational metadata.
- [ ] Round-trip representative `CMOF-GOV`, `DML-DEF`, `CAT-CON`, and `CAT-LOG` content when the schema implementation exists.
- [ ] Confirm no `BDM-DATA` was introduced into catalog storage by tests or fixtures.
- [ ] Remove only the explicitly disposable test volume after recording results.

## 14. Completion Criteria

The scaffold is complete when:

- [ ] all approved Phase 0 decisions are recorded;
- [ ] the committed uv project reproduces under Python 3.14 from `uv.lock`;
- [ ] the API image is pinned, non-root, and contains only runtime material;
- [ ] PostgreSQL, migration, and API services satisfy the designed dependency and health behavior;
- [ ] migration history validates and replays from empty state;
- [ ] persistent data survives normal recreation;
- [ ] failures are visible and block dependent startup;
- [ ] no product DDL exists without an accepted physical-model source; and
- [ ] no product API behavior exists without an accepted capability source.

## 15. Decisions Explicitly Deferred

- Physical schema and extension activation
- Product API contract and authorization
- Production credentials, roles, TLS, secrets, backup, and high availability
- Additional services and uv workspace conversion
- Performance targets and connection-pool sizing
- CI and release automation

## 16. Open Questions

The remaining open questions in technical-design section 8 remain authoritative. The accepted Flyway, local-login, and port decisions are no longer open questions. Engineers must not resolve the remaining questions implicitly in code or configuration.

## 17. Recommended Next Step

Resolve `IR-001`, create the source-colocated outbound transform for the named runnable sibling layer, and then execute Phase 1 through the operational scaffold while the physical-model transform is designed separately.

## 18. Approval Status

Architecture approved; execution blocked on implementation finding `IR-001`.

## 19. Product Owner Review

Approved Flyway, FastAPI/Uvicorn with async Psycopg, the three-service Compose topology, the root uv project, a local shared database login, and ports `25432`/`28000` on 2026-07-26.

## 20. Sign-Off

### Author

- Signer: Codex
- Signer type: agent
- Role: development checklist author
- Review perspective: implementation planning
- Disposition: updated after product-owner decision
- Date: 2026-07-26

### Review Entries

- Reviewer: product owner (human)
- Date: 2026-07-26
- Disposition: approved the six Phase 0 product decisions

- Reviewer: project architect (human)
- Date: 2026-07-26
- Disposition: approved the technical design

- Reviewer: Codex
- Role: senior implementation engineer
- Date: 2026-07-26
- Disposition: changes required before implementation; see technical-design finding `IR-001`

### Product Owner Sign-Off

- Signer: product owner (human)
- Status: approved product decisions on 2026-07-26

### Workflow Status

- Current status: active checklist; runtime artifact-boundary decision remains open
