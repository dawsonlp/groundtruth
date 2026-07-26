# Transform: Product Conception to Data-Modeling Definition

## Status

- Transform status: draft
- Initial execution: complete
- Validation status: incomplete
- Source layer: `product-conception`
- Source revision: `a62edf4`
- Target layer: `data-modeling-definition`
- Target status: draft and not effective

This transform refines the first application named by the product conception. It does not alter the conception layer and does not imply that the target definition is generated logically from it. The target definition must preserve the conception and conform to the selected governing model.

## Purpose

Produce a reviewable definition of a data-modeling language that:

- distinguishes conceptual, logical, relational-logical, and physical data models;
- spans business entity types through heterogeneous physical designs, deployment artifacts, observed resources, and maintenance comparisons;
- covers relational databases and their complete target-specific metadata surfaces, non-relational stores, APIs, JSON and XML schemas, and metadata-bearing stored assets;
- records explicit realization between model elements and deployment artifacts at different refinements;
- can be realized losslessly as a deployed relational catalog without making that repository schema part of this layer;
- is expressible as a CMOF 2.5.1 model; and
- uses DAMA and industry standards only for the concerns they actually govern.

The transform is also the evidence-producing judgment round required by Domain Catalog ADR 0001. It tests whether using CMOF directly is sufficient before that follow-up decision is accepted.

## Inputs

### Authoritative project inputs

- `layers/product-conception/artifacts/product-investigation.md` at source revision `a62edf4`
- `adr/0001-require-mof-conformance-for-the-governing-model-definition.md` at source revision `a62edf4`

### Human decisions supplied to this transform

- Use the user's 2010 DAMA-DMBOK edition as the current verification baseline.
- Prefer applicable industry standards over project-specific invention.
- Presume CMOF 2.5.1 as the governing model while testing its fit.
- Make the target artifact authoritative for its OMG and ISO standards profile; keep standards research with the transform as evidence.
- Use OCL wherever the required semantics can be expressed over modeled state; make every exception explicit.
- Cover conceptual, logical, and physical data abstraction, from business entity types to tables, columns, foreign-key constraints, and indexes.
- Treat physical design as technology-specific rather than relational-only. Cover traditional and non-traditional RDBMSs, document, key-value, wide-column and graph stores, APIs, JSON and XML schemas, and metadata-bearing file, object, blob, or block-backed assets.
- Represent every physical fact available from a named target and version, using portable typed constructs where honest and explicit target metadata profiles for native kinds, properties, and relationships.
- Support stepwise refinement through detailed design, deployment, observation, drift comparison, and maintenance revisions.
- Require the language and its instances to have a lossless relational repository realization, while keeping the repository implementation distinct from subject systems represented in the catalog.

### External evidence

- OMG Meta Object Facility 2.5.1, including CMOF and its production constraints
- User-owned 2010 DAMA-DMBOK edition; exact pages still required
- ISO and OMG sources listed in `standards-assessment.md`

## Upstream Meaning to Preserve

The output must preserve these distinctions from `product-conception`:

1. CMOF governs the valid form of the data-modeling definition; it does not supply data-modeling semantics.
2. The data-modeling definition governs particular data models by conformance.
3. Conceptual, logical, and physical models are separate purposeful models, not labels applied interchangeably to individual elements.
4. Conformance is not generation, transformation, or realization.
5. Realization relationships must permit judgment, many-to-many correspondence, introduced detail, omission, and information loss.
6. Data-modeling vocabulary must not be promoted into the use-case-neutral conception.
7. Later product behavior and software architecture remain out of scope.
8. Authority, provenance, and external observation remain distinct; observed deployed state must not silently replace intended design.

## Additional Decisions Made by This Transform

- Separate a technology-neutral logical package from a relational-logical package. A relation is not treated as a table.
- Represent entity relationships and cross-model mappings as classes with explicit ends. This supports n-ary relationships and relationship-owned semantics despite CMOF associations being binary.
- Reuse ISO/IEC 11179-31 concepts for the semantic connection between object classes, properties, data-element concepts, conceptual domains, value domains, and data elements.
- Use ISO/IEC 19507:2012 OCL 2.3.1 for definition rules, derived values, model queries, guards, and expressible business/logical constraints. Distinguish definition-model evaluation from subject-data evaluation.
- Retain target SQL for physical view, default, and check expressions; retain a separate transformation language boundary because OCL is side-effect free.
- Use ISO/IEC 19509:2014 XMI as the machine-readable validation representation. Require a relational runtime repository realization without yet selecting its product, schema, or migration mechanism.
- Treat ISO/IEC 19508:2014 as an MOF alignment obligation rather than as equivalent to the later governing OMG MOF 2.5.1.
- Require explicit alignment boundaries for IDEF1X, ISO/IEC 11404, ISO SQL, ISO/IEC 11179-35, ISO/IEC 19763-12, and UML rather than treating shared terminology as conformance.
- Treat physical indexes as target-specific access structures, distinct from logical identifiers and physical uniqueness constraints.
- Require every physical element either to realize an upstream element or to record that it was introduced at the physical level with a rationale.
- Make the physical package technology-neutral at its root and organize relational, document/NoSQL, schema-document, API, and stored-asset concerns as profiles.
- Measure physical metadata completeness against an explicit target/version inventory. Use profile-defined native element, property, and relationship representations instead of either discarding target metadata or inflating it into universal concepts.
- Separate intended physical design, immutable deployment packages, deployment execution records, observed physical inventories, and maintenance comparisons.
- Generalize realization from model-to-model correspondence to refinement-artifact correspondence so deployment material participates without being mislabeled as a data model.
- Require artifact revision lineage and acyclic refinement rather than a fixed universal conceptual-to-logical-to-relational-to-physical sequence.
- Require a future relational repository realization to reconstruct the CMOF definition and representative instances without semantic loss; retain XMI as validation/interchange rather than runtime persistence.

