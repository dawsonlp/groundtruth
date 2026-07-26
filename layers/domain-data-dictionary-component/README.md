# Domain Data Dictionary Component

## Layer Status

- Status: draft
- Design status: complete; review pending
- Effective: no
- Owning source layer: `data-modeling-definition`
- Owning transform: [`transform.md`](../data-modeling-definition/transforms/domain-data-dictionary-component/transform.md)
- Design artifact: [`component-design.md`](artifacts/component-design.md)

This layer is reserved for the design of the first deployable Domain Catalog component. The component will support DAMA-informed domain exploration and the refinement of particular business data models from conceptual through logical and physical forms, while retaining their realization, deployment, observation, and maintenance relationships as data-dictionary content.

The draft design selects one Domain Data Dictionary boundary with a Catalog Record Kernel and capability-oriented internal components. It deliberately defers the persistence schema, implementation technology, deployment topology, first physical target, and other architecture decisions. Design execution exposed that `DML-DEF` names `BDM-FAMILY` without structurally defining family identity or membership. That gap prevents acceptance but does not block further draft architecture or implementation exploration; any descendant must carry the gap and its provisional assumption explicitly, and must be regenerated after the upstream correction.
