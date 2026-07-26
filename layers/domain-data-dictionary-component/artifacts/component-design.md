# Domain Data Dictionary Component Design

## Document Status

- Status: draft
- Transform execution: complete
- Validation status: incomplete
- Effective: no
- Source definition: `DML-DEF` at revision `19133fd`
- Owning transform: [`transform.md`](../../data-modeling-definition/transforms/domain-data-dictionary-component/transform.md)
- DAMA verification baseline: user's 2010 DAMA-DMBOK edition
- DAMA page verification: inherited as pending from `DML-DEF`
- Product owner component-model decision: Model C accepted 2026-07-26
- First physical deployment constraint: PostgreSQL; version and physical design deferred
- Interface direction: one capability-oriented application surface for human and machine clients; API design deferred

This artifact is a component model, not a technical design. It defines responsibility, authority, data ownership, collaboration, and change boundaries for the first deployable Domain Catalog capability. It records PostgreSQL as the required first physical deployment target and a common capability surface as the interface direction, but does not select the PostgreSQL version, repository schema, programming language, framework, user interface, API protocol, or deployment topology.

## 1. Purpose

The Domain Data Dictionary Component enables a business analyst and data architect to establish a shared understanding of a business domain and carry that understanding into implementable data structures without losing the relationships between abstraction levels.

It manages a particular business data-model family (`BDM-FAMILY`) as related model revisions and lifecycle records:

1. conceptual meaning (`BDM-CON`);
2. technology-neutral logical structure (`BDM-LOG`);
3. optional relational-logical structure (`BDM-REL`);
4. one or more target-specific physical designs (`BDM-PHY`);
5. deployment packages and execution evidence (`BDM-DEPLOY`);
6. observed physical state (`BDM-OBS`); and
7. intended-versus-observed comparison and maintenance disposition (`BDM-COMP`).

The component is a data dictionary because it retains the definitions, structures, constraints, correspondences, provenance, and lifecycle evidence for these artifacts as `CAT-DATA`. It is not merely a glossary and is not the operational store for the business data (`BDM-DATA`) described by those models.

## 2. Scope and Boundary

### 2.1 Responsibilities inside the component

The component is responsible for:

- establishing a domain and a `BDM-FAMILY` within it;
- managing stable identity, revision lineage, status, provenance, and governing-definition references for cataloged artifacts;
- constructing and querying conceptual, logical, optional relational-logical, physical-design, and observed models using the vocabulary permitted by `DML-DEF`;
- validating definitions and model instances against the applicable CMOF and `DML-DEF` rules;
- recording explicit, many-to-many realization among model elements and deployment artifacts;
- identifying introduced, omitted, or transformed detail and its rationale;
- determining downstream impact from an upstream revision without silently changing descendants;
- managing target and metadata-profile references required to interpret physical models;
- producing immutable deployment packages from a physical-design revision through a selected target capability;
- requesting deployment through an external executor and recording execution evidence without equating success with conformance;
- accepting externally collected metadata as a new observed physical model with collection and coverage evidence;
- comparing intended and observed physical state and recording difference dispositions; and
- importing, exporting, and reconstructing governed definitions and model families without semantic loss.

### 2.2 Responsibilities outside the component

The component does not own:

- the definition or revision of `CMOF-GOV` or `DML-DEF`; it consumes identified revisions of them;
- operational `BDM-DATA`, business transactions, or business-system behavior;
- the database, API, storage service, or other subject infrastructure represented by `BDM-RUNTIME`;
- native execution of DDL, migrations, schemas, API publications, or infrastructure changes;
- native collection of target metadata from every supported platform;
- acceptance of an observed structure as intended design without a model revision at the level that owns the meaning;
- requirements management, solution architecture, application code generation, or general enterprise governance;
- organization-wide access control, approval workflow, or collaboration semantics; or
- an assertion that every target can be represented by relational concepts.

Deployment executors and metadata collectors are external collaborators. The component supplies and records governed artifacts around those actions; it does not make external side effects part of the catalog's atomic state change.

### 2.3 Users and external collaborators

