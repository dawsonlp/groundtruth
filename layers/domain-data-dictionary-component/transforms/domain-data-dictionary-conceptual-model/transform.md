# Transform: Domain Data Dictionary Component to Conceptual Catalog Model

## Status

- Transform status: draft
- Transform execution: complete
- Validation status: incomplete
- Source layer: `domain-data-dictionary-component`
- Source revision: `5a0993d`
- Source status: draft and not effective
- Target layer: `domain-data-dictionary-conceptual-model`
- Target status: draft and not effective

This transform applies the selected Model C component boundary to the business concepts the Domain Data Dictionary must retain. It produces a build-direction document and a conceptual data model. It deliberately stops before logical structures, PostgreSQL design, API contracts, or implementation.

## Purpose

Produce a conceptual design that can drive the next logical refinement while preserving:

- the business analyst's domain-exploration workflow;
- the catalog's authority, revision, realization, deployment, observation, and maintenance semantics;
- one catalog record authority across the Model C capability modules;
- PostgreSQL as a downstream physical constraint rather than a conceptual modeling assumption; and
- one future capability surface shared by LLMs, other AI agents, automations, and human-oriented interfaces.

## Inputs

### Authoritative project inputs

- `layers/domain-data-dictionary-component/artifacts/component-design.md` at source revision `5a0993d`
- `layers/data-modeling-definition/artifacts/data-modeling-language.md` at revision `19133fd`
- `layers/product-conception/artifacts/product-investigation.md`
- Domain Catalog ADR 0001, requiring MOF conformance for the governing model definition
- Project ADR 0001, organizing product refinement as a flat layer graph

### Human decisions supplied to this transform

- Select Model C, Catalog Kernel with Capability Modules.
- Make the Domain Data Dictionary's conceptual data model the driver for its later logical model.
- Refine the logical model into a physical deployment targeting PostgreSQL.
- Defer the physical repository schema and API design until their own refinement layers.
- Design the later API around application capabilities available through the same boundary to LLMs, other AI agents, automations, and human-facing user interfaces.
- Continue draft refinement despite provisional upstream layers, while recording gaps and regenerating affected descendants after upstream correction.

## Provisional Decisions and Registry Gaps

This execution proceeds with three explicit provisional matters rather than blocking:

1. The component requires explicit model-family identity and membership. This execution defines `Model Family` as a Domain Catalog business entity governed by `DML-CON`. Its placement is provisional pending product-owner review; it moves into `DML-DEF` only if later evidence shows the concern is general rather than catalog-specific.
2. The canonical registry starts the catalog-repository chain at `CAT-PHY`. This execution provisionally introduces role references `CAT-FAMILY`, `CAT-CON`, and `CAT-LOG` for the repository's model family and conceptual and logical data models. Those names are not authoritative until the registry is revised.
3. `CAT-DATA` includes provenance in its stated scope and the standards profile requires PROV-DM alignment. This execution defines `Responsible Agent` and `Provenance Record` as catalog business concepts governed by `DML-CON`; exact PROV-DM alignment remains pending rather than requiring generic classes in `DML-DEF`.

Every descendant must preserve these as provisional assumptions until the owning layer resolves them.

## Upstream Meaning to Preserve

1. `DML-DEF` governs particular data models; the component and its repository do not redefine the language.
2. Conceptual, logical, and physical models are separate purposeful artifacts connected by explicit realization.
3. `CAT-DATA` represents definitions, models, mappings, provenance, deployments, and observations, not operational `BDM-DATA`.
4. Intended design, deployment material, execution evidence, observed state, and comparison remain distinct.
5. Accepted revisions and observations remain immutable evidence; change creates new revisions.
6. Model C provides one catalog authority with capability-oriented internal boundaries.
7. Target-native meaning remains governed by an identified physical target and metadata profile.
8. OCL remains the default where rules can be evaluated over modeled state.
9. PostgreSQL constrains the later physical realization but does not narrow `DML-DEF` or the component's ability to describe other subject technologies.
10. A common capability API does not imply common authorization; it means that client type does not receive a separate implementation path or direct datastore authority.

