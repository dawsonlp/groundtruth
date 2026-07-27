# PostgreSQL Realization Verification

## Status and Basis

- Verification status: structural realization passed
- Runtime effectiveness: no
- Logical source revision: `5728636`
- Source design revision: `f10afc7`
- Runtime-transform specification revision: `a56b2c3`
- Catalog-kernel implementation revision: `90d3dc9`
- Complete-inventory implementation revision: `949d079`
- Verification date: 2026-07-26
- Target: PostgreSQL 18.4

This evidence verifies the PostgreSQL structural realization described by `artifacts/infra/postgres/realization-manifest.md`. It does not claim full CMOF/DML conformance because the machine-readable governing definitions and definition-aware validator do not yet exist.

## Clean-Room Execution

An isolated Compose project named `domaincatalog_schema_verify` was created with a new project-scoped PostgreSQL volume. Its temporary host ports were PostgreSQL `25434` and API `28002`, avoiding the retained local instance on `25432` and `28000`.

Observed clean startup order:

1. PostgreSQL 18.4 initialized a new empty volume and became healthy.
2. Flyway validated one migration and created `public.flyway_schema_history`.
3. Flyway applied `V202607260001__create_catalog_kernel.sql` and `V202607260002__complete_catalog_inventory.sql` transactionally in sequence; the clean two-migration run completed in 0.030 seconds.
4. The API started after migration success and became healthy.

The migration created schema `catalog` and did not depend on executable content in `/docker-entrypoint-initdb.d`.

## Migration Repeatability and Validation

- Initial replay: both migrations passed from an empty database at version `202607260002`.
- Second `migrate` invocation: passed as a no-op with `Schema "public" is up to date`.
- Explicit `flyway validate`: passed with two unchanged migrations.
- Flyway history: successful rows for `202607260001 - create catalog kernel` and `202607260002 - complete catalog inventory`.
- Failure behavior: the earlier scaffold verification proved a transactional Flyway failure blocks API startup and leaves no partial probe table; the same Flyway transaction policy applies to this migration.

Checksum-tampering detection was not repeated against this product migration. The checklist leaves that isolated test open rather than treating Flyway's documented behavior as new execution evidence.

## Automated Verification

Static and local checks:

- `uv run ruff check .`: passed.
- `uv run mypy src tests`: passed in strict mode for eight source/test modules.
- Unit tests without a database: six passed.

Complete suite against the isolated clean database:

- 13 tests passed.
- Seven live PostgreSQL integration tests passed.
- API `/health/ready` returned `{"status":"ready"}`.

The catalog-specific integration tests demonstrated:

- all six logical authorities persist and reconstruct through their authoritative tables;
- the four identified authority kinds share one global catalog-identifier namespace;
- model-family membership, responsible-agent evidence, and sealed provenance reconstruct exactly;
- reference and value property occurrences remain distinct;
- recursive values reconstruct through derived paths without storing a competing path value;
- incomplete value occurrences fail deferred validation;
- incomplete provenance records fail deferred validation;
- sealed provenance and its dependent records are immutable; and
- disconnected value-tree cycles fail deferred validation.

All test content ran inside rollback-only transactions. No representative record remained in the database after verification.

## Deployed Inventory

The named `catalog.deployed_object_inventory` profile reported:

| Object kind | Count |
| --- | ---: |
| Columns | 121 |
| Constraints | 113 |
| Functions | 9 |
| Indexes | 30 |
| Relations, including tables, views, indexes, and the value-node identity sequence | 44 |
| Schemas | 1 |
| Triggers | 23 |
| Types, including table row types, domains, enums, and arrays | 34 |

The eleven authoritative and supporting product tables are:

- `catalog_object`
- `catalog_record`
- `model_family`
- `model_family_model_revision`
- `property_occurrence`
- `provenance_record`
- `provenance_responsible_agent`
- `provenance_source_reference`
- `provenance_subject`
- `responsible_agent`
- `value_node`

The inventory also contains the two declared read-only views, physical enum/domain types, trigger functions, identity sequence, declared constraints, and indexes produced by the migration. PostgreSQL and Flyway operational metadata remain outside schema `catalog`.

Only the core `plpgsql` extension is installed. PostGIS, pgvector, AGE, pgRouting, sample tables, sample graph, TIGER helpers, and `BDM-DATA` are absent.

## Traceability Result

The realization manifest maps:

- the three typed authorities (`ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord`);
- the three reflective authorities (`CatalogObject`, `PropertyOccurrence`, and `ValueNode`);
- every logical datatype used by those authorities; and
- every integrity rule from `CATLOG-001` through `CATLOG-024`.

The manifest distinguishes database enforcement, partial structural enforcement, definition-aware validation, capability-transaction enforcement, and verification. No PostgreSQL object is treated as permission to weaken a rule that cannot yet be enforced.

## Remaining Validation

The runtime remains draft and non-effective. The following are not demonstrated:

- loading the actual machine-readable `CMOF-GOV` and `DML-DEF` closures;
- definition-aware property applicability, inheritance, multiplicity, semantic uniqueness, composition, and type conformance;
- datatype-specific recursive value validation driven by the loaded definition;
- accepted-artifact closure and immutability beyond sealed provenance;
- governed realization/supersession acyclicity and target-profile semantics;
- generated typed capability projections; and
- lossless import/export of normative `CMOF-GOV`, `DML-DEF`, `CAT-CON`, and a subject model.

These are upstream-dependent conformance work, not defects concealed by the physical realization.

## Retained Local Runtime

The pre-existing `domaincatalog_verify` local instance on PostgreSQL port `25432` and API port `28000` was migrated successfully to `202607260002`. All seven live integration tests also passed against it. Its named volume remains retained.

The disposable `domaincatalog_schema_verify` containers, network, and named volume were removed after evidence capture. They contained only the clean-room schema and rollback-only test activity; they are not recoverable and held no user data.