| Party | Relationship to the component |
| --- | --- |
| Business analyst | Establishes domain vocabulary, conceptual entities, properties, relationships, cardinality, and business constraints; reviews downstream traceability |
| Data architect | Refines conceptual meaning into logical and physical designs, records realization decisions, validates models, and assesses change impact |
| Deployment operator or automation | Receives an immutable deployment package, acts on subject infrastructure, and returns execution evidence |
| Metadata collector | Reads an identified target environment and supplies an observed model plus collection and coverage evidence |
| Model consumer | Queries or exports definitions, models, lineage, and comparison results without becoming an independent authority |
| Governing-definition provider | Supplies identified `CMOF-GOV` and `DML-DEF` revisions and their constraints |
| Target-profile provider | Supplies target/version vocabulary, metadata coverage inventory, datatype mappings, and packaging behavior |

## 3. Inputs Consulted

- `layers/product-conception/artifacts/product-investigation.md`
- `layers/data-modeling-definition/artifacts/data-modeling-language.md` at revision `19133fd`
- `layers/product-conception/transforms/data-modeling-definition/worked-example.md`
- `layers/product-conception/transforms/data-modeling-definition/cmof-fit-assessment.md`
- `layers/data-modeling-definition/transforms/domain-data-dictionary-component/transform.md`
- Domain Catalog ADR 0001, requiring MOF conformance for the governing model definition
- Project ADR 0001, organizing product refinement as a flat layer graph
- The user's stated business-analyst workflow and requirement for a deployable, DAMA-informed data dictionary

The user's 2010 DAMA-DMBOK edition has not been inspected page by page for this execution. Accordingly, this design inherits the source artifact's DAMA orientation but makes no new DAMA conformance claim.

## 4. Authority and Invariants

The following invariants determine the component boundaries:

1. `CMOF-GOV` governs `DML-DEF`; `DML-DEF` governs each `BDM-*` model. Stored copies do not acquire authority to redefine their source.
2. One catalog record authority owns each `CAT-DATA` identity and revision. Capability modules do not create private copies that can diverge.
3. Conceptual, logical, relational-logical, physical-design, and observed models are distinct artifacts with distinct purposes.
4. An accepted model revision is historical evidence and is not changed in place. Maintenance creates another revision and explicit lineage.
5. Cross-artifact meaning is recorded in `DML-REA` realization records, not inferred from names, order, containment, or similar structure.
6. A descendant remains derived from its recorded source revision. An upstream change makes affected descendants candidates for regeneration; it does not rewrite or relabel them silently.
7. Intended design, deployment material, deployment execution, runtime state, observation, and comparison are different facts.
8. External observation is evidence, not design authority. Promotion of a discovered change requires an explicit revision at the earliest model that owns the meaning.
9. The catalog stores `CAT-DATA`; subject systems store or exchange `BDM-DATA`.
10. Portable physical constructs and target-native metadata remain distinguishable and are interpreted only under an identified target and profile version.
11. OCL validation over modeled state, target-language expressions, transformations, deployment effects, and external collection are separate execution domains.
12. A represented model must be reconstructable with identity, ordering, multiplicity, expressions, native metadata, revisions, and realization links intact.

## 5. Expected Change Profile

| Change type | Expected importance | Evidence and boundary consequence |
| --- | --- | --- |
| Business understanding changes | High | Domain exploration is the entry workflow; change must begin in conceptual or semantic artifacts and expose affected descendants |
| Logical modeling choices change | High | Normalization, identities, structures, and constraints evolve independently of business terminology and physical targets |
| New physical target or target version | High | `DML-PHY` explicitly supports target/version profiles; target change should not alter conceptual or logical capabilities |
| New physical technology family | Medium to high | The source supports relational, document, graph, API, schema-document, and stored-asset branches; shared lifecycle must remain stable |
| Governing definition or OCL rule changes | Medium, high impact | Every conforming artifact may require revalidation; authority must be centralized rather than duplicated by model level |
| Realization or transformation policy changes | Medium | Mapping is judgment-bearing and many-to-many; it changes independently of either endpoint's internal vocabulary |
| Deployment tooling changes | Medium | External executors and packaging mechanisms vary without changing catalog semantics |
| Observation coverage changes | High | Metadata inventories and collectors vary by target/version; observed evidence must carry profile and coverage context |
| Repository technology changes | Low frequency, high impact | The relational realization may change, but `CAT-DATA` meaning and lossless reconstruction obligations must remain stable |
| Collaboration and governance features | Unknown | The source deliberately defers roles, permissions, workspaces, and approvals; the component must not bake in an unverified workflow |

