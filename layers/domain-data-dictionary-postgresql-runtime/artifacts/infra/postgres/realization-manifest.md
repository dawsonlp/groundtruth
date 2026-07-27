# PostgreSQL Realization Manifest

## Status and Authority

- Status: implementation manifest
- Effective: no
- Semantic source: `CAT-LOG/domain-data-dictionary@1` at revision `5728636`
- Owning design revision: `f10afc7`
- Executable physical authority: `infra/flyway/migrations/V202607260001__create_catalog_kernel.sql`
- Target: PostgreSQL 18.4
- Extension policy: PostgreSQL core only; no optional extension is required or activated

This manifest is derived traceability evidence. It does not define catalog meaning and is not independently writable authority. If it disagrees with `CAT-LOG`, correct the owning layer or transform and regenerate this manifest and the SQL together.

## Physical Organization

All product objects are contained in schema `catalog`. Flyway retains its operational history in `public.flyway_schema_history`. The migration creates no operational business data (`BDM-DATA`) and no seed model content.

`catalog.catalog_record` is a physical identity registry used to enforce one global `CatalogIdentifier` namespace across the four independently identified logical record kinds. It is not a seventh logical authority. A deferred constraint trigger requires every committed registry row to have exactly the subtype named by its `record_kind`.

## Logical Authority Mapping

| Logical authority | Authoritative PostgreSQL object | Supporting objects | Notes |
| --- | --- | --- | --- |
| `ModelFamily` | `catalog.model_family` | `catalog.model_family_model_revision` | The relationship table preserves family membership and prevents a model revision from belonging to more than one family. Definition-aware validation must prove that domain, status, and members have the required governed types. |
| `ResponsibleAgent` | `catalog.responsible_agent` | none | Agent kind is an exact `CatalogObject` reference. External identity remains evidence, not authorization. |
| `ProvenanceRecord` | `catalog.provenance_record` | `catalog.provenance_source_reference`, `catalog.provenance_responsible_agent`, `catalog.provenance_subject` | A technical construction flag must be sealed before commit. Deferred checks require at least one agent and subject. Once sealed, the record and its dependent rows are immutable. |
| `CatalogObject` | `catalog.catalog_object` | `catalog.catalog_record` | Each object references one governing type and one exact governing-definition revision. Both references are deferred to permit transactional loading of self-describing definition closures. |
| `PropertyOccurrence` | `catalog.property_occurrence` | deferred payload-integrity trigger | The composite primary key is `(subject_identifier, property_definition_identifier, position)`. `payload_kind` makes the physical representation explicit; a deferred check requires exactly one reference target or root value. |
| `ValueNode` | `catalog.value_node` | `catalog.value_node_with_path` view and deferred tree-integrity trigger | `value_node_identifier` is a physical surrogate only. The logical `(occurrence, path)` identity is reconstructed by the recursive view from parentage, role, field definition, and position. |

## Datatype Mapping

| Logical datatype | PostgreSQL realization |
| --- | --- |
| `CatalogIdentifier` | `catalog.catalog_identifier` domain over trimmed, non-empty `text` |
| `Text`, `LexicalValue`, `ContentReference`, `ExternalReference` | `text`, with non-empty checks where the logical value is identity-like evidence |
| `Ordinal` | non-negative `bigint` |
| `Instant` | `timestamp with time zone` |
| `ContentDigest` | paired algorithm/value columns with all-or-none checks |
| `ExternalReferenceSet` | normalized rows in `catalog.provenance_source_reference`, unique per provenance record |
| `ValueRole` | `catalog.value_role` enum using the exact logical literals |
| `ValuePath` | derived `text` in `catalog.value_node_with_path`; field identifiers are hex-encoded in path segments to avoid delimiter ambiguity |

## Integrity Rule Coverage

Enforcement classifications:

- **Database**: rejected by PostgreSQL constraints, indexes, or deferred constraint triggers.
- **Database partial**: structural portion is enforced; definition-dependent meaning requires validation after governing definitions are loaded.
- **Definition validator**: requires machine-readable CMOF/DML/OCL interpretation and cannot honestly be hard-coded into this generic kernel.
- **Capability transaction**: must be enforced by the later command boundary in addition to database structure.

