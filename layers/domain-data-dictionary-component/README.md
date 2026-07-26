# Domain Data Dictionary Component

## Layer Status

- Status: draft
- Design status: Model C selected; downstream refinement in progress
- Effective: no
- Owning source layer: `data-modeling-definition`
- Owning transform: [`transform.md`](../data-modeling-definition/transforms/domain-data-dictionary-component/transform.md)
- Design artifact: [`component-design.md`](artifacts/component-design.md)

This layer is reserved for the design of the first deployable Domain Catalog component. The component will support DAMA-informed domain exploration and the refinement of particular business data models from conceptual through logical and physical forms, while retaining their realization, deployment, observation, and maintenance relationships as data-dictionary content.

The product owner selected Model C: one Domain Data Dictionary boundary with a Catalog Record Kernel and capability-oriented internal components. PostgreSQL is the required first physical deployment target, and the later API must expose the same application capabilities to machine and human-facing clients. The PostgreSQL version, repository schema, API protocol, implementation technology, and deployment topology remain downstream decisions.

The component requires explicit model-family identity and membership. Conceptual refinement places that responsibility in the Domain Catalog repository model under `DML-CON`, rather than promoting a catalog-specific construct into `DML-DEF` without evidence that it is generally required.
