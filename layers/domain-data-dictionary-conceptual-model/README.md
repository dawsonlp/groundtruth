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

PostgreSQL is the required downstream physical target. The later API must expose one capability boundary to machine and human-facing clients. Neither decision changes the conceptual meanings in this layer.

The next refinement is a logical data model that covers this conceptual model explicitly. Draft work may continue while the provisional placement, naming, and standards-alignment decisions remain unresolved, but affected descendants must be regenerated after an upstream correction.
