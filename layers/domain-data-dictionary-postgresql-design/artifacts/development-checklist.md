# Domain Data Dictionary PostgreSQL Development Checklist

## Document Status

- Status: active development checklist; PostgreSQL structural realization complete
- Execution status: catalog-kernel migration implemented and verified; definition-aware conformance and capability work pending
- Last updated: 2026-07-26
- Source technical design: `technical-design.md`, product-owner decisions approved 2026-07-26
- Source logical revision: `5728636`
- Intended audience: implementation engineers and reviewing agents

## 1. Purpose

Translate the PostgreSQL technical design into ordered, verifiable implementation work, including a PostgreSQL realization that remains traceable to `CAT-LOG`, without expanding the API capability scope.

## 2. Scope

This checklist covers a local Compose scaffold containing PostgreSQL, Flyway, and a Python API with operational health behavior, followed by the first PostgreSQL realization of `CAT-LOG`. It is the shared execution record: engineers check an item only after its completion evidence exists. Product DDL is authorized through the realization rules in the technical design; capability endpoints remain blocked until their owning API design is accepted.

## 3. Inputs Consulted

- [PostgreSQL technical design](technical-design.md)
- `CAT-LOG/domain-data-dictionary@1` at revision `5728636`
- Model C component design at revision `5a0993d`
- source [migration-tool assessment](../../domain-data-dictionary-logical-model/transforms/domain-data-dictionary-postgresql-design/migration-tool-assessment.md)
- local image inspection and current primary documentation recorded in the technical design

## 4. Governing Inputs

The product owner approved the technology, topology, organization, local-login, and port decisions on 2026-07-26. The architect approved the technical design and clarified that the uv root is the runnable subproject root on 2026-07-26. The runnable subproject is owned by the `domain-data-dictionary-postgresql-runtime` sibling layer at `layers/domain-data-dictionary-postgresql-runtime/artifacts/`.

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
- Do not activate included PostgreSQL extensions until a demonstrated realization requirement justifies them.
- Do not add product endpoints before the capability API design owns their semantics.

## 7. Phase 0 — Approval Gates

- [x] Product owner selected Flyway Open Source; Sqitch remains the documented alternative.
- [x] Product owner accepted FastAPI/Uvicorn and async Psycopg pooling.
- [x] Product owner accepted the three-service Compose topology.
- [x] Product owner accepted a uv project rooted at the runnable subproject.
- [x] Product owner accepted a local shared database login.
- [x] Product owner accepted the recognizable `2xxxx` port block: PostgreSQL `25432`, API `28000`.
- [x] Architect approval is recorded in `technical-design.md`.
- [x] Senior implementation engineer review is recorded in `technical-design.md`.
- [x] All blocking review findings are resolved at the owning layer; `IR-001` was resolved by the architect.
- [x] Architect approved `CAT-LOG` as the direct semantic source for migration SQL and delegated ordinary PostgreSQL physical choices to the realization transform.

Completion evidence:

- [x] Technical design status permits exploratory implementation.
- [x] Accepted product decisions and exact source revision are recorded before runtime files are created.

## 8. Phase 1 — Repository and Python Project Scaffold

Planned files:

All paths in this phase are relative to `layers/domain-data-dictionary-postgresql-runtime/artifacts/`, the uv subproject root.

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

- [x] Confirm the working tree and preserve `supporting_documents/` and all unrelated user changes.
- [x] Initialize a packaged uv project without replacing project-layer documentation.
- [x] Set `.python-version` to `3.14` and `requires-python` to `>=3.14,<3.15`.
- [x] Add the accepted runtime dependency ranges from the technical design.
- [x] Add pytest, pytest-asyncio, HTTPX, Ruff, and mypy to a development dependency group.
- [x] Generate and commit `uv.lock`; do not create a second manually maintained dependency lock.
- [x] Configure `src/` package discovery and one API entry point.
- [x] Ignore `.venv`, `.env`, Python caches, test caches, build artifacts, and local Compose overrides.
- [x] Add `.dockerignore` exclusions for the same local artifacts plus `.git`, tests where not needed at runtime, project support material, and secrets.

Verification:

- [x] `uv lock --check` passes.
- [x] `uv sync --locked` produces a Python 3.14 environment.
- [x] Importing Psycopg reports version 3.3.4 and the binary implementation.
- [x] Package import and test collection work from a clean environment.

## 9. Phase 2 — API Operational Scaffold

