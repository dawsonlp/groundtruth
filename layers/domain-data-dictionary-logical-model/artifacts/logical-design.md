# Domain Data Dictionary Logical Design

## Document Status

- Status: product-owner accepted for continued exploratory refinement
- Effective: no
- Provisional canonical reference: `CAT-LOG/domain-data-dictionary@1`
- Source conceptual model: `CAT-CON/domain-data-dictionary@1` at revision `73ed9df`
- First repository realization: PostgreSQL

## Inputs Consulted

- `CAT-CON/domain-data-dictionary@1` conceptual data model and build design at revision `73ed9df`
- Model C component design at revision `5a0993d`
- `DML-DEF` at revision `19133fd`, principally `DML-LOG`, `DML-SEM`, and `DML-REA`
- source-colocated conceptual-to-logical transform at this source revision

No input layer is effective. This document remains an exploratory refinement, not an effective product layer. The selected component boundary, PostgreSQL target, and hybrid-kernel authority model are product-owner decisions. Acceptance of the hybrid approach authorizes continued draft refinement; it does not close the upstream definition, conformance, performance, or round-trip gaps.

## 1. Decision

Use a **hybrid catalog kernel with typed governance records, reflective model content, and typed derived projections**.

The authoritative logical state has two non-overlapping forms:

- typed records for the catalog-specific `ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord` concepts that are not part of general `DML-DEF`; and
- governed objects, property occurrences, object references, and recursively structured values for CMOF/DML definitions and model instances.

CMOF and `DML-DEF` definitions are stored through the same reflective mechanism as the models they govern. Capability modules derive typed views of that reflective content by interpreting the exact governing-definition revision associated with an object. The three catalog-specific record types are already typed authority and are not reconstructed as projections.

This is a logical model decision, not a PostgreSQL EAV schema decision. The PostgreSQL realization may use several tables, typed partitions, materialized projections, JSON, or other PostgreSQL mechanisms, provided it reconstructs both parts of the logical kernel exactly and retains one authority for each fact.

## 2. Why This Model

### Type-specific entities only

Advantages:

- familiar entity-by-entity structure;
- direct static constraints for the current language; and
- straightforward typed queries.

Rejected as the authority because every change to CMOF, `DML-DEF`, or a target metadata profile could require a repository-model change. The database structure would become a second manually maintained copy of the governing definition.

### Reflective kernel for all catalog state

Advantages:

- smallest authoritative model;
- direct support for self-description and new governed types; and
- uniform identity, multiplicity, ordering, and references.

Rejected because catalog-only governance records would need either nonexistent CMOF classes or a second governance plane inside the generic kernel. Both would hide a product-specific type system inside the persistence mechanism. Callers also should not need to reconstruct metamodel semantics for routine work.

### Hybrid kernel plus typed projections

Selected because:

- governing definitions remain the semantic authority;
- catalog-specific governance does not leak into the general data-modeling definition;
- every fact has exactly one writable representation;
- projections give capabilities typed, comprehensible records;
- a projection can be regenerated when its definition changes; and
- PostgreSQL optimization remains a physical concern.

## 3. Authority Boundary

- `ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord` are authoritative typed logical entities owned by the Catalog Record Kernel.
- `CatalogObject`, `PropertyOccurrence`, and `ValueNode` are the authoritative logical entities for reflected CMOF/DML objects and their values.
- A typed projection is derived from those entities plus an exact governing-definition revision.
- A projection may be cached or materialized physically but is never independently writable.
- Typed governance records and reflected model objects may reference one another only through relationships defined in `CAT-LOG`; no capability module owns a private joining copy.
- Commands express changes in governed object terms and commit through the Catalog Record Kernel.
- Queries may return typed capability records without exposing the kernel's physical representation.
- Imports and exports operate on complete governed object closures, not disconnected rows.

## 4. Self-Description

Every `CatalogObject` identifies a cataloged CMOF/DML object and the cataloged CMOF class that defines its type. CMOF packages, classes, datatypes, enumerations, properties, constraints, and expressions are themselves catalog objects. `DML-DEF`, `CAT-CON`, `CAT-LOG`, and particular model artifacts therefore use the same reflective representation.

`ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord` are application records described by `CAT-LOG`, not new CMOF classes in `DML-DEF`. Keeping them typed and separate preserves that upstream boundary. Their relationships to reflected domains, models, and evidence are explicit catalog relationships.

The root bootstrap loads an identified `CMOF-GOV` revision whose objects are typed according to CMOF's self-conformance. The kernel does not use an unrecorded application type name as a substitute for that relationship. Exact bootstrap loading and verification remain to be demonstrated before effectiveness.

## 5. Logical Value Strategy

A property occurrence has exactly one payload kind:

- an object reference; or
- a root `ValueNode` representing a datatype value.

Primitive values use one atomic node with their cataloged datatype definition and target-independent lexical meaning. Record, collection, map, choice, and opaque datatype values use an acyclic node tree. Field definitions, roles, and explicit positions preserve structure and order.