## 6. Componentization Models Considered

### 6.1 Model A: Abstraction-Stage Components

This model follows the visible analyst workflow by assigning each modeling level to a separate component.

| Component | Area of responsibility | Owns state/data? |
| --- | --- | --- |
| Conceptual Modeling | Domains, business vocabulary, conceptual entities, properties, relationships, and constraints | Conceptual records |
| Logical Modeling | Logical entities, attributes, identifiers, datatypes, relationships, and constraints | Logical records |
| Physical Modeling | Relational-logical and target-specific physical designs | Relational and physical records |
| Deployment Management | Deployment packages, executions, and target environments | Deployment records |
| Observation and Drift | Observed models, coverage, comparison, and disposition | Observation records |
| Shared Dictionary | Cross-level lookup, identity, and mappings | Shared reference and realization records |

#### Boundaries and interfaces

- Each stage offers create, revise, validate, and query interfaces for its own artifact kind.
- Each downstream stage consumes an accepted revision from the preceding stage and produces mappings back to it.
- Deployment Management consumes physical designs; Observation and Drift consumes intended designs and collector output.
- Shared Dictionary supplies identifiers and cross-stage queries.

#### Collaboration and change locality

The workflow reads naturally from left to right, and a change confined to one model's internal vocabulary is local. However, artifact identity, validation, realization, revision, and impact analysis cut across every stage. Those responsibilities either become duplicated or accumulate in the Shared Dictionary until it becomes the actual system core.

| Change type | Locality | Components affected | Evidence |
| --- | --- | --- | --- |
| Add a conceptual construct | Medium | Conceptual, Shared Dictionary, validation consumers | Identity and governing rules cross the stage boundary |
| Add a target profile | High | Physical Modeling, possibly Deployment and Observation | Mostly local to physical concerns |
| Change revision semantics | Low | All | Every stage owns revisions independently |
| Trace one business concept to runtime | Low | All | The principal use case crosses every boundary |

#### Risks

- The component boundaries coincide with artifacts, not stable responsibilities.
- Cross-level traceability becomes distributed coordination.
- Similar lifecycle and validation behavior is repeated, conflicting with DRY.
- A forced sequential pipeline contradicts branches that omit `BDM-REL` or produce multiple physical targets.

### 6.2 Model B: Undivided Data Dictionary

This model uses one application component for all authoring, validation, mapping, deployment evidence, observation, and persistence behavior.

| Component | Area of responsibility | Owns state/data? |
| --- | --- | --- |
| Domain Data Dictionary | All `CAT-DATA` and all behavior in the component scope | Yes |
| External Target Tools | Deployment and collection outside the catalog | External only |

#### Boundaries and interfaces

- One interface exposes every authoring, query, validation, deployment, and observation operation.
- One internal state model stores definitions, model families, realizations, profiles, and evidence.
- Target tools receive deployment material and return execution or observation evidence.

#### Collaboration and change locality

This is the smallest deployable shape and gives one clear authority. It avoids distributed transactions and premature service boundaries. Its weakness is internal: without explicit capability boundaries, target-specific behavior, lifecycle policy, validation, and model editing can call each other freely and change together.

| Change type | Locality | Components affected | Evidence |
| --- | --- | --- | --- |
| Add a conceptual construct | Medium | Undivided component | One deployment, but no protected internal boundary |
| Add a target profile | Medium | Undivided component | Target behavior can leak into shared model behavior |
| Change revision semantics | High | Undivided component | One authority owns the rule |
| Replace deployment executor | High | Boundary adapter | External collaboration is explicit |

