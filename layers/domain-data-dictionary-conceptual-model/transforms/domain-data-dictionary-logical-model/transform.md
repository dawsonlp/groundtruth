# Transform: Domain Data Dictionary Conceptual Model to Logical Repository Model

## Status

- Transform status: draft
- Transform execution: complete
- Validation status: incomplete
- Source layer: `domain-data-dictionary-conceptual-model`
- Source revision: `f311eac`
- Source status: draft and not effective
- Target layer: `domain-data-dictionary-logical-model`
- Target status: draft and not effective

## Purpose

Refine the Domain Data Dictionary conceptual model into a technology-neutral logical repository model that:

- preserves every conceptual entity, property, relationship, cardinality, and constraint;
- stores CMOF, `DML-DEF`, catalog definitions, and conforming model instances without requiring a repository redesign for every new governed type;
- supplies stable logical identity, typed values, ordered multiplicity, containment, references, and recursive structured values;
- remains independent of PostgreSQL structures and API message design; and
- provides the complete semantic input for the later PostgreSQL physical model.

## Inputs

- `layers/domain-data-dictionary-conceptual-model/artifacts/build-design.md` at source revision `f311eac`
- `layers/domain-data-dictionary-conceptual-model/artifacts/conceptual-data-model.md` at source revision `f311eac`
- `layers/domain-data-dictionary-component/artifacts/component-design.md` at revision `5a0993d`
- `layers/data-modeling-definition/artifacts/data-modeling-language.md` at revision `19133fd`

## Human Decisions Preserved

- Use Model C with one Catalog Record Kernel and capability-oriented modules.
- Use the conceptual model to drive the logical model.
- Target PostgreSQL only in the later physical refinement.
- Expose the later component through one capability boundary shared by machine and human-facing clients.
- Continue exploratory refinement while provisional upstream decisions remain explicit.

## Alternatives Considered

1. **Type-specific logical entities only.** Mirror every CMOF and `DML-DEF` class directly. This is easy to read but duplicates the governing definition in repository structure and makes language evolution a repository redesign.
2. **Reflective object/property/value kernel only.** Store governed objects, property occurrences, references, and values generically. This preserves self-description and change locality but is difficult for capability consumers to interpret directly.
3. **Hybrid authority with typed governance records and derived model projections.** Keep catalog-specific family and provenance concepts as typed logical records, retain a reflective kernel for CMOF/DML model objects, and derive typed views of those objects from exact governing-definition revisions. This retains one authority per fact without pretending catalog-only concepts are part of the general metamodel.

This transform selects option 3.

## Provisional Decisions and Registry Gaps

- `CAT-FAMILY`, `CAT-CON`, and `CAT-LOG` remain provisional canonical role references.
- `Model Family` remains a `CAT-CON` business concept unless later evidence requires promotion into `DML-DEF`.
- Responsible-agent and provenance concepts remain subject to exact PROV-DM alignment.
- The machine-readable CMOF and OCL definitions required to prove reflective validation remain pending upstream.

## Upstream Meaning to Preserve

1. A model's governing definition is authority; repository code and projections do not redefine permitted types or properties.
2. Conceptual, logical, physical-design, deployed, observed, and comparison artifacts remain distinct.
3. Model and element identity never transfers implicitly through realization.
4. Ordered collections, multiplicity, expressions, native metadata, and revisions must round-trip without semantic loss.
5. Accepted revisions and observations are immutable evidence.
6. `CAT-DATA` remains distinct from operational `BDM-DATA`.
7. Direct repository access is not a product capability boundary.
8. OCL is the default constraint language over modeled state.

## Decisions Made by This Transform

- Use three typed authoritative governance entities: `ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord`.
- Use three authoritative reflective-content entities: `CatalogObject`, `PropertyOccurrence`, and `ValueNode`.
- Represent every CMOF/DML governed object—including definitions—as a `CatalogObject` typed by another cataloged CMOF class.
- Give the three typed governance entities their own identifiers, required core text and classification fields, optional external evidence fields, and explicit relationships to reflected domains, model revisions, and evidence subjects.
- Represent each governed property occurrence once, either as an object reference or as a recursively structured value.
- Preserve order with occurrence and value-node positions; do not infer order from storage.
- Represent structured datatype values as acyclic `ValueNode` trees governed by cataloged datatype and field definitions.
- Derive typed capability projections for reflected model content from governing definitions and kernel state; projections are read-only and replaceable.
- Join typed governance records and reflected content through explicit `CAT-LOG` relationships rather than duplicated capability-owned state.
- Introduce no PostgreSQL datatype, table, key, index, JSON representation, API resource, endpoint, or message.

## Expected Outputs

- `layers/domain-data-dictionary-logical-model/artifacts/logical-design.md`
- `layers/domain-data-dictionary-logical-model/artifacts/logical-data-model.md`

## Validation Conditions

- [x] Every conceptual entity has an explicit logical realization.
- [x] Every conceptual property and relationship has an explicit authoritative representation, either typed or reflective.
- [x] Logical identifiers, datatypes, optionality, ordering, references, and integrity rules are defined.
- [x] Relationship-owned meaning remains representable through reified governed objects.
- [x] Expressions and recursive structured values have explicit logical representations intended to round-trip without loss.
- [x] Target-native metadata definitions, values, and relationships have explicit reflective representations.
- [x] Typed projections cannot become independent writable authorities.
- [x] The model contains no PostgreSQL or API contract design.
- [ ] Machine-readable realization coverage is produced for every conceptual property and relationship.
- [ ] Kernel constraints are encoded and validated as OCL.
- [ ] Representative `CMOF-GOV`, `DML-DEF`, and `CAT-CON` instances round-trip through the logical kernel.
- [ ] The bootstrap path for loading self-describing `CMOF-GOV` is demonstrated.
- [ ] Provisional catalog role names are accepted or replaced in the canonical registry.
- [ ] DAMA logical-model terminology is verified against the user's 2010 edition.
- [ ] The product owner accepts or revises the hybrid-kernel decision and logical inventory.

## Retry Guidance

Draft PostgreSQL refinement may continue from this exact revision while failures and provisional decisions remain explicit. If a representative model cannot round-trip, first determine whether the loss belongs to the conceptual model, this transform, or the generic value representation. Correct the earliest owning layer and regenerate affected descendants; do not add an untraceable PostgreSQL escape column as a substitute for missing logical meaning.