| Rule | Enforcement | PostgreSQL mechanism or remaining obligation |
| --- | --- | --- |
| `CATLOG-001` | Database | `catalog.catalog_record` primary key plus exact-kind subtype foreign keys provide one namespace for `CatalogObject`, `ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord`. |
| `CATLOG-002` | Database partial | `catalog_object.governing_type_identifier` and `governing_definition_revision_identifier` are mandatory exact references. The definition validator must prove that the type is a CMOF class in that revision's closure. |
| `CATLOG-003` | Definition validator | Property-definition applicability and inheritance require the loaded governing definition. |
| `CATLOG-004` | Database | `property_occurrence` composite primary key and non-negative position check. |
| `CATLOG-005` | Database | Payload-kind row check plus deferred `assert_property_occurrence_payload` trigger requiring exactly one reference or one root node. |
| `CATLOG-006` | Database partial | Positions, reference integrity, and sibling uniqueness are enforced. Multiplicity, semantic uniqueness, composition, and target/value conformance require definition validation. |
| `CATLOG-007` | Database | Same-occurrence parent foreign key, root/parent checks, sibling uniqueness, and deferred cycle detection. |
| `CATLOG-008` | Database | Tree structure and sibling uniqueness make the recursively derived occurrence path unique and order-preserving. |
| `CATLOG-009` | Database partial | Carrier exclusivity, digest pairing, root/field roles, and parent/child payload exclusion are enforced. Datatype-specific shape requires definition validation. |
| `CATLOG-010` | Definition validator | Generic tree cycles are blocked. CMOF composite-reference ownership and cycles require interpretation of property definitions. |
| `CATLOG-011` | Database partial | Internal references cannot dangle. Whether an accepted closure may use an external reference requires artifact-state and definition validation. |
| `CATLOG-012` | Database partial | Sealed provenance is immutable. Accepted model revisions and observations require status-aware capability and definition validation. |
| `CATLOG-013` | Definition validator | Supersession and realization edges are reflective properties; their kinds and acyclicity require the loaded definition. |
| `CATLOG-014` | Database partial | Provenance records require responsible agents and subjects before commit. Which modeled activities require provenance is a capability/definition rule. |
| `CATLOG-015` | Definition validator | Intended and observed model roles are governed types and must be checked from the loaded definition. |
| `CATLOG-016` | Definition validator | Deployment result semantics are governed model content, not database migration status. |
| `CATLOG-017` | Definition validator | Lexical values are retained losslessly; active target/profile membership requires loaded target metadata definitions. |
| `CATLOG-018` | Database and capability transaction | The migration creates no writable typed projection tables. `catalog.value_node_with_path` is a replaceable read-only view; future capability projections must remain read-only. |
| `CATLOG-019` | Verification | Representative import/export and round-trip tests must prove reconstruction from the six authorities and derived value paths. |
| `CATLOG-020` | Boundary and review | The migration creates catalog metadata structures only and no subject-system operational data tables. |
| `CATLOG-021` | Database partial | Family domain is mandatory; membership uniqueness gives each recorded model at most one family. Governed-type checks and the requirement that every concrete data model has a family require definition validation. |
| `CATLOG-022` | Database partial | Every agent has one agent-kind object and an optional external evidence reference. Permitted kind values require definition validation. |
| `CATLOG-023` | Database | Sealing, minimum agent/subject cardinality, recorded time, activity kind, and immutable dependent rows are enforced before commit and thereafter. |
| `CATLOG-024` | Database partial | Global identifier kinds prevent one identified record from being both typed governance and reflected content. Semantic duplicate facts and source identity in future combined read models require definition/capability validation. |

## Index and Access Rationale

- Primary and unique constraints implement logical identity before query optimization.
- Every non-primary foreign-key access path has an explicit B-tree index so integrity checks and graph traversal do not require avoidable full scans.
- `catalog.value_node_with_path` derives paths recursively; paths are not stored and therefore cannot drift from parentage or order.
- No materialized typed projection is created. This avoids a second writable authority before workload evidence justifies caching.
- No partitioning is introduced. There is no volume or retention evidence that justifies it yet.

## Construction Protocols

Self-describing definition closures may contain circular references. Insert their `catalog_record` and `catalog_object` rows in one transaction; the relevant foreign keys and subtype checks are initially deferred.

Create a provenance record in one transaction as follows:

1. insert its `catalog_record` and unsealed `provenance_record` rows;
2. insert unique source references, responsible-agent links, and subject links;
3. set `sealed = true`; and
4. commit.

The deferred completeness trigger rejects an unsealed or incomplete provenance record. After sealing, triggers reject changes to the record or its dependent rows.

## Known Upstream-Dependent Validation Gaps

This realization intentionally does not encode CMOF class/property semantics as PostgreSQL constants. The following require the pending machine-readable `CMOF-GOV` and `DML-DEF` load plus OCL/definition evaluation:

- governing-class membership and inherited property applicability;
- property multiplicity, semantic uniqueness, composition, and target datatype/class conformance;
- datatype-specific recursive value shapes;
- accepted-artifact closure and immutability beyond provenance;
- realization and supersession acyclicity;
- governed status, model-role, target-profile, and provenance-requirement semantics; and
- generated typed capability projections.

These are explicit incomplete validations, not permission for the database representation to weaken them.
