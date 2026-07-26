# SQL Migration Tool Assessment

## Status and Decision

- Assessment date: 2026-07-26
- Source logical revision: `f71a279`
- Decision: use Flyway Open Source `13.0.0` for the first implementation
- Serious alternative: Sqitch
- Reconsider when: cross-project database-change dependencies or mandatory per-change deploy/revert/verify scripts outweigh Flyway's simpler versioned flow

## Decision Criteria

The tool must:

1. treat PostgreSQL SQL as the migration authority;
2. run independently of the Python API and any ORM;
3. work as a one-shot Docker Compose service on arm64 and amd64;
4. record applied history and detect changed or missing migrations;
5. serialize concurrent migration attempts;
6. fail the API startup path when migration fails; and
7. remain understandable without a database-management SaaS product.

## Comparison

| Tool | Strengths for this project | Costs or weaknesses | Judgment |
| --- | --- | --- | --- |
| Flyway Open Source 13.0.0 | Plain versioned SQL; official multi-architecture image; PostgreSQL 18 support; ordered execution; schema-history records with applied checksums; explicit validation; conventional one-shot Compose operation | Java-based image is comparatively large; dependency modeling is sequence-based; robust rollback remains a project discipline rather than something to delegate blindly to undo scripts | Selected. Best balance of integrity evidence, familiarity, and low project ceremony |
| Sqitch | Native `psql` scripts; explicit plan and dependencies; separate deploy, revert, and verify scripts; advisory locking and deployment-integrity tracking | At least three scripts per change plus a plan; substantially more authoring and review surface; the extra control is not yet justified by the first local deployment | Retain as the alternative if migration dependencies or formal verification become central |
| dbmate | Very small standalone tool; plain SQL; timestamp versions; transactional up/down sections; schema dump; official container | Its migration table records the version rather than the applied SQL content; strict ordering is optional; therefore it supplies weaker evidence that an applied migration still matches source control | Not selected for this governed catalog |

Alembic is not shortlisted. It would couple migration ownership to Python and commonly to SQLAlchemy, while the selected database access is direct Psycopg and the requirement is SQL-authored migration authority.

## Flyway Operating Profile

- Use `flyway/flyway:13.0.0`, not a mutable major or `latest` tag.
- Use versioned SQL migrations named `V<UTC timestamp>__<description>.sql`.
- Do not introduce repeatable migrations initially; use another versioned migration so history remains explicit.
- Treat an applied versioned file as immutable. Corrections roll forward in a new migration.
- Run `validate` in verification and CI. Do not normalize checksum failures with `repair` unless an investigated recovery decision records why history is being changed.
- Keep `clean` disabled outside deliberately disposable test databases.
- Let each PostgreSQL-compatible migration execute transactionally by default. Any non-transactional exception requires a script-local setting and review rationale.
- Use an empty-database replay as a required verification, not only incremental application to one developer volume.
- Do not use `/docker-entrypoint-initdb.d` for evolving catalog schema. Entrypoint initialization runs only for a fresh volume and cannot supply migration history.

## Rollback Policy

Local disposable databases may be rebuilt from an empty named volume after explicit destructive intent. Shared or durable environments roll forward with a corrective migration. A migration that may destroy or rewrite data requires an explicit backup/recovery plan and review before execution. Migration success records schema change; it does not prove that application semantics or logical round-trip obligations are satisfied.

## Primary Sources

- [Flyway Docker and Compose use](https://documentation.red-gate.com/flyway/reference/usage/flyway-docker)
- [Flyway versioned migrations and checksum rule](https://documentation.red-gate.com/fd/versioned-migrations-273973333.html)
- [Flyway validation behavior](https://documentation.red-gate.com/flyway/reference/commands/validate)
- [Flyway schema-history semantics](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/flyway-schema-history-table)
- [Flyway PostgreSQL version support](https://documentation.red-gate.com/fd/supported-databases-for-flyway-143754067.html)
- [Flyway Open Source 13.0.0 image](https://hub.docker.com/r/flyway/flyway/tags)
- [Sqitch model and dependency behavior](https://sqitch.org/docs/manual/sqitch/)
- [Sqitch deploy and verification behavior](https://sqitch.org/docs/manual/sqitch-deploy/)
- [dbmate behavior and migration record](https://github.com/amacneil/dbmate)
