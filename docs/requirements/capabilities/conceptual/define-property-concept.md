# Capability: Define Reusable Property Concept ⚡

- **URI**: `req://conceptual/define-property-concept`
- **Bounded Context**: `conceptual`
- **Lifecycle**: `ACTIVE`

## 1. Human Purpose & Intent
Defines a reusable conceptual property concept (e.g. Designation, Definition, OccurrenceTime, LifecycleState, Classification) applied across object classes to form DataElementConcepts.

## 2. Operational Contract

### Preconditions (Required State Prior to Execution)
- **Concept name must be a recognized conceptual property category**
  - Expression: `concept.name in ['Designation', 'Definition', 'Purpose', 'Scope', 'Classification', 'Canonical Reference', 'Version Designation', 'Authority', 'Lifecycle State', 'Evidence Fingerprint', 'Occurrence Time', 'Rationale', 'Native Language', 'Expression Text', 'Lexical Representation', 'Product Designation', 'Inventory Exception']`
- **Conceptual domain must be declared**
  - Expression: `len(concept.domain.strip()) > 0`

### Postconditions (Guaranteed State Upon Success)
- **Property concept is registered under data://conceptual/properties/<slug>**
  - Expression: `catalog.has_property_concept(concept.slug) == True`

### State Transitions
*No explicit state transitions.*

## 3. Explicit Failure Modes & Error Recovery
Formal error branches that must be handled by autonomous implementations:

| Error Name | Domain Error Code | Trigger Condition | Recovery Action |
| :--- | :--- | :--- | :--- |
| **`InvalidPropertyConceptError`** | `CONCEPTUAL_002` | Property concept category is not recognized in governing definition | Select an approved property concept category or propose an extension to DML-CON |

## 4. Governance, Decisions & Invariant Guardrails
### Governing Architectural Decisions (ADRs)
- **decision://groundtruth/adr-0001-require-mof-conformance-for-the-governing-model-definition** (`decision://groundtruth/adr-0001-require-mof-conformance-for-the-governing-model-definition`)
- **decision://groundtruth/adr-0002-dama-aligned-4-tier-data-modeling-architecture** (`decision://groundtruth/adr-0002-dama-aligned-4-tier-data-modeling-architecture`)
### Active Invariant Guardrails
- ⚠️ **Mandatory Plain-Language Business Definition** (`constraint://groundtruth/mandatory-business-definition`)
  *Remediation*: Add a descriptive business definition explaining the real-world business meaning of this term.
