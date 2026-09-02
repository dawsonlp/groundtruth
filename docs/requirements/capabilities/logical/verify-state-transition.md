# Capability: Verify Finite State Machine Transition ⚡

- **URI**: `req://logical/verify-state-transition`
- **Bounded Context**: `logical`
- **Lifecycle**: `ACTIVE`

## 1. Human Purpose & Intent
Verifies that a proposed entity state mutation obeys the finite state machine matrix declared for that logical entity.

## 2. Operational Contract

### Preconditions (Required State Prior to Execution)
- **Entity must declare a state machine on the target attribute**
  - Expression: `entity.has_state_machine(attribute) == True`
- **Current state must be in the entity's declared legal state list**
  - Expression: `from_state in entity.state_machine.states`

### Postconditions (Guaranteed State Upon Success)
- **Returns True if transition (from_state -> to_state) is legal**
  - Expression: `(from_state, to_state) in entity.state_machine.legal_transitions`

### State Transitions
*No explicit state transitions.*

## 3. Explicit Failure Modes & Error Recovery
Formal error branches that must be handled by autonomous implementations:

| Error Name | Domain Error Code | Trigger Condition | Recovery Action |
| :--- | :--- | :--- | :--- |
| **`IllegalStateTransitionError`** | `LOGICAL_003` | Attempted transition is not present in legal_transitions matrix | Reject state change and return legal next states |

## 4. Governance, Decisions & Invariant Guardrails
### Governing Architectural Decisions (ADRs)
- **decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance** (`decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance`)
### Active Invariant Guardrails
- ⚠️ **Finite State Machine Mutation Validity** (`constraint://groundtruth/state-machine-validity`)
  *Remediation*: Verify that transition is declared in entity state machine matrix before calling state update.
