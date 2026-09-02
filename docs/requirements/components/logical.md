# Component: GroundTruth Logical Data Model 📦

- **URI**: `component://groundtruth/logical`
- **Domain**: `groundtruth`
- **Lifecycle**: `ACTIVE`

## 1. Purpose and Responsibility
DAMA-compliant logical entity schemas, typed attribute definitions, primary/foreign key relations, and finite state transition machines.

## 2. Exported Public Capabilities
These capabilities represent the public operational interface exposed by this bounded context:

- **[Define Logical Entity Schema](../capabilities/logical/define-entity-schema.md)** (`req://logical/define-entity-schema`)
  *Intent*: Defines a DAMA-compliant logical entity with typed attributes, nullability constraints, primary key indicators, and conceptual mappings.
- **[Verify Finite State Machine Transition](../capabilities/logical/verify-state-transition.md)** (`req://logical/verify-state-transition`)
  *Intent*: Verifies that a proposed entity state mutation obeys the finite state machine matrix declared for that logical entity.
- **[req://logical/validate-foreign-key-integrity](../capabilities/logical/validate-foreign-key-integrity.md)** (`req://logical/validate-foreign-key-integrity`)

## 3. Required External Dependencies
Capabilities required by this component that must be satisfied by external components:

- **Target Component**: `component://groundtruth/conceptual`
  - **Required Capability**: `req://conceptual/register-business-term`
  - **Rationale**: Every logical entity must link to a governing conceptual business term.

## 4. Boundary Invariants & Guardrails
Enforced by automated pre-commit AST analysis to prevent architectural leakage:

- ⚠️ **Finite State Machine Mutation Validity** (`constraint://groundtruth/state-machine-validity`)
  *Remediation Hint*: Verify that transition is declared in entity state machine matrix before calling state update.