This strategy avoids choosing PostgreSQL columns or JSON while still defining what a lossless physical representation must retain.

## 6. Typed Capability Projections

The following read models are required, but their transport representations are deferred. A read model may combine typed governance records with projections of reflected model content without creating another authority:

| Projection family | Principal conceptual content |
| --- | --- |
| Domain Semantics | Data domains and semantic definitions |
| Model Governance | Governing definitions, model families, model revisions, model elements, expressions, lineage, and status |
| Realization and Impact | Realization sets, mappings, coverage, and affected descendants |
| Target Context | Physical targets, profiles, native definitions, native facts, and environments |
| Deployment Evidence | Packages, artifacts, attempts, and results |
| Observation and Maintenance | Captures, coverage assessments, comparisons, differences, and dispositions |
| Provenance | Responsible agents, activities, sources, evidence, and subjects |

Each reflected-content projection names the governing type and property definitions used to derive it. Missing required definitions are validation errors, not silently nullable output. Fields sourced from typed governance records retain their logical entity and attribute identities instead.

Projection structure is generated from applicable CMOF properties rather than maintained as a second handwritten type system. Multiplicity determines scalar or collection shape; references retain catalog identity; datatype fields reconstruct their governed value; and derived properties remain computed. Every returned field remains traceable to its property definition and governing-definition revision.

## 7. Command and Query Consequences

- A command targets catalog identities and exact artifact revisions, not physical rows.
- Acceptance validates the complete governed closure and commits the new status plus required realization and provenance atomically.
- A query may request generic objects or a typed projection.
- LLMs, agents, automations, and human-facing interfaces use the same command/query semantics.
- Authorization filters capabilities and scopes; it does not create a second data model.
- Direct PostgreSQL mutation bypasses validation and is outside the product interface.

## 8. PostgreSQL Realization Constraints

The PostgreSQL realization must demonstrate:

- unique and stable catalog identity;
- type and property-definition referential integrity;
- typed integrity for model-family, agent, and provenance records and their references to reflected content;
- payload exclusivity;
- ordered multiplicity;
- acyclic containment and value trees;
- atomic accepted-artifact publication;
- immutable accepted revisions and observations;
- lossless recursive values and target-native lexical facts;
- replaceable typed projections; and
- round-trip reconstruction of representative governing and subject models.

It may not make a projection table, JSON document, generated API model, or vendor catalog import an independent source of truth.

## 9. Deferred Decisions

- PostgreSQL version, extensions, schemas, tables, columns, indexes, constraints, and partitioning
- Whether projections are computed, cached, or materialized
- Query language, API protocol, resource shapes, and tool descriptions
- OCL engine and transformation engine
- Concurrency-control and migration mechanisms
- Content storage for large opaque or native artifacts
- Bootstrap tooling and distribution format

## 10. Accepted Product-Owner Decision

On 2026-07-28, the product owner accepted the hybrid catalog kernel as the approach to continue exploring. The decision preserves:

- reflective authority for CMOF/DML-governed objects and properties;
- typed authority for catalog-specific governance records;
- derived typed projections as the readable boundary for capabilities and clients; and
- the type-specific base/extension-table realization as a fallback alternative if measured performance, operability, or comprehensibility makes the reflective realization unsuitable.

The acceptance is conditional on consequence-bearing tests rather than confidence in flexibility alone. The next refinements must demonstrate that:

- capability implementers can work against typed semantic contracts without reconstructing kernel rows;
- human-facing interfaces remain thin consumers of the same capability semantics used by machine clients;
- representative projection and traversal workloads remain understandable and performant as object and occurrence counts grow; and
- the catalog can model its own conceptual and ontological structure, refine that model through design, observe this PostgreSQL realization, and compare intended with observed state without bypassing the capability boundary.

The product owner described the first modeling stage as "conceptual with anthological." This document provisionally interprets that phrase as conceptual and ontological modeling; the terminology remains subject to correction without changing the accepted hybrid authority decision.

## 11. Recommended Next Step

Execute the source-colocated capability-API architecture transform. Define a semantic capability boundary over typed projections, commands, validation, observation, and comparison without exposing the reflective kernel or assigning business logic to user interfaces. Use self-modeling and observation of the local PostgreSQL runtime as the first end-to-end test. Route semantic failures to the earliest owning layer; route ordinary projection and query-performance work to downstream technical design or the PostgreSQL realization transform.

## 12. Review and Sign-Off

### Architect Review

Pending.

### Senior Implementation Engineer Review

Pending.

### Product Owner Review

- Status: accepted for continued exploratory refinement
- Decision: continue the hybrid typed/reflective kernel with derived projections
- Conditions: prove semantic API readability, thin-client fidelity, self-modeling, PostgreSQL reflection, and performance at increasing catalog scale
- Alternative retained: type-specific base/extension tables as a fallback physical realization
- Date: 2026-07-28

### Author

- Signer: Codex
- Signer type: agent
- Role: logical design author
- Disposition: submitted for review
- Date: 2026-07-26

### Workflow Status

- Current status: product-owner accepted for continued exploratory refinement; draft and non-effective
