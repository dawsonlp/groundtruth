# Domain Data Dictionary Capability API Architecture

## Purpose

Define the architecture that makes the Domain Data Dictionary usable above its reflective persistence representation. Preserve the sparse hybrid authority while giving capability implementers, agents, automations, and human-facing interfaces typed and readable semantic operations.

## Scope

This architecture covers:

- the boundary between clients, capability behavior, typed projections, validation, and the Catalog Record Kernel;
- preservation of the six Model C component responsibilities inside one first-increment deployable component;
- command, query, diagnostic, and external-effect consequences;
- the first self-modeling and PostgreSQL-reflection test;
- the thin-user-interface constraint;
- performance and comprehensibility constraints that downstream technical design must test; and
- the decision boundary for reconsidering a type-specific base/extension-table realization.

It does not define endpoint paths, transport schemas, authentication policy, UI framework, persistence algorithms, OCL engine, cache technology, deployment topology, or production code.

## Inputs Consulted

- Model C Domain Data Dictionary component design, revision `5a0993d`
- `CAT-CON/domain-data-dictionary@1` conceptual model and build design, revision `73ed9df`
- `CAT-LOG/domain-data-dictionary@1` logical design and logical data model, revision `5728636`
- PostgreSQL technical design and runtime transform
- PostgreSQL realization manifest and verification evidence through runtime revision `d969917`
- product-owner decisions supplied 2026-07-28

## Governing Inputs

- The Domain Data Dictionary is one deployable component for the first increment.
- Model C preserves one Catalog Record Kernel plus Model Construction, Conformance Validation, Realization and Impact, Target Capability Gateway, and Deployment and Reconciliation responsibilities.
- The hybrid logical authority uses typed catalog-specific governance records, reflective CMOF/DML content, and derived typed projections.
- PostgreSQL is the first repository realization.
- Machine and human-facing clients use the same capability meanings.
- User interfaces remain thin and do not own product business logic.
- The type-specific base/extension-table path remains a fallback physical realization, not the selected authority on this branch.

## Supporting Context

- The live PostgreSQL kernel is structurally operational but contains no loaded governing definitions, catalog models, definition-aware validator, or generated typed projections.
- Structural tests prove identity, references, recursive values, provenance, and generic round trips; they do not yet prove real `Table`, `View`, `Column`, constraint, or `Index` behavior.
- The product owner values the flexibility and sparseness of the current authority but requires evidence about large-catalog performance and code comprehensibility.
- The product owner described the first semantic stage as "conceptual with anthological." This architecture provisionally interprets the intended word as "ontological" and leaves correction open.

## Decisions Made

- Continue the hybrid reflective-kernel approach.
- Expose named application capabilities rather than repository CRUD.
- Keep the reflective kernel private behind capability, projection, validation, and repository boundaries.
- Make typed semantic projections the normal query surface for clients and capability implementation.
- Keep commands, queries, diagnostics, and external effects distinct because they have different authority and recovery consequences.
- Preserve one authoritative commit boundary in the Catalog Record Kernel.
- Keep interfaces thin; no interface owns semantic validation, lifecycle transitions, projections, comparison, or durable mutation behavior.
- Use the Domain Catalog's own model and its running PostgreSQL realization as the first end-to-end test.
- Treat performance and developer comprehensibility as measured architectural validation concerns.
- Reconsider type-specific base/extension tables only through an explicit sibling realization decision supported by evidence.

## Approved Component Model

The architecture preserves these responsibilities without turning them into independently deployed services:

| Responsibility | Architectural ownership | Excluded ownership |
| --- | --- | --- |
| Catalog Record Kernel | Identity, revision, provenance, authoritative commit, reconstruction, and durable query primitives | Client-specific behavior or duplicated semantic records |
| Model Construction | Semantic commands and views for creating and revising governed model content | Persistence representation and independent storage |
| Conformance Validation | Definition-aware validation and diagnostics over identified snapshots | Silent repair or mutation |
| Realization and Impact | Explicit mappings, coverage, rationale, and affected-descendant analysis | Ownership of either mapped endpoint |
| Target Capability Gateway | Identified target/profile vocabulary, mappings, packaging, and observation contracts | Upstream conceptual or logical meaning |
| Deployment and Reconciliation | Packages, attempts, observations, comparisons, differences, and dispositions | Treating observed state as intended authority |