#### Risks

- KISS at deployment level can become accidental coupling internally.
- Target-native growth can dominate the general catalog code.
- Validation logic may become entangled with mutation and persistence.
- The absence of named responsibilities makes later extraction arbitrary.

### 6.3 Model C: Catalog Kernel with Capability Modules

This model keeps one deployable Domain Data Dictionary boundary for the first increment but defines internal components around stable responsibilities rather than modeling stages.

| Component | Area of responsibility | Owns state/data? |
| --- | --- | --- |
| Catalog Record Kernel | Identity, domain and family membership, revision lineage, status, provenance, governing references, repository atomicity, query, and lossless import/export | Sole persistence authority for `CAT-DATA` |
| Model Construction | Commands and views for `DML-SEM`, `DML-CON`, `DML-LOG`, `DML-REL`, and intended `DML-PHY` content | No independent store; semantic ownership of authoring rules |
| Conformance Validation | CMOF production checks, `DML-DEF`/OCL validation, and diagnostics | No independent authoritative state |
| Realization and Impact | `DML-REA` correspondence, introduced/omitted detail, coverage, refinement DAG, and affected-descendant analysis | Realization and impact records through the kernel |
| Target Capability Gateway | Identified physical-target profiles, native metadata vocabulary, datatype/expression mappings, packaging capability, and collector capability contracts | Profile records through the kernel; target behavior remains replaceable |
| Deployment and Reconciliation | Immutable packages, execution requests and records, observed-model intake, coverage assessment, comparison, and disposition | Deployment and observation records through the kernel |

These are logical component boundaries. They do not imply separately deployed services or separate databases.

#### Boundaries and interfaces

- Only the Catalog Record Kernel commits or reconstructs `CAT-DATA`.
- Model Construction cannot define new language vocabulary; it interprets the selected `DML-DEF` revision.
- Conformance Validation evaluates snapshots and reports results; it does not mutate the model to make validation pass.
- Realization and Impact owns cross-artifact correspondence but not either endpoint's content.
- Target Capability Gateway isolates product/version-specific semantics from shared modeling and lifecycle behavior.
- Deployment and Reconciliation coordinates durable catalog records around external actions but does not claim transactional control of target infrastructure.

#### Collaboration and change locality

| Change type | Locality | Components affected | Evidence |
| --- | --- | --- | --- |
| Add a conceptual or logical construct already permitted by `DML-DEF` | High | Model Construction, Validation | Kernel retains generic identity and revision behavior |
| Change `DML-DEF` | Medium | Validation, Model Construction, possibly affected capability | Central definition reference makes impact discoverable |
| Add a target profile or version | High | Target Capability Gateway, Validation | Shared lifecycle and authoring remain unchanged |
| Change realization policy | High | Realization and Impact, Validation | Endpoint components remain authoritative for content |
| Replace deployment executor or collector | High | Target Capability Gateway, Deployment and Reconciliation | External ports isolate provider behavior |
| Change revision or provenance policy | Medium | Kernel plus callers | Centralized rule prevents inconsistent stage-specific semantics |
| Change repository technology | Medium | Kernel boundary | Other capabilities consume catalog operations, not repository structures |

#### Risks

- The kernel can become a generic dumping ground unless its responsibility stays limited to authority, lifecycle, and representation fidelity.
- Capability modules can become artificial ceremony if their interfaces are made remote too early.
- Validation and authoring must share the same selected definition revision without sharing mutation authority.
- External deployment and collection require reconciliation because catalog commits and target effects cannot be one atomic action.

## 7. Comparative Assessment

| Model | Responsibility clarity | Boundary clarity | Interface simplicity | Change locality | Main tradeoff |
| --- | --- | --- | --- | --- | --- |
| A. Abstraction-Stage Components | Medium | Medium | Medium | Low | Mirrors the workflow but distributes identity, revision, validation, and traceability |
| B. Undivided Data Dictionary | Low | High externally, low internally | High initially | Medium | Simplest deployment but permits unrelated capabilities to couple internally |
| C. Catalog Kernel with Capability Modules | High | High | Medium | High | Requires disciplined internal boundaries while retaining one deployable unit |