These are provisional definition decisions, not accepted product decisions, until the validation conditions pass.

## Procedure

1. Classify candidate standards by the concern they actually standardize and incorporate the resulting standards profile into the target artifact.
2. Establish unambiguous definitions for each data-model abstraction.
3. Define a minimal shared semantic core.
4. Define conceptual, logical, relational-logical, heterogeneous physical, deployment, observation, and realization packages using only CMOF classes, properties, datatypes, enumerations, generalizations, packages, and constraints.
5. State cross-package well-formedness rules independently of any future software validator.
6. Exercise the language with one subject model across all abstractions.
7. Classify each required capability against CMOF and assess unused CMOF surface and the practical UML relationship.
8. Test physical extensibility against at least one relational catalog, one JSON or XML schema, one API description, one non-relational store, and one metadata-bearing stored-asset example.
9. Test deployment, readback, drift comparison, and maintenance revision without conflating intended and observed state.
10. Test a relational repository mapping for lossless round-trip of the language definition and representative instances.
11. Record unresolved evidence rather than converting uncertainty into a conformance claim.

## Expected Outputs

- `layers/data-modeling-definition/artifacts/data-modeling-language.md`
- `layers/product-conception/transforms/data-modeling-definition/standards-assessment.md`
- `layers/product-conception/transforms/data-modeling-definition/cmof-fit-assessment.md`
- `layers/product-conception/transforms/data-modeling-definition/worked-example.md`

The first file is the target product artifact and is authoritative for its standards profile. The other files are evidence governing this execution of the transform and remain with the transform.

## Validation Conditions

The target can become effective only when all conditions below pass.

- [x] The target is a sibling layer and this transform is colocated with its source.
- [x] Conceptual, logical, relational-logical, and physical meanings are distinct.
- [x] The vocabulary covers business entity type, relationship, constraint, relation, table, view, column, foreign-key constraint, and index.
- [x] Every definition construct has a stated CMOF representation.
- [x] A worked example exercises all abstractions and cross-model realization.
- [x] No ISO registration standard is misrepresented as a complete data-modeling language.
- [x] The target artifact identifies each adopted, governing, aligned, or informative standard and its authority boundary.
- [x] Standards research remains transform evidence rather than a competing product definition.
- [x] OCL is the default for constraints, derivations, queries, guards, and pre/postconditions over modeled state; non-OCL cases have explicit boundaries.
- [x] Physical design is no longer defined as relational-only, and target-native metadata has an explicit representation boundary.
- [x] Intended design, deployment material, deployment records, observations, comparisons, and revision lineage are semantically distinct.
- [x] The required relational repository realization is distinguished from the subject systems represented by the catalog.
- [ ] Exact definitions and model-level distinctions are verified against cited pages in the user's 2010 DAMA-DMBOK edition.
- [ ] Adopted semantics from ISO/IEC/IEEE 31320-2, ISO/IEC 11179-31, ISO/IEC 11404, and ISO/IEC 9075-2 are checked against their normative texts, not only their public abstracts.
- [ ] The `DM-*` rules and derived properties are encoded in ISO/IEC 19507:2012 OCL 2.3.1 and shown equivalent to the normative prose.
- [ ] Separate OCL evaluation environments are defined and tested for definition-model validation and subject-data validation.
- [ ] A machine-readable CMOF/ISO 19509 XMI form of the definition is produced and passes the normative CMOF 2.5.1 production constraints.
- [ ] The version delta between OMG MOF 2.5.1 and ISO/IEC 19508:2014 is assessed before any ISO MOF conformance claim.
- [ ] Alignment mappings to ISO/IEC 11179-35, ISO/IEC 19763-12, and UML are demonstrated where claimed.
- [ ] ISO/IEC 9075-11 and one selected RDBMS vendor catalog are inventoried, with every accessible kind, property, and relationship mapped to a portable construct or native profile definition.
- [ ] JSON Schema 2020-12, XML Schema 1.1, and OpenAPI 3.2.0 examples round-trip without losing native structure, references, or constraints.
- [ ] Representative document, key-value, wide-column, graph, and stored-asset metadata can be represented without falsely forcing it into relational constructs.
- [ ] A design model, deployment package, observed inventory, drift comparison, and maintenance revision are exercised end to end.
- [ ] A relational repository prototype round-trips the CMOF definition and representative instances without loss of identity, ordering, multiplicity, expressions, profiles, revisions, or realization links.
- [ ] The product owner accepts or revises the language inventory and abstraction boundaries.
- [ ] A follow-up ADR decides whether direct CMOF use is accepted.

Until these conditions pass, this target is useful design evidence but is not an effective product layer and cannot be used as an accepted source for further refinement.

## Retry Guidance

If DAMA verification changes the meaning of a model level or construct, revise this transform's decisions and regenerate the target artifact. If a required construct cannot be represented coherently in CMOF, record the precise counterexample in `cmof-fit-assessment.md` before proposing a project-specific MOF-conforming governing model. Do not patch the target definition in isolation.
