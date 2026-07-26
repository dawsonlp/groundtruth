# Domain Data Dictionary Build Design

## Document Status

- Status: draft
- Effective: no
- Selected component model: Model C, Catalog Kernel with Capability Modules
- Source component revision: `5a0993d`
- Conceptual model: [`conceptual-data-model.md`](conceptual-data-model.md)
- First physical deployment constraint: PostgreSQL
- API direction: common capability boundary for machine and human-facing clients

This document defines the refinement and authority constraints needed to build the Domain Data Dictionary. It is not a logical schema, physical database design, API contract, or implementation plan.

## 1. Build Objective

Build one deployable Domain Data Dictionary component that lets business analysts and data architects establish domain meaning, refine it into logical and physical data designs, deploy target artifacts, observe actual infrastructure, and trace differences back to the artifact that owns the meaning.

The component must preserve the complete chain as catalog data without storing the operational business data described by subject models.

## 2. Refinement Sequence

```text
Model C component design
        |
        v
CAT-CON  Domain Data Dictionary conceptual model   <- this layer
        |
        v
CAT-LOG  technology-neutral logical repository model
        |
        v
CAT-PHY  PostgreSQL physical repository model
        |
        +--> CAT-DEPLOY / CAT-RUNTIME / CAT-OBS / CAT-COMP
        |
        v
capability API and executable component
        |
        +--> LLMs, AI agents, automations, human-facing interfaces
```

`CAT-FAMILY`, `CAT-CON`, and `CAT-LOG` are provisional role references because the current canonical registry begins at `CAT-PHY`. Their use here records the missing refinement roles rather than asserting that the upstream registry already defines them.

## 3. Authority Model

- `CMOF-GOV` governs the form of `DML-DEF`.
- `DML-DEF`, principally `DML-SEM` and `DML-CON`, governs the conceptual model in this layer.
- The conceptual model owns the business meaning the logical repository model must preserve.
- The logical model will own technology-neutral structures, identifiers, datatypes, and integrity decisions.
- The PostgreSQL physical model will own tables, columns, constraints, indexes, PostgreSQL-native metadata, and deployment material.
- The capability design will own commands, queries, responses, interaction semantics, and client-independent access to component behavior.
- The implementation may realize these authorities but may not redefine them through code, repository structure, or API convenience.

## 4. Model C Build Boundaries

| Logical component | Build responsibility derived from the conceptual model | Must not own independently |
| --- | --- | --- |
| Catalog Record Kernel | One commit and reconstruction authority for cataloged domains, definitions, artifacts, revisions, provenance, and evidence | Private copies of model state in other modules |
| Model Construction | Create and revise domain semantics and purposeful model content under an identified governing definition | New data-modeling vocabulary outside `DML-DEF` |
| Conformance Validation | Evaluate definition and model constraints and return diagnostics without mutation | Automatic repair or silent reinterpretation |
| Realization and Impact | Record explicit correspondence, introduction, omission, rationale, and affected descendants | Ownership of either mapped endpoint |
| Target Capability Gateway | Interpret physical targets and metadata profiles and later package or collect target-native artifacts | Conceptual or logical meaning |
| Deployment and Reconciliation | Retain packages, attempts, observations, coverage, comparisons, and dispositions around external actions | Authority over subject infrastructure or observed state as intent |

These remain logical boundaries inside one deployable component unless later operational evidence justifies separation.

## 5. Capability-Access Constraint

The executable component will expose application capabilities rather than repository-oriented CRUD or client-specific back doors.

The same capability semantics must be available to:

- LLM-driven tools;
- other AI agents;
- scheduled and event-driven automations;
- command-line or integration clients; and
- human-oriented user interfaces.

Equal capability access means that the client classes reach the same commands, queries, validation, traceability, deployment-evidence, and comparison behavior. It does not mean every identity has equal permission. Authentication, authorization, policy, rate limits, and human approval may vary by actor and environment without creating separate implementations of the underlying capability.

