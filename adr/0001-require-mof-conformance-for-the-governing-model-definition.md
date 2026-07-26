# Domain Catalog ADR 0001: Require MOF Conformance for the Governing Model Definition

- Status: Accepted
- Date: 2026-07-25
- Decision owners: Product owner and project architect
- Follow-up decision required: Determine whether CMOF is the governing model definition

## Context

The product conception requires a model that defines how other models are constructed. That model must describe itself, provide explicit conformance rules, and support more specialized definitions, beginning with a DAMA-aligned data-modeling definition.

Calling this model simply "the metamodel" is imprecise. A model is meta only relative to a named model whose valid form it defines. Without both ends of that relationship, the term hides rather than explains the governing relationship.

The project could invent an unconstrained model-definition language, adopt the full UML metamodel, or anchor its governing definition in an existing metamodeling standard. The OMG Meta Object Facility (MOF) exists specifically to define metamodels. MOF supports self-description and defines Essential MOF (EMOF) and Complete MOF (CMOF) as its two conformance points.

This decision must establish the external constraint without prematurely deciding whether CMOF itself is sufficient for the project.

## Decision

The model that directly governs construction of the project's specialized definition models must conform to the OMG Meta Object Facility (MOF), version 2.5.1.

The initial specialized definition will be the DAMA-aligned data-modeling definition. The governing relationships will be stated explicitly:

```text
selected MOF-conforming governing model definition
    governs the valid form of
DAMA-aligned data-modeling definition
    governs the valid form of
a particular domain data model
```

If CMOF is selected as the governing model definition, it occupies the first position directly and conforms to itself. If a project-specific governing model is selected instead, that model must identify and conform to the chosen MOF conformance point.

Project documentation must not use "the metamodel" as an unanchored proper name. It should name the governing model, the governed model, and their conformance relationship.

This ADR decides model conformance. It does not claim that a future software implementation is an OMG-certified or fully conforming MOF implementation.

## Decision Drivers

- Anchor model validity in a named, externally defined standard.
- Preserve the requirement that the governing model can be expressed as a valid model.
- Avoid inventing a new meta-metamodel without demonstrated need.
- Support multiple adjacent model-definition levels without assigning them fixed universal layer numbers.
- Keep DAMA terminology and data-modeling semantics outside the general model-definition foundation.
- Make conformance distinct from transformation, generation, and realization.

## Alternatives Considered

### Unconstrained project-specific definition language

Rejected because the project would have to define and verify type, property, relationship, containment, constraint, reflection, and self-description semantics that MOF already addresses.

### Full UML metamodel

Rejected as the governing foundation because UML contains software- and systems-modeling semantics beyond the general model-definition role. UML remains relevant prior art and a major example of a MOF-defined metamodel.

### MOF-conforming governing model definition

Selected because it supplies a precise external conformance anchor while leaving the project free to determine whether CMOF, EMOF, or a separate MOF-conforming model provides the appropriate immediate constraint.

## Consequences

Positive consequences:

- Every specialized definition can identify the model that governs its valid form.
- The project can reuse established concepts for classes, datatypes, properties, associations, packages, constraints, identifiers, and reflection.
- Self-description has a defined precedent rather than being a project-specific assertion.
- The DAMA-aligned definition can focus on data-modeling semantics instead of inventing its own modeling foundation.

Negative consequences:

- Model definitions will be constrained by MOF's class-, property-, association-, and package-oriented formalism.
- The project acquires a dependency on a substantial external standard.
- MOF conformance does not provide DAMA semantics, catalog authority, provenance, realization history, or transformation behavior; those still require explicit project models.
- A precise conformance point and means of demonstrating conformance remain unresolved.

## Not Decided Here

- Whether CMOF 2.5.1 is used directly as the governing model definition.
- Whether EMOF is sufficient.
- Whether a distinct project model conforming to EMOF or CMOF is necessary.
- Whether MOF's XMI representation or OCL constraints become implementation requirements.
- How the product stores, evaluates, or reports conformance.
- How MOF version changes would be adopted.

## Required Follow-Up Decision: Is CMOF the Governing Model Definition?

The next ADR must compare using CMOF directly with using EMOF or a separate MOF-conforming governing model. At minimum, it must test whether CMOF can describe without semantic distortion:

- model identity and boundaries;
- specialized model-element types;
- binary and n-ary domain relationships;
- separately scoped metamodel, definition-model, and subject-model constraints;
- composition and extension of definition models;
- correspondence and realization relationships across models; and
- stable identity and provenance across refinement.

If CMOF cannot express one of these directly, the decision must distinguish a genuine expressiveness gap from a concept that properly belongs in a MOF-conforming project definition rather than in CMOF itself.

## References

- [OMG MOF 2.5.1 specification page](https://www.omg.org/spec/MOF/2.5.1)
- [OMG MOF 2.5.1 normative PDF](https://www.omg.org/spec/MOF/2.5.1/PDF)
- [OMG MOF machine-readable resources](https://www.omg.org/spec/MOF/machine-readable)