## Architecture Structure

```text
human UI     agent/tool     automation     integration client
    \            |              |                  /
     +---- thin transport and presentation adapters --------+
                              |
                 client-independent capability boundary
                   /          |           |          \
              commands      queries    diagnostics   external attempts
                   \          |           |          /
                    typed semantic projections and inputs
                              |
       +---------------- Model C responsibilities ----------------+
       | construction | validation | realization | target | reconcile |
       +-----------------------------------------------------------+
                              |
                 Catalog Record Kernel commit boundary
                              |
                 private reflective repository mapping
                              |
                         PostgreSQL runtime
```

The diagram describes authority and dependency direction. It does not require separate network services. The first increment remains one deployable application component plus PostgreSQL and its migration process.

### Client-independent capability boundary

The capability boundary presents operations in governed product language. Ordinary clients work with identified definitions, model families, artifact revisions, model elements, validations, mappings, target profiles, observations, comparisons, and provenance. They do not work with `catalog_object`, `property_occurrence`, `value_node`, table names, joins, or migration details.

The same capability meaning may have more than one transport representation. Transport adapters translate syntax, identity credentials, request framing, and response framing; they do not alter semantic preconditions, authority consequences, validation rules, or transaction meaning.

### Typed semantic projection

Typed projection is a derived architectural facility over an exact governing-definition revision and kernel snapshot. It:

- resolves governed classes and inherited properties;
- reconstructs scalar, reference, ordered, unique, and recursively structured values;
- computes derived properties rather than reading competing stored facts;
- retains source object, property, and definition identities;
- reports missing, ambiguous, or invalid content as diagnostics; and
- may later be cached or materialized only as disposable, revision-bound derived state.

Projection does not become another writable model. A capability command changes kernel authority and then any derived representation is regenerated or invalidated.

### Command, query, diagnostic, and effect consequences

| Interaction kind | Consequence |
| --- | --- |
| Command | Requests an authorized change to authority-bearing catalog state and commits atomically through the kernel |
| Query | Returns a generic or typed view of an identified snapshot without mutation |
| Diagnostic | Reports validation, coverage, impact, or comparison evidence without silently changing the subject |
| External attempt | Records durable intent and identity around deployment or collection, performs no distributed transaction with the target, then records the observed outcome for reconciliation |

An endpoint or interface gesture is not the authority for these distinctions. The capability contract is.

### Bootstrap and definition trust

The first governing-definition load is an explicit bootstrap boundary, not an ordinary model-authoring shortcut. Bootstrap identifies the exact `CMOF-GOV` source, revision, content evidence, and responsible provenance; loads a complete closure atomically; and verifies the structural and self-conformance conditions available at that stage. Ordinary capability clients cannot silently replace the governing root or reinterpret an existing definition revision.

The mechanism for establishing trust, approving a replacement root, and recovering from a failed bootstrap remains a technical-design and product-policy decision. The architectural requirement is that bootstrap authority is visible, attributable, versioned, and distinct from importing or authoring ordinary governed models.

### Draft construction and validated projection

Model construction must support incomplete draft revisions without presenting them as valid accepted artifacts. A draft query may return a diagnostic semantic representation containing the facts that can be reconstructed plus explicit missing, ambiguous, or invalid-property evidence. It must not invent defaults or suppress violations to resemble a valid typed object.

An accepted typed projection is available only after the complete governed closure passes the required definition and lifecycle validation. Acceptance atomically binds the validated content, governing revisions, realization/provenance evidence, and resulting status. This distinction lets thin interfaces support incremental authoring while keeping validation authority in the capability boundary.

### Refinement and transformation boundary

The capability architecture represents every refinement attempt with identified sources, transform identity and revision, human inputs, candidate outputs, validation evidence, and disposition. Whether a particular transform is executed automatically by the first increment or performed by a human and recorded through the capability boundary is a scoped product decision. A generated candidate remains draft until its validation and acceptance conditions pass.

## Boundary And Interface Definitions