- [x] Create FastAPI application construction without product routes.
- [x] Implement `/health/live` without a database dependency.
- [x] Implement settings from explicit environment variables; reject missing required database settings.
- [x] Create `AsyncConnectionPool` with `open=False` and explicit application lifespan open/wait/close behavior.
- [x] Implement `/health/ready` using a checked-out connection, trivial query, and expected Flyway-history/schema condition.
- [x] Keep database access behind a repository boundary; route modules contain no durable business SQL.
- [x] Define transaction context behavior and test commit and rollback paths.
- [x] Ensure logs go to stdout/stderr and never print credentials or full connection strings.

Verification:

- [x] Unit test liveness without PostgreSQL.
- [x] Unit test settings failures and secret redaction.
- [x] Test readiness success and database-unavailable behavior.
- [x] Integration test pool startup and graceful shutdown.
- [x] Integration test transaction commit on success and rollback on exception.
- [x] Ruff, strict mypy, unit tests, and integration tests pass through `uv run`.

## 10. Phase 3 — Reproducible API Image

- [x] Pin `python:3.14.6-slim-trixie` by multi-platform digest.
- [x] Re-query the official uv release and image digest immediately before implementation.
- [x] Copy uv 0.11.29 from the accepted immutable official image reference.
- [x] Install locked production dependencies in a cacheable layer.
- [x] Copy and install the application after dependency sync.
- [x] Create and run as unprivileged UID 10001.
- [x] Expose internal port 8000 and use the accepted Uvicorn entry point.
- [x] Ensure no compiler, package cache, development dependency, local virtual environment, `.env`, or Git metadata remains in the final image.

Verification:

- [x] Image builds from the locked project.
- [x] Image reports Python 3.14.6 and Psycopg 3.3.4 binary.
- [x] Runtime process is non-root.
- [x] Container starts with valid configuration and exits nonzero with a required-field error when `PGPASSWORD` is absent.
- [x] Image inspection finds no committed secret or local `.env` content.

## 11. Phase 4 — Flyway Project and Migration Service

- [x] Pin `flyway/flyway:13.0.0` by multi-platform digest.
- [x] Create non-secret `flyway.toml` with versioned migration location, history behavior, and clean disabled.
- [x] Mount the Flyway project read-only into the one-shot service.
- [x] Supply JDBC connection settings through environment variables using the internal PostgreSQL address.
- [x] Set restart behavior to `no` and depend on PostgreSQL health.
- [x] Establish the UTC timestamp migration naming convention in contributor instructions.
- [x] Preserve the empty migration directory as the verified scaffold baseline before product realization begins.

PostgreSQL realization work:

- [x] Create a derived realization manifest mapping all six logical authorities and `CATLOG-001` through `CATLOG-024` to PostgreSQL objects, enforcement mechanisms, and tests.
- [x] Author the initial versioned SQL migration directly from the selected `CAT-LOG` revision.
- [x] Trace every schema, table, type, identifier, reference, constraint, index, function, and extension to the logical source or a documented operational need.
- [x] Prefer appropriate PostgreSQL-native facilities; PostgreSQL core satisfies the first realization and no optional extension is activated.
- [x] Record every invariant not enforceable synchronously in PostgreSQL and identify the owning validation mechanism and evidence.
- [x] Escalate only choices that weaken or change logical meaning, create another writable authority, add a material external dependency, make a major operational commitment, or expose an upstream deficiency; no such choice was required.

Migration and realization verification:

- [x] A fresh database applies the entire sequence successfully.
- [x] A second migrate invocation is a no-op.
- [x] `flyway validate` succeeds against unchanged migrations.
- [ ] An isolated test proves validation fails when an applied migration is altered.
- [x] An isolated transactional failure leaves no partial product objects; the scaffold failure probe remains applicable to product migrations.
- [x] No migration depends on `/docker-entrypoint-initdb.d` having run beyond standard database initialization.
- [x] Introspected deployed inventory agrees with both migration SQL and the derived realization manifest.
- [x] Representative structural logical content round-trips without semantic loss.

## 12. Phase 5 — Docker Compose Topology