## 8. Selected Component Model

The product owner selected **Model C: Catalog Kernel with Capability Modules** on 2026-07-26.

It preserves KISS by keeping one deployable component and one catalog authority for the first increment. It preserves DRY by centralizing identity, revision, provenance, and lossless representation instead of reimplementing them for conceptual, logical, and physical artifacts. It gives volatile target-specific behavior its own boundary without pretending that every adapter should be an independent service.

Most importantly, its boundaries follow the project's actual invariants. The product exists to preserve meaning and explicit realization across refinements. Those relationships remain first-class responsibilities rather than integration glue between model-level silos.

```text
Business analyst / data architect
                 |
          Model Construction
                 |
       +---------+----------+
       |                    |
Conformance Validation   Realization and Impact
       |                    |
       +---------+----------+
                 |
        Catalog Record Kernel
                 |
       CAT-DATA authority boundary

Target Capability Gateway
       |                    |
external deployer     external collector
       |                    |
       +---- Deployment and Reconciliation ----+
                              |
                    Catalog Record Kernel
```

The diagram shows authority and collaboration, not process hosting or network topology.

## 9. Recommended Interfaces

The names below describe capabilities, not transport protocols.

### 9.1 Interfaces offered by the component

| Interface | Responsibility | Principal consumers |
| --- | --- | --- |
| Domain and Model-Family | Establish domains, model families, artifact identities, drafts, revisions, status, and provenance | Business analyst, data architect |
| Model Construction | Create and revise semantic, conceptual, logical, relational-logical, and intended physical content permitted by the selected definition | Business analyst, data architect |
| Validation and Diagnostics | Validate a snapshot against its governing definition and return rule-specific evidence without mutation | Authoring workflow, acceptance workflow, import workflow |
| Realization and Impact | Record mappings and rationales; query upstream/downstream coverage; identify descendants affected by a proposed change | Data architect, maintenance workflow |
| Catalog Query and Interchange | Retrieve and round-trip definitions, model families, revisions, provenance, deployment evidence, and observations | Model consumers, migration and verification tools |
| Deployment Package | Produce and identify immutable target artifacts from one physical-design revision using one profile version | Data architect, deployment operator |
| Deployment Evidence | Request execution through a configured collaborator and record attempt, outcome, and external reference | Deployment automation, operator |
| Observation Intake | Accept a collector-produced observed model with environment, time, collector, evidence digest, profile, and coverage | Metadata collector |
| Physical Comparison | Compare one intended physical revision with one observed revision and record differences and dispositions | Data architect, operator |

### 9.2 Interfaces consumed by the component

| Interface | Provider | Boundary condition |
| --- | --- | --- |
| Governing Definition | Versioned CMOF and `DML-DEF` provider | Definition identity and digest must be retained; the component cannot rewrite the definition |
| Target Profile | Standard- or product-specific capability provider | Product, version, authority, vocabulary, mappings, and coverage inventory are explicit |
| Deployment Execution | External deployment tool or operator | Receives immutable material and an execution identity; results are evidence, not proof of deployed equivalence |
| Metadata Collection | External collector | Returns evidence tied to one environment, time, collector version, target profile, and stated coverage |
| Artifact Content | External content-addressable or document facility if needed | The catalog retains identity and digest even if large target-owned content is referenced rather than embedded |

## 10. Principal Collaborations

### 10.1 Domain exploration and conceptual modeling

1. The analyst establishes a domain and model family under an identified `DML-DEF` revision.
2. Model Construction creates semantic and conceptual elements in a draft `BDM-CON` revision.
3. Conformance Validation evaluates the snapshot and returns diagnostics.
4. Acceptance commits the valid revision and its provenance through the Catalog Record Kernel after validation succeeds.

The design does not require the analyst to choose tables, target datatypes, or indexes during this collaboration.

### 10.2 Logical and physical refinement