## Decisions Made by This Transform

- Treat the target conceptual model as the Domain Catalog repository's conceptual model, provisionally referenced as `CAT-CON/domain-data-dictionary@1`.
- Define only business-significant entity types, properties, relationships, cardinalities, and constraints; omit identifiers, datatypes, keys, logical record structures, tables, columns, endpoints, and messages.
- Model the repository's own concepts, not the operational business data described by cataloged subject models.
- Retain model kind as governed semantic classification. Do not represent conceptual, logical, and physical level as one freely editable label.
- Include responsible-agent and provenance concepts because authority and traceability require them; define them as catalog business entities under `DML-CON` rather than generic metamodel primitives.
- Keep capability names in the build design rather than turn API operations into conceptual data entities.
- Require the logical transform to cover every conceptual entity, relationship, property, and constraint with explicit realization or omission rationale.

## Procedure

1. Translate the selected Model C responsibilities into the business information the catalog must retain.
2. Separate durable domain concepts from application behavior, interface mechanics, and physical storage choices.
3. Define entity types and untyped business properties using `DML-CON` and `DML-SEM` semantics.
4. Define explicit relationships and cardinalities for model governance, refinement, deployment, observation, and maintenance.
5. Give each concept an explicit `DML-CON`/`DML-SEM` representation and trace it to the component responsibility or standard that requires it; record registry or language gaps separately.
6. Record PostgreSQL and the common capability surface only as downstream design constraints.
7. Define the contract the next logical model must satisfy.

## Expected Outputs

- `layers/domain-data-dictionary-conceptual-model/artifacts/build-design.md`
- `layers/domain-data-dictionary-conceptual-model/artifacts/conceptual-data-model.md`

## Validation Conditions

- [x] The conceptual model has a stated purpose, scope, and exclusions.
- [x] It contains business entity types, business properties, relationships, cardinalities, and business constraints only.
- [x] It contains no logical datatype, identifier, record structure, foreign key, table, column, SQL type, index, endpoint, or message design.
- [x] Every Model C responsibility that owns durable business information is represented.
- [x] Conceptual, logical, physical-design, deployment, observed, and comparison artifacts remain distinct.
- [x] `CAT-DATA` is distinguished from operational `BDM-DATA`.
- [x] PostgreSQL is recorded as a downstream physical constraint without affecting conceptual meaning.
- [x] The future API is constrained to a common capability boundary without designing API operations prematurely.
- [x] Every conceptual construct has an explicit `DML-CON`/`DML-SEM` representation and traces to a component responsibility or selected standard.
- [x] Entity types and business properties have an explicit `DML-SEM` object-class, property-concept, data-element-concept, and conceptual-domain binding convention.
- [x] The next logical refinement has explicit coverage and realization obligations.
- [ ] The product owner confirms that model-family identity and membership belong in `CAT-CON` rather than `DML-DEF`.
- [ ] The canonical registry accepts or replaces provisional `CAT-FAMILY`, `CAT-CON`, and `CAT-LOG` references.
- [ ] Responsible-agent and provenance concepts are mapped to the selected PROV-DM alignment boundary.
- [ ] Conceptual terminology and abstraction are checked against exact pages in the user's 2010 DAMA-DMBOK edition.
- [ ] Business constraints expressible over modeled state are encoded and validated as subject-data OCL.
- [ ] The product owner accepts or revises the conceptual entity and relationship inventory.

## Retry Guidance

Further draft logical and physical refinement may proceed from these exact revisions while provisional decisions and registry gaps remain explicit. When `DML-DEF`, its registry, or the selected provenance alignment changes, regenerate this layer and every affected descendant. A logical or physical convenience must not be promoted backward into conceptual meaning merely because PostgreSQL or an API makes it easy to implement.