No client may treat direct PostgreSQL access as a substitute for the application capability boundary. Administrative and recovery access may exist operationally, but it is not a competing product interface or semantic authority.

API resources, operations, protocols, schemas, error formats, streaming behavior, and tool descriptions are deferred until after the logical and physical data responsibilities are stable.

## 6. PostgreSQL Constraint

PostgreSQL is the required first `CAT-PHY` target. The physical refinement must therefore provide:

- a named PostgreSQL version and extension policy;
- a target metadata profile and complete declared catalog inventory;
- a lossless representation of the accepted logical model and required CMOF/DML content;
- executable deployment and migration artifacts;
- observation of the running repository through PostgreSQL metadata;
- intended-versus-observed comparison; and
- round-trip evidence demonstrating that catalog meaning survives persistence.

This constraint does not authorize PostgreSQL concepts in `CAT-CON` or `CAT-LOG`. Tables, columns, keys, indexes, JSONB, arrays, schemas, sequences, triggers, functions, and catalog-specific facts belong to `CAT-PHY` unless a technology-neutral logical need independently requires an upstream construct.

The PostgreSQL version, extensions, schema design, migration mechanism, hosting, backup, and performance choices remain deferred.

## 7. Conceptual Model Contract

The conceptual model is the authority for:

- which business-significant things the catalog retains;
- what each concept means and excludes;
- the material relationships and cardinalities among those concepts;
- the business rules that survive every implementation; and
- the distinctions among intent, realization, deployment, observation, and maintenance evidence.

It is not the authority for identifiers, data structures, datatypes, normalization, persistence, or interfaces.

## 8. Logical Refinement Contract

The next logical model must:

1. assign a logical entity or explicit omission rationale to every conceptual entity;
2. cover every conceptual property and relationship through explicit realization;
3. introduce identifiers, datatypes, structures, and integrity rules without changing conceptual meaning;
4. preserve many-to-many realization and revision lineage without inferring correspondence from names;
5. resolve categorical structures such as model kinds and realization endpoints without collapsing their semantic distinctions;
6. define technology-neutral representations for provenance, ordered collections, expressions, and target-native metadata values;
7. identify every detail introduced at the logical level and its rationale;
8. remain independent of PostgreSQL declarations and API message shapes; and
9. provide enough structure for a lossless PostgreSQL physical realization.

## 9. API Refinement Contract

After the logical and physical responsibilities are stable, the capability design must:

- derive capabilities from Model C responsibilities and lifecycle consequences, not from PostgreSQL tables;
- distinguish commands that change authority-bearing state from queries and derived diagnostics;
- bind every operation to exact artifact, definition, and profile revisions where applicable;
- make external deployment and collection attempts identifiable and reconcilable;
- offer equivalent semantics across human and machine-oriented representations;
- avoid UI-only or agent-only product behavior unless a concrete requirement justifies it; and
- keep authorization policy separate from capability meaning.

## 10. Provisional Assumptions

Draft descendants may proceed using these explicit assumptions:

- `Model Family` has stable identity and explicit membership as a `CAT-CON` business entity. Its placement remains subject to review and moves into `DML-DEF` only if it proves to be a general modeling concern.
- `CAT-FAMILY`, `CAT-CON`, and `CAT-LOG` identify the repository model family and conceptual and logical roles, although the canonical registry does not yet name them.
- provenance and responsible-agent records are required `CAT-CON` concepts; their exact PROV-DM alignment remains pending.

These assumptions enable exploration but cannot become effective authorities. When the upstream definitions change, this layer and affected descendants must be regenerated.

## 11. Completion Boundary for This Layer

This layer is complete as a draft when the conceptual entity, property, relationship, cardinality, and business-rule inventory is reviewable; every concept has an explicit `DML-CON`/`DML-SEM` representation; and its motivating component responsibility or standard is recorded. Product-owner review remains required before treating the inventory as accepted input to a logical model.
