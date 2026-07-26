# Domain Data Dictionary Logical Model

## Status

- Status: draft
- Effective: no
- Selected refinement branch: `product-conception` → `data-modeling-definition` → `domain-data-dictionary-component` → `domain-data-dictionary-conceptual-model` → `domain-data-dictionary-logical-model`
- Source layer: `domain-data-dictionary-conceptual-model`
- Source revision: `f311eac`
- Owning transform: [domain-data-dictionary-logical-model](../domain-data-dictionary-conceptual-model/transforms/domain-data-dictionary-logical-model/transform.md)

## Artifacts

- [Logical design](artifacts/logical-design.md)
- [Logical data model](artifacts/logical-data-model.md)

This layer refines the conceptual Domain Data Dictionary into a technology-neutral repository model. It selects a hybrid catalog kernel: typed authoritative records for `ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord`; a reflective `CatalogObject`/`PropertyOccurrence`/`ValueNode` graph for CMOF and DML model objects; and typed capability projections derived from the exact governing-definition revision. Derived projections are readable interfaces to one authority, not independently writable copies.

The draft PostgreSQL implementation-design refinement is [domain-data-dictionary-postgresql-design](../domain-data-dictionary-postgresql-design/README.md), produced by its source-colocated [transform](transforms/domain-data-dictionary-postgresql-design/transform.md). It specifies the runtime and engineering boundary but deliberately does not create the `CAT-PHY` schema or API contract. PostgreSQL structures and API contracts do not belong in this logical layer.

This layer remains non-effective because its source is non-effective and its transform validation is incomplete. Downstream experimentation may continue from this exact revision, but any affected upstream correction makes the resulting descendants stale and requires regeneration in transform order.