1. The architect creates a new `BDM-LOG`, optional `BDM-REL`, or `BDM-PHY` draft from identified source revisions.
2. Realization and Impact records element correspondence, introduced detail, omission, and rationale.
3. The applicable target capability supplies target/version vocabulary and mappings for physical work.
4. Validation checks both the target artifact and realization coverage before acceptance.
5. The kernel accepts the target revision and its realization set as one coherent catalog change.

Several physical designs may realize the same logical revision. Omitting `BDM-REL` on a non-relational branch is valid when the realization is explicit.

### 10.3 Deployment

1. A valid intended `BDM-PHY` revision and one target-profile version produce an immutable deployment package.
2. Realization records connect package artifacts to the physical elements they create or alter.
3. Deployment and Reconciliation records the planned attempt before handing the package to an external executor.
4. The returned execution reference and outcome complete the attempt record.
5. A successful outcome does not mark the runtime equivalent to the design; observation is required for that evidence.

No catalog transaction is claimed to be atomic with the external infrastructure action. Recovery depends on the durable attempt identity, immutable package digest, external execution reference, and later observation.

### 10.4 Observation, comparison, and maintenance

1. A collector reads a named environment using an identified target/profile version.
2. Observation Intake records a new `BDM-OBS` plus collection provenance and coverage evidence.
3. Physical Comparison relates it to one intended `BDM-PHY` and records missing, unexpected, changed, or equivalent facts.
4. A human or policy records a disposition for each material difference.
5. A legitimate semantic change restarts at the earliest conceptual, logical, or physical-design revision that owns it; unauthorized drift produces corrective deployment from existing intent.

The observed model remains unchanged as evidence regardless of the disposition.

## 11. State, Commit, and Recovery Semantics

### 11.1 Catalog state authority

- The Catalog Record Kernel is the only authority that commits `CAT-DATA`.
- Drafts may evolve, but an accepted revision is immutable. Supersession creates a new revision and preserves the previous one.
- An accepted target revision and the realization records required to interpret it become visible together or not at all.
- Every validation, transformation, packaging, deployment, and collection result names the exact input revisions and profile versions it used.
- Read models, indexes, caches, and exports are replaceable projections and never independent authorities.

### 11.2 Failure boundaries

- Validation failure leaves the draft and diagnostics available but does not accept the revision.
- Packaging failure creates no deployable package identity unless its contents and digest are complete.
- Deployment may fail after external effects have occurred or before a final result is recorded. The attempt remains unresolved until execution evidence or observation reconciles it.
- Collection failure does not produce a complete observation. Partial evidence may be retained only with coverage `incomplete` or `unknown`.
- Comparison never mutates either input model.
- Import failure does not partially accept a model family. Fidelity validation precedes acceptance.

These are behavioral constraints for later architecture. The transaction mechanism, job protocol, retry policy, and storage implementation remain deferred.

## 12. First Deployable Increment

The first increment should prove the entire meaning-preservation loop with narrow technology breadth. It includes:

- one domain and multiple `BDM-FAMILY` instances whose model members are revisioned;
- semantic, conceptual, logical, optional relational-logical, and physical-design authoring;
- explicit realization and affected-descendant queries;
- validation against one identified `DML-DEF` revision;
- one PostgreSQL physical target profile whose version and metadata inventory are selected in the physical refinement;
- immutable deployment-package production for that target;
- external execution-result recording;
- observed metadata intake for the same target and declared coverage;
- intended-versus-observed comparison and maintenance disposition;
- catalog queries that trace a business concept through every realized artifact; and
- lossless export and re-import of the exercised definitions, model family, mappings, and lifecycle evidence.

The component boundaries remain capable of adding other target families, but the first increment does not need to implement every relational, NoSQL, API, schema, and stored-asset profile simultaneously. Breadth is added through the Target Capability Gateway after the end-to-end invariant is demonstrated.

## 13. Traceability to the Governing Definition

