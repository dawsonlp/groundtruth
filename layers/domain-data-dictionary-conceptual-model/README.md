# Domain Data Dictionary Conceptual Model

## Layer Status

- Status: draft
- Effective: no
- Source layer: `domain-data-dictionary-component`
- Source revision: `5a0993d`
- Owning transform: [`transform.md`](../domain-data-dictionary-component/transforms/domain-data-dictionary-conceptual-model/transform.md)
- Build direction: [`build-design.md`](artifacts/build-design.md)
- Conceptual model: [`conceptual-data-model.md`](artifacts/conceptual-data-model.md)

This layer defines the business concepts the Domain Data Dictionary must retain. It is the provisional `CAT-CON` member of `CAT-FAMILY` and the source for a later `CAT-LOG` refinement. It contains no repository schema or API contract.

PostgreSQL is the required downstream repository realization. Its migration SQL will be the executable physical authority, accompanied by derived traceability and deployed-inventory evidence rather than a separately approved physical design. The later API must expose one capability boundary to machine and human-facing clients. Neither decision changes the conceptual meanings in this layer.

The draft logical refinement is [domain-data-dictionary-logical-model](../domain-data-dictionary-logical-model/README.md), produced by its source-colocated [transform](transforms/domain-data-dictionary-logical-model/transform.md). Draft work may continue while provisional placement, naming, and standards-alignment decisions remain unresolved, but affected descendants must be regenerated after an upstream correction.
