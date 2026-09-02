# Capability: Define Logical Entity Schema ⚡

- **URI**: `req://logical/define-entity-schema`
- **Bounded Context**: `logical`
- **Lifecycle**: `ACTIVE`

## 1. Human Purpose & Intent
Defines a DAMA-compliant logical entity with typed attributes, nullability constraints, primary key indicators, and conceptual mappings.

## 2. Operational Contract

### Preconditions (Required State Prior to Execution)
- **Entity must link to an existing conceptual term URI**
  - Expression: `catalog.has_node(entity.conceptual_term_ref) == True`
- **Entity must declare at least one primary key attribute**
  - Expression: `any(attr.is_primary_key for attr in entity.attributes)`

### Postconditions (Guaranteed State Upon Success)
- **Logical entity is registered under data://logical/<domain>/<EntityName>**
  - Expression: `catalog.has_logical_entity(entity.uri) == True`

### State Transitions
*No explicit state transitions.*

## 3. Explicit Failure Modes & Error Recovery
Formal error branches that must be handled by autonomous implementations:

| Error Name | Domain Error Code | Trigger Condition | Recovery Action |
| :--- | :--- | :--- | :--- |
| **`MissingPrimaryKeyError`** | `LOGICAL_001` | Entity schema defined without a primary key | Declare primary key attribute or surrogate ID |
| **`UnmappedConceptualTermError`** | `LOGICAL_002` | Conceptual term reference does not exist in conceptual catalog | Register conceptual term before defining logical entity |

## 4. Governance, Decisions & Invariant Guardrails
### Governing Architectural Decisions (ADRs)
- **decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance** (`decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance`)