| Recommended component | Principal governing scope | Responsibility traced |
| --- | --- | --- |
| Catalog Record Kernel | `DML-DEF` Core package, `DML-SEM`, `CAT-DATA` obligations | Identity, domains, revisions, status, provenance, model containment, faithful persistence |
| Model Construction | `DML-SEM`, `DML-CON`, `DML-LOG`, `DML-REL`, intended `DML-PHY` | Model-specific vocabulary and authoring boundaries |
| Conformance Validation | `CMOF-GOV`, `DML-DEF`, OCL usage profile, `DM-*` rules | Definition and model conformance without mutation |
| Realization and Impact | `DML-REA` | Many-to-many correspondence, introduction, omission, rationale, coverage, refinement DAG |
| Target Capability Gateway | `DML-PHY`, physical metadata profiles | Target/version interpretation, native metadata, datatype and expression boundaries |
| Deployment and Reconciliation | `DML-DEP`, `DML-OBS` | Packages, execution evidence, observations, coverage, comparisons, dispositions |

### 13.1 Placement of explicit model-family identity

The canonical registry names `BDM-FAMILY` and says that it groups the purposeful models for one business scope. The structural definition does not currently supply a corresponding class or membership relationship:

- `DataDomain` groups meaning by domain but cannot distinguish multiple model families within one domain;
- `DataModel::domain` assigns a model to a domain but not to a family;
- `lineageIdentifier` connects revisions of one artifact, not conceptual, logical, and physical artifacts of different kinds; and
- realization records state correspondence but do not establish one authoritative family boundary.

Inferring membership from names, containment, or reachability would violate the explicit-relationship principle. However, absence of a general `ModelFamily` class from `DML-DEF` is not by itself an expressiveness gap: `DML-CON` permits the Domain Catalog's own conceptual model to define `Model Family` as a business entity and its explicit membership relationship.

For the current branch, model-family identity and membership belong to the Domain Catalog repository conceptual model. This keeps catalog-specific organization out of the general modeling language. If later evidence shows that family membership must participate in conformance or exist independently of the catalog, the decision moves upstream into `DML-DEF` and affected descendants are regenerated.

The canonical role name `BDM-FAMILY` still lacks a structural catalog realization until the conceptual model defines it. Descendants must use that explicit repository concept rather than infer grouping, and must not promote it into `DML-DEF` without evidence that the responsibility is general.

No component responsibility currently demonstrates a new governing-model primitive or definition-language gap. Executable transformation behavior, repository mapping, validation-report retention, and target-profile contracts still require later refinement.

## 14. Rejected Alternatives

- **Separate deployable service per model level:** rejected because the principal behavior—preserving identity and realization across levels—would become distributed integration, while lifecycle and validation would be duplicated.
- **One unstructured application component:** rejected as the enduring component model because target-specific growth and validation behavior would have no protected change boundary. It remains an acceptable deployment shape if it implements the recommended logical boundaries.
- **Separate database or source of truth per capability:** rejected because it creates cross-store consistency obligations before independent scaling or ownership needs have been observed.
- **Observed infrastructure as the catalog authority:** rejected because it collapses evidence into intent and makes unauthorized drift indistinguishable from an approved design change.
- **Relational schema as the universal internal model:** rejected because it would distort non-relational physical targets and confuse the repository realization (`CAT-PHY`) with the governed modeling language (`DML-DEF`).

## 15. Decisions Made

- The Domain Data Dictionary is one deployable component boundary for the first increment.
- Internally it uses a catalog kernel plus capability modules organized by stable responsibility, not by conceptual/logical/physical stages.
- One Catalog Record Kernel is the persistence and revision authority for `CAT-DATA`.
- Model stages remain separate artifacts within one family and can branch rather than forming one mandatory pipeline.
- Realization and impact analysis are first-class responsibilities independent of endpoint authoring.
- Validation observes a model snapshot and reports evidence; it does not repair or mutate the model.
- Target-specific semantics enter through an identified target capability boundary.
- Deployment execution and metadata collection remain external effects surrounded by durable catalog evidence.
- Accepted revisions, deployment packages, and observations are immutable evidence.
- The first increment proves one complete target loop before adding broad target coverage.
- PostgreSQL is the required first physical deployment target; that constraint does not introduce tables, columns, SQL types, or PostgreSQL-native metadata into conceptual or logical models.
- The future API is capability-oriented. LLMs, other AI agents, automations, and human-oriented interfaces invoke the same application capabilities rather than receiving separate privileged paths to the catalog store.
- Common capability access does not imply identical authorization. Identity and policy may limit which callers can invoke a capability, but client type does not create a separate functional implementation.