| Consumer | Provider | Architectural contract |
| --- | --- | --- |
| Thin clients | Capability boundary | Named commands, queries, diagnostics, and attempt semantics using governed identities and revisions |
| Capability boundary | Model Construction | Create or revise governed content without repository-shaped operations |
| Capability boundary | Conformance Validation | Validate an exact snapshot against an exact governing-definition revision and return evidence |
| Capability boundary | Realization and Impact | Record and query explicit correspondence, coverage, and affected descendants |
| Capability boundary | Target Capability Gateway | Resolve identified target/profile semantics and request packaging or observation behavior |
| Capability boundary | Deployment and Reconciliation | Initiate identifiable attempts and record observation, comparison, and disposition evidence |
| Capability responsibilities | Typed projection | Obtain readable, traceable semantic records from reflective authority |
| Capability responsibilities | Catalog Record Kernel | Commit or reconstruct authoritative records through one boundary |
| Catalog Record Kernel | PostgreSQL repository mapping | Persist the six logical authorities without exposing their physical form upstream |
| Target Capability Gateway | PostgreSQL observer | Read target metadata under an identified profile without treating observation as intent |

## First End-to-End Test: The Catalog Models Itself

The first test is a vertical consequence-bearing scenario, not a demonstration fixture:

1. Load identified machine-readable `CMOF-GOV` and `DML-DEF` revisions needed to govern the test.
2. Create a Domain Catalog model family and its conceptual model through capability commands.
3. Represent the product's conceptual and provisionally interpreted ontological meaning without collapsing those levels unless the governing definition explicitly does so.
4. Refine the model through the applicable logical and PostgreSQL physical-design artifacts, preserving explicit realization mappings and provenance.
5. Observe the running local Domain Catalog PostgreSQL database through an identified PostgreSQL target profile.
6. Store the observation as a distinct observed physical-model revision.
7. Compare intended and observed models through capability diagnostics, retaining coverage, differences, evidence, and dispositions.
8. Query the entire chain through typed capability projections.
9. Exercise the same capabilities through at least one machine client and one thin human-facing interface without duplicating business logic.

Passing requires lossless reconstruction, definition-aware validity, explicit intended/observed distinction, and traceability from a client-visible field to kernel identity and governing definition.

## Performance And Comprehensibility Constraints

The sparse authority is accepted as a hypothesis whose costs must be measured.

### Query boundedness

- A capability query identifies its snapshot, projection family, traversal scope, and result bounds.
- No client operation implies an unbounded recursive traversal of the catalog.
- Collection and graph-shaped results support bounded continuation without weakening semantic identity or order.

### Batch interpretation

- Projection architecture supports interpreting sets and closures, not only one object-property lookup at a time.
- Definition, property, and datatype resolution may be reused within an exact definition revision.
- Downstream technical design must prevent client access patterns from producing repository-level request multiplication.

### Derived acceleration

- Indexes, cached projections, or materialized read models may be introduced when measurements justify them.
- Every accelerated representation names its source revision and can be discarded and rebuilt.
- No performance optimization becomes a competing writable authority.

### Evidence

Technical design must define increasing catalog-size and graph-shape workloads, capture query plans and resource use, and measure representative capability latency and throughput. It must test both cold derivation and permitted warmed/derived paths. Numeric acceptance thresholds require product-owner input; this architecture does not invent them.

### Readability

- Capability contracts and typed projections use product vocabulary rather than storage vocabulary.
- Repository mapping remains localized behind an explicit boundary.
- Transport adapters and interfaces do not contain alternative validation or lifecycle implementations.
- A maintainer can trace each returned semantic field to its governing property and authoritative kernel fact.
- Technical design and tests must demonstrate the path for representative `Table`, `View`, `Column`, primary key, foreign key, check constraint, and `Index` capabilities.

## Alternative Physical Realization Retained

A type-specific base/extension-table realization remains available as a sibling alternative. It is reconsidered when measured evidence shows that the selected realization cannot meet accepted performance, operational, or maintainability conditions after ordinary indexing, bounded queries, batched projection, and disposable derived acceleration have been tested.

Selecting that alternative requires an explicit human decision and a source-colocated transform. It must identify whether extension tables are authoritative physical decomposition or derived projections, preserve one writable representation for each fact, and prove the same self-modeling and round-trip scenario. It must not be introduced piecemeal into this branch as an undocumented second authority.

## Decisions Explicitly Deferred

