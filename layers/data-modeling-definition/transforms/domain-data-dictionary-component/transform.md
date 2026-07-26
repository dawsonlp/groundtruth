# Transform: Data-Modeling Definition to Domain Data Dictionary Component Design

## Status

- Transform status: draft
- Transform execution: complete
- Directory scaffolding: complete
- Validation status: incomplete
- Source layer: `data-modeling-definition`
- Source revision: `19133fd`
- Source status: draft and not effective
- Target layer: `domain-data-dictionary-component`
- Target status: draft design and not effective

This transform refines the data-modeling language definition into the design of the first deployable Domain Catalog component. The initial directory scaffold recorded the intended refinement branch; the completed execution now supplies a draft design but does not make either layer effective.

## Purpose

Produce a reviewable component design for a data dictionary that supports a business analyst or data architect who is exploring a business domain in preparation for building solutions. The component must support the purposeful refinement of a particular business data-model family from conceptual meaning, through logical structure, to one or more deployable physical designs. It must also retain the deployed and observed physical state needed to compare infrastructure with intended design during maintenance.

The design must remain governed by `DML-DEF`. It must not replace that language definition, promote component choices into the governing model, or assume that one physical technology is universal.

## Inputs

### Authoritative project inputs

- `layers/data-modeling-definition/artifacts/data-modeling-language.md` at source revision `19133fd`
- `adr/0001-require-mof-conformance-for-the-governing-model-definition.md` at source revision `19133fd`

The source is still draft. All target design work is therefore provisional and must be revisited if the source definition changes before acceptance.

### Human decisions supplied to this transform

- Establish the first deployable model as a component with its own refinement layer.
- Design it for business analysts and data architects beginning exploration of a particular business domain with the expectation of building solutions there.
- Follow the DAMA-informed progression from conceptual modeling to logical modeling and then to technology-specific physical modeling.
- Treat the component as a data dictionary whose stored content remains aligned across those modeling levels.
- Preserve the relationship between intended physical models, deployed infrastructure, observed physical state, and maintenance activity in the component's data.
- Keep the component aligned with the architectural and modeling constraints already defined by the project.
- Create the component structure now; write the component design as the next step.

## Upstream Meaning to Preserve

The component design must preserve these distinctions and constraints from `DML-DEF`:

1. `CMOF-GOV` governs the form of `DML-DEF`; `DML-DEF` governs particular `BDM-*` models. The component implements support for those models but does not become their governing definition.
2. A `BDM-FAMILY` contains separate, purposeful conceptual, logical, optional relational-logical, and target-specific physical models. Model levels are not interchangeable labels on one mutable artifact.
3. Refinement and realization are explicit, revisioned, and potentially many-to-many. A physical element may realize upstream meaning or record justified detail introduced at the physical level.
4. Relational deployment is one branch, not the universal physical form. The language also permits non-relational stores, APIs, schema documents, and metadata-bearing stored assets.
5. Intended physical design, deployment packages, deployed runtime structures, observed inventories, and intended-versus-observed comparisons remain distinct.
6. `CAT-DATA` stores model definitions, model instances, mappings, lineage, provenance, deployments, and observations. It does not silently acquire responsibility for operational `BDM-DATA`.
7. The repository realization must preserve represented CMOF and data-model content without semantic loss.
8. OCL is the default expression language where the required rule can be evaluated over modeled state; transformation and external-observation behavior remain separate concerns.
9. DAMA terminology is a current verification baseline, while normative conformance claims remain bounded by the standards profile and evidence recorded with the source transform.
10. Observed infrastructure is evidence about deployed state; it must not silently overwrite intended design.

## Decisions Reserved for the Design

The scaffold makes none of the following decisions. They belong in the component design and require explicit justification:

- the component's responsibility boundary and excluded responsibilities;
- user workflows and lifecycle states;
- internal subcomponents and their interfaces;
- the commands, APIs, or events exposed to other components;
- how `BDM-*`, `CAT-*`, realization, revision, deployment, and observation concepts are partitioned in persistence;
- the repository schema and lossless round-trip strategy;
- model validation and OCL execution boundaries;
- import, deployment, metadata readback, comparison, and maintenance behavior;
- database product, programming language, frameworks, migration tooling, or deployment topology; and
- the boundary between a deployable first increment and later capabilities.

## Procedure

1. Reconcile the requested analyst workflow with the canonical model and artifact registry in `DML-DEF`.
2. State one coherent component responsibility and its explicit exclusions.
3. Describe the component's users, external systems, inputs, outputs, and consequence-bearing workflows.
4. Partition behavior into the smallest set of components or modules needed to keep responsibilities clear without duplicating the language model.
5. Specify lifecycle, authority, revision, realization, deployment, observation, and recovery behavior.
6. Define interfaces and persistence responsibilities at the design level without prematurely selecting implementation technologies.
7. Trace every design responsibility to a `DML-*`, `BDM-*`, or `CAT-*` concept and identify any required capability not supported by the source definition.
8. Validate the design against the conditions below before proposing an implementation transform.

## Expected Output

- `layers/domain-data-dictionary-component/artifacts/component-design.md`

The artifact exists as a draft component model. It remains provisional while its source and the transform validation are incomplete.

## Validation Conditions

The target design can become effective only when all conditions below pass.

- [x] The component has one coherent responsibility and explicit exclusions.
- [x] The analyst workflow preserves conceptual, logical, and physical models as distinct revisioned artifacts.
- [x] Cross-model realization and traceability are explicit rather than inferred from names or containment.
- [x] Intended design, deployment material, runtime state, observation, comparison, and maintenance are distinct.
- [x] The design supports relational and non-relational physical branches without weakening the first deployable increment.
- [x] The data dictionary stores `CAT-DATA` and does not conflate it with operational `BDM-DATA`.
- [x] Persistence is constrained to reconstruct represented definitions and models without semantic loss; implementation proof remains downstream.
- [x] Validation, transformation, deployment, and external observation have explicit authority boundaries.
- [ ] DAMA-informed terminology agrees with the verified source definitions and does not overstate unverified conformance.
- [x] The design introduces no infrastructure or technology choice without a requirement that makes it necessary.
- [x] Every design responsibility traces to the source definition or records a concrete upstream gap.
- [ ] The product owner accepts the component boundary and first deployable scope.

The design execution exposed one concrete upstream gap: `DML-DEF` names `BDM-FAMILY` as the grouping object for related subject models but revision `19133fd` has no family class or explicit membership relationship. The target design records the required responsibility but does not infer or invent the missing construct. The source definition must resolve the gap before this target can be accepted.

Because the source layer is not effective, passing these conditions would still leave the target provisional until its accepted source revision and transform are identified.

## Retry Guidance

If design work exposes an unsupported modeling concept or a contradiction in `DML-DEF`, change the source definition and its owning transform first, then restart this transform from the corrected source revision. If the problem is limited to component boundaries or implementation responsibilities, revise this transform and regenerate only the component-design layer. Do not repair an implementation symptom by weakening the governing model silently.