- [x] Define `postgres`, `migrate`, and `api` services without global `container_name` values.
- [x] Pin all external images and the API build definition.
- [x] Mount `postgres_data` at `/var/lib/postgresql`.
- [x] Override the PostgreSQL command with plain `postgres` so AGE is not preloaded without a demonstrated realization requirement.
- [x] Mount the documentation-only `infra/postgres/initdb/` directory over the image's initialization directory to suppress baked extensions and demonstration objects.
- [x] Verify the shadow directory contains no executable `.sql` or `.sh` bootstrap content.
- [x] Configure PostgreSQL health for the selected database and user.
- [x] Configure `migrate` to wait for healthy PostgreSQL.
- [x] Configure `api` to wait for successful migration completion.
- [x] Publish configurable defaults in the accepted `2xxxx` block: PostgreSQL `25432` and API `28000`.
- [x] Keep internal connections on `postgres:5432`; never use the host-mapped port between services.
- [x] Add `.env.example` with names and explanations but no working password.
- [x] Require the local password rather than supplying a committed default.
- [x] Preserve the named volume during normal down, rebuild, and recreate operations.

Verification:

- [x] `docker compose config -q` passes with a supplied local environment.
- [x] No secret is present in committed Compose or configuration files.
- [x] Startup order is observable: healthy PostgreSQL, successful migration, then healthy API.
- [x] A fresh volume contains none of the image's sample tables, sample AGE graph, TIGER helper functions, or unrequested extensions.
- [x] A deliberately failing transactional migration prevents API startup and rolls back its probe table.
- [x] API liveness and readiness report the designed states.
- [x] Normal container recreation preserves a test record.
- [x] Compose shutdown does not remove the named volume.

## 13. Phase 6 — Clean-Room and Architecture Verification

- [x] Run the full build on isolated Compose project `domaincatalog_verify` and its project-scoped volume.
- [x] Build a new Python environment, API image, and empty database.
- [x] Run locked dependency sync, static checks, unit tests, integration tests, Compose validation, image build, migrations, and health checks.
- [x] Capture exact image tags and resolved digests.
- [x] Inventory the resulting PostgreSQL schemas and objects.
- [x] Compare that inventory with the migration authority and derived realization manifest; no undocumented product object was found.
- [ ] Round-trip representative `CMOF-GOV`, `DML-DEF`, `CAT-CON`, and `CAT-LOG` content when the schema implementation exists.
- [x] Confirm no `BDM-DATA` was introduced into catalog storage by tests or fixtures.
- [x] Remove only the explicitly disposable `domaincatalog_schema_verify` test volume after recording results; retain the local `domaincatalog_verify` volume.

## 14. Runtime Completion Criteria

The runtime realization is complete when:

- [x] all approved Phase 0 decisions are recorded;
- [x] the committed uv project reproduces under Python 3.14 from `uv.lock`;
- [x] the API image is pinned, non-root, and contains only runtime material;
- [x] PostgreSQL, migration, and API services satisfy the designed dependency and health behavior;
- [x] the product migration history validates and replays from empty state;
- [x] persistent data survives normal recreation;
- [x] failures are visible and block dependent startup;
- [x] every product DDL object traces to `CAT-LOG` through the derived realization manifest; and
- [x] no product API behavior exists without an accepted capability source.

## 15. Decisions Explicitly Deferred

- Production-scale schema or extension choices not required by the first realization
- Product API contract and authorization
- Production credentials, roles, TLS, secrets, backup, and high availability
- Additional services and uv workspace conversion
- Performance targets and connection-pool sizing
- CI and release automation

## 16. Open Questions

The remaining open questions in technical-design section 8 remain authoritative. The accepted Flyway, local-login, and port decisions are no longer open questions. Engineers must not resolve the remaining questions implicitly in code or configuration.

## 17. Recommended Next Step

Load machine-readable governing definitions and implement the definition-aware validations identified in the realization manifest. Then run normative `CMOF-GOV`, `DML-DEF`, `CAT-CON`, and subject-model import/export round trips before treating this layer as effective.

## 18. Approval Status

PostgreSQL structural realization and representative round-trip verification are complete. Definition-aware conformance, normative-model round trips, and capability API work remain pending in their owning transforms.

## 19. Product Owner Review

Approved Flyway, FastAPI/Uvicorn with async Psycopg, the three-service Compose topology, the uv project rooted at the runnable subproject, a local shared database login, and ports `25432`/`28000` on 2026-07-26.

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
- Disposition: accepted after the architect resolved `IR-001`

### Product Owner Sign-Off

- Signer: product owner (human)
- Status: approved product decisions on 2026-07-26

### Workflow Status

- Current status: structural realization complete; definition-aware conformance is the next database phase