## 16. Architecture Constraints Implied

- Preserve the six logical component boundaries even if they are implemented and deployed together.
- Provide one authoritative commit boundary for catalog records and do not expose repository tables as component interfaces.
- Bind every artifact, validation, realization, package, observation, and comparison to exact revisions of its governing inputs.
- Make acceptance atomic with the realization and provenance needed to interpret the accepted artifact.
- Do not rely on a distributed transaction with subject infrastructure; make external attempts identifiable and reconcilable.
- Keep target adapters replaceable and prevent native target vocabulary from leaking into conceptual or logical interfaces.
- Treat definition validation and subject-data validation as separate OCL evaluation environments.
- Preserve target-owned expressions and artifacts in their native language while linking them to upstream meaning.
- Make export/import fidelity independently testable before claiming lossless repository realization.
- Keep read projections disposable and derivable from authoritative `CAT-DATA`.
- Do not split logical modules into services until observed scaling, failure isolation, release cadence, or ownership evidence justifies it.
- Keep PostgreSQL choices in the physical repository model and infrastructure design; upstream models express meaning and technology-neutral structure.
- Expose component behavior through one capability boundary used by machine and human-facing clients; no client may acquire semantic authority by bypassing that boundary and editing repository structures directly.

## 17. Decisions Explicitly Deferred

- Repository database product and the `CAT-PHY` relational schema
- Programming language, frameworks, process topology, and hosting platform
- User interface and transport protocols for offered interfaces
- PostgreSQL version, extensions, metadata inventory, repository schema, and physical tuning
- Transformation language and the division between automatic generation and human decisions
- OCL engine and classifier/property mapping for subject-data evaluation
- Deployment executor and metadata collector implementations
- Storage of large native artifact bodies versus content references
- Authentication, authorization, workspaces, collaboration, and approval workflow
- Branching and merge semantics for concurrent model editing
- Retention, archival, backup, and disaster-recovery policies
- Performance, scale, availability, and latency objectives
- Whether any logical module later becomes an independently deployed service

## 18. Open Questions

1. Which PostgreSQL version, extension policy, and catalog inventory should govern the first physical target profile?
2. Which transformations must be executable in the first increment, and which should initially be recorded human decisions?
3. What human acceptance process is required around the draft/accepted/superseded/retired artifact statuses already defined?
4. How will a target capability prove the completeness of its metadata inventory and collector coverage?
5. What exact interchange representation will serve as the independent round-trip oracle: CMOF/XMI alone or CMOF/XMI plus referenced native artifacts?
6. How are changes to `DML-DEF` applied to existing model families: revalidation only, explicit migration, or both?
7. Which actor and decision provenance is minimally required before collaboration and access-control semantics are designed?
8. Does the first increment need to deploy changes itself, or is package production plus externally supplied execution evidence sufficient?
9. Does model-family membership remain a Domain Catalog repository concept, or will later evidence require promoting it into `DML-DEF` as a general modeling construct?
10. What is the smallest stable capability vocabulary that supports LLMs, agents, automations, and human-facing interfaces without exposing repository-specific operations?

## 19. Validation Result

This design satisfies the structural componentization conditions in its owning transform by inspection. It does not make the layer effective because:

- `DML-DEF` is still draft and not effective;
- model-family identity is provisionally assigned to the downstream catalog conceptual model and still requires product-owner review;
- DAMA and several normative-standard checks remain pending upstream;
- no repository round-trip or target-profile implementation has validated the design constraints; and
- product owner acceptance is pending.

The next component work is the Domain Catalog repository conceptual model. It must define model-family identity and membership explicitly, then drive the logical model. PostgreSQL and the capability API remain downstream constraints rather than reasons to move storage or interface concepts into this component model.