- Endpoint paths, resource shapes, RPC or query protocol, and error wire format
- API description and tool-description formats
- Authentication, authorization, workspaces, approval policy, and rate limits
- Concurrency tokens, revision-conflict protocol, and detailed transaction design
- OCL or other definition-evaluation engine
- Projection implementation, query plans, caching, or materialization technology
- PostgreSQL collector implementation and exact target-profile inventory
- UI frameworks, navigation, visualization, and client-side state technology
- Numeric performance, scale, availability, and latency objectives
- Production deployment, observability stack, backup, and recovery design

## Open Questions

- Does "anthological" mean "ontological," and what governed artifact distinguishes that work from conceptual modeling?
- What is the smallest first capability vocabulary that completes the self-modeling scenario without degenerating into repository CRUD?
- Which capability is the first authority-changing vertical slice: definition import, model-family creation, conceptual revision authoring, or another product-owner-selected action?
- What initial catalog-size, relationship-density, and latency targets should performance tests use?
- Which machine and human-facing clients constitute sufficient proof that the capability meaning is truly shared?
- Does the first increment import an existing conceptual artifact, author one incrementally, or support both?

## Questions For Product Owner

- Confirm or correct the provisional interpretation of "anthological" as "ontological."
- Select the first authority-changing capability slice after the architecture review.
- Supply initial performance and scale expectations before technical-design acceptance.

## Decisions Requested

- Accept, revise, or reject this capability-API architecture.
- Confirm that interfaces may perform non-authoritative ergonomic checks while the capability boundary remains the sole semantic validator.
- Confirm that the type-specific table approach remains a fallback sibling realization rather than parallel implementation work now.

## Recommended Next Step

Review this architecture as a senior systems engineer for fidelity to Model C and `CAT-LOG`. After findings are resolved and the product owner accepts the architecture, produce a capability-API technical design for the selected first vertical slice. Do not implement product endpoints before that slice and its validation consequences are explicit.

## Approval Status

Draft and non-effective. The product-owner direction is accepted as transform input; the resulting architecture is submitted for review.

## Senior Systems Engineer Review

### Findings

- `SSE-001` — resolved, medium: the first scenario depended on `CMOF-GOV`/`DML-DEF` loading without an architectural trust boundary. The architecture now distinguishes visible, attributable root bootstrap from ordinary imports and authoring.
- `SSE-002` — resolved, medium: typed projections were described only for valid content, leaving incremental conceptual authoring ambiguous. The architecture now distinguishes diagnostic draft representations from accepted typed projections without moving validation into clients.
- `SSE-003` — open, medium: technical design cannot establish a bounded first increment until the product owner confirms which authority-changing capability is first and whether the first increment executes refinements or records human-performed refinements.
- `SSE-004` — open, medium: the performance evidence architecture is coherent, but numeric scale and latency expectations remain absent. Technical design may define the measurement method but cannot decide what constitutes acceptable product performance without product-owner input.

### Required Changes

No further architectural correction is required before product-owner review. Resolve `SSE-003` and `SSE-004` as human inputs before accepting a capability-API technical design.

### Open Questions

- Confirm whether "anthological" means "ontological" and identify the governed artifact distinction, if any.
- Confirm the first authority-changing capability slice.
- Confirm whether initial model refinement is executed or recorded.
- Supply initial performance scale and latency expectations.

### Review Disposition

Accepted as a coherent exploratory architecture for product-owner review. It preserves Model C, the hybrid logical authority, one commit boundary, client-independent capability meaning, and thin interfaces. It is not yet sufficient authority for technical design because the open human scope and performance decisions materially affect that design.

## Product Owner Review

Pending review of the architecture artifact. The hybrid direction, self-modeling test, thin-interface constraint, and fallback-alternative treatment are accepted inputs.

## Sign-Off

### Author

- Signer: Codex
- Signer Type: agent
- Role: Architecture author
- Review Perspective: architecture drafting
- Disposition: submitted-for-review
- Summary Notes: Preserves the hybrid authority and Model C boundaries; defines a typed capability surface, self-modeling test, thin-client rule, and evidence boundary for performance and readability.
- Date: 2026-07-28

### Review Entries

- Reviewer: Codex
- Signer Type: agent
- Role: senior systems engineer
- Review Perspective: architecture fidelity and technical-design readiness
- Disposition: accepted for product-owner review; technical design blocked on `SSE-003` and `SSE-004`
- Date: 2026-07-28

### Product Owner Sign-Off

- Signer: product owner (human)
- Signer Type: human
- Status: pending architecture review

### Workflow Status

- Current Status: draft and non-effective
