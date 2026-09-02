# Component: GroundTruth Conceptual Catalog 📦

- **URI**: `component://groundtruth/conceptual`
- **Domain**: `groundtruth`
- **Lifecycle**: `ACTIVE`

## 1. Purpose and Responsibility
Enterprise business glossary, conceptual ontology, ObjectClasses, PropertyConcepts, and DataElementConcept semantics.

## 2. Exported Public Capabilities
These capabilities represent the public operational interface exposed by this bounded context:

- **[Register Conceptual Business Term](../capabilities/conceptual/register-business-term.md)** (`req://conceptual/register-business-term`)
  *Intent*: Authoritatively registers an enterprise business term with formal definitions, business context, synonyms, and governance stewardship.
- **[Define Reusable Property Concept](../capabilities/conceptual/define-property-concept.md)** (`req://conceptual/define-property-concept`)
  *Intent*: Defines a reusable conceptual property concept (e.g. Designation, Definition, OccurrenceTime, LifecycleState, Classification) applied across object classes to form DataElementConcepts.
- **[req://conceptual/map-term-to-logical-entity](../capabilities/conceptual/map-term-to-logical-entity.md)** (`req://conceptual/map-term-to-logical-entity`)

## 3. Required External Dependencies
Capabilities required by this component that must be satisfied by external components:

*No external dependencies.*

## 4. Boundary Invariants & Guardrails
Enforced by automated pre-commit AST analysis to prevent architectural leakage:

- ⚠️ **Mandatory Plain-Language Business Definition** (`constraint://groundtruth/mandatory-business-definition`)
  *Remediation Hint*: Add a descriptive business definition explaining the real-world business meaning of this term.
