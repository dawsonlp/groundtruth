# Transform: Logical Catalog Model to Capability API Architecture

## Status

- Transform status: draft
- Transform execution: first architecture draft complete
- Validation status: pending senior systems engineer and product-owner review
- Primary source layer: `domain-data-dictionary-logical-model`
- Semantic source revision: `5728636`
- Source decision supplement: product-owner acceptance recorded 2026-07-28
- Additional source layers: `domain-data-dictionary-conceptual-model`, `domain-data-dictionary-component`, and `domain-data-dictionary-postgresql-runtime`
- Target layer: `domain-data-dictionary-capability-api-architecture`
- Target effectiveness: draft and not effective

## Purpose

Refine the accepted hybrid logical authority into a capability-API architecture that gives machine and human-facing clients a typed semantic surface without exposing reflective repository structures. Define the architectural boundary, first self-modeling test, performance and readability obligations, and thin-client constraint without selecting endpoint shapes or writing implementation code.

## Source Basis

- `layers/domain-data-dictionary-logical-model/artifacts/logical-design.md` and `logical-data-model.md`, semantic revision `5728636`
- Model C component design, revision `5a0993d`
- conceptual build design and API refinement contract, revision `73ed9df`
- verified PostgreSQL structural realization through runtime revision `d969917`
- PostgreSQL realization evidence showing a working reflective kernel but incomplete definition-aware validation and typed projections

## Required Human Inputs

The product owner decided on 2026-07-28 to:

- continue the hybrid reflective-kernel approach because of its flexibility and sparse authoritative representation;
- retain type-specific base/extension tables as an alternative physical realization to reconsider if evidence warrants it;
- build the capability API before user interfaces so clients operate at a higher semantic level;
- use the Domain Catalog itself as the first modeling case, beginning with conceptual and provisionally interpreted ontological modeling, continuing through the design chain, and reflecting the local PostgreSQL database back into the catalog;
- explore the result through the capability API and later user interfaces; and
- keep user interfaces thin and free of product business logic, with the capability API owning semantic behavior and abstraction changes.

The product owner also identified two validation risks rather than resolving them by preference:

- performance as the reflective repository grows; and
- comprehensibility for people building or maintaining capability behavior.

## Procedure

1. Preserve the six approved Model C component responsibilities and the single Catalog Record Kernel authority.
2. Define one client-independent capability boundary for commands, queries, validation, diagnostics, observation, and comparison.
3. Keep reflective PostgreSQL objects private behind repository and projection interfaces.
4. Define typed projection as a derived architectural facility, not another writable authority.
5. Define the self-modeling and PostgreSQL-reflection sequence as the first end-to-end architecture test.
6. State performance, query-boundedness, batching, derivation, and observability constraints without inventing unapproved latency or scale targets.
7. State the thin-client boundary for human and machine-facing adapters.
8. Preserve type-specific extension tables as a separately selectable fallback realization rather than silently mixing authorities.
9. Record deferred technical-design decisions and explicit questions for human review.

## Expected Outputs

- `layers/domain-data-dictionary-capability-api-architecture/README.md`
- `layers/domain-data-dictionary-capability-api-architecture/artifacts/architecture.md`

## Preservation Constraints

- Capabilities must be derived from Model C responsibilities and logical lifecycle consequences, not PostgreSQL tables.
- No transport, UI, or client may mutate repository tables directly.
- Commands change authority-bearing state only through the Catalog Record Kernel commit boundary.
- Queries and diagnostics do not become writable authorities.
- Typed projections identify their governing definition revision and remain regenerable.
- Thin interfaces may own presentation and interaction state but not product validation, model lifecycle, projection, observation, comparison, or durable mutation logic.
- The architecture must not select endpoint paths, wire schemas, UI frameworks, caching products, OCL engines, or detailed query algorithms.
- Performance concerns must produce measured evidence before physical denormalization or a sibling realization is selected.
- The type-specific base/extension-table path remains an explicit alternative, not an untracked mutation of this branch.

## Validation Conditions

- [x] The architecture preserves all six Model C responsibilities.
- [x] The capability boundary hides `catalog_object`, `property_occurrence`, and `value_node` from ordinary clients.
- [x] Commands, queries, diagnostics, external effects, and derived projections have distinct authority consequences.
- [x] Human and machine clients consume the same capability meanings.
- [x] Thin user interfaces own no product business logic.
- [x] The first end-to-end test models the catalog, refines its designs, observes PostgreSQL, and compares intended with observed state.
- [x] Performance and developer comprehensibility are explicit validation concerns.
- [x] The typed-table alternative is preserved with an explicit reconsideration boundary.
- [x] A senior systems engineer confirms fidelity to the component and logical models for product-owner review; technical design remains blocked on the recorded human scope and performance inputs.
- [ ] The product owner confirms or corrects the provisional interpretation of "anthological" as "ontological."
- [ ] The product owner accepts the capability-API architecture for technical design.

## Descendant Impact

This is a new downstream branch and does not invalidate the existing PostgreSQL design or runtime. A later capability implementation will consume both this architecture branch and the PostgreSQL runtime. If capability design exposes a semantic defect in `CAT-CON` or `CAT-LOG`, correct the earliest owning layer and regenerate affected descendants in transform order.

## Retry Guidance

Return architectural boundary defects to this transform. Return missing capability responsibilities to Model C or the conceptual build design. Return authority, identity, projection, or lifecycle defects to `CAT-LOG`. Return ordinary query plans, indexes, materialization, caching, batching, or persistence tuning to downstream technical design or the PostgreSQL realization transform. Do not move product logic into a route or interface to avoid correcting its owner.
