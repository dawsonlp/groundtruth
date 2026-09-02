# ADR 0003: First-Principles Capability Ontology Over Project Management Taxonomies 🏛️

- **URI**: `decision://arch/adr-0003-first-principles-capability-ontology`
- **Status**: `ACTIVE`

## 1. Context and Problem Statement
Requirement management tools historically classify business needs into administrative project management hierarchies (e.g. Jira's `Epic` $\to$ `Feature` $\to$ `User Story` $\to$ `Task` and story point estimates). 

While useful for human sprint planning and team velocity tracking, these taxonomies carry **zero semantic information** for:
1. **Compiling a `groundtruth` data model** (what entities exist, what fields they contain, what state machines govern them).
2. **Compiling a `codemesh` program graph** (what function signatures, parameter types, preconditions, postconditions, and error handlers are needed).
3. **Automated verification** (what invariant checks and test suites validate the system).

To enable seamless human elicitation and autonomous AI agent compilation, Northstar must model intent around **real information dependencies and formal operational contracts**.

---

## 2. Decision Outcome
We establish that `northstar` replaces project management taxonomies with a **first-principles capability ontology**:

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    CAPABILITY SPEC                     │
                               │                req://<domain>/<slug>                   │
                               └──────────────────────────┬─────────────────────────────┘
                                                          │
                   ┌──────────────────────────────────────┼──────────────────────────────────────┐
                   ▼                                      ▼                                      ▼
┌──────────────────────────────────────┐┌──────────────────────────────────────┐┌──────────────────────────────────────┐
│          OPERATED ENTITIES           ││         OPERATIONAL CONTRACT         ││            FAILURE MODES             │
│        (Links to GroundTruth)        ││        (Pre & Postconditions)        ││           (Error Handlers)           │
├──────────────────────────────────────┤├──────────────────────────────────────┤├──────────────────────────────────────┤
│ • creates: List[data://logical/...]  ││ • preconditions: List[str]           ││ • error_name: str                    │
│ • reads:   List[data://logical/...]  ││ • postconditions: List[str]          ││ • condition: str                     │
│ • mutates: List[data://logical/...]  ││ • state_transitions: List[Transition]││ • recovery_action: str               │
└──────────────────────────────────────┘└──────────────────────────────────────┘└──────────────────────────────────────┘
                   │                                                                             │
                   └──────────────────────────────────────┬──────────────────────────────────────┘
                                                          │
                                                          ▼
                                       ┌──────────────────────────────────────┐
                                       │        GOVERNANCE & INVARIANTS       │
                                       ├──────────────────────────────────────┤
                                       │ • governed_by: List[decision://...]  │
                                       │ • constrained_by: List[constraint://]│
                                       │ • policy_mandates: List[policy://...]│
                                       └──────────────────────────────────────┘
```

### Core Primitives Defined:

1. **`CapabilitySpec` (`req://<domain>/<slug>`)**:
   * **`intent`**: Clear natural-language business purpose.
   * **`operated_entities`**: Explicit references to `data://logical/...` entities (`creates`, `reads`, `mutates`).
   * **`preconditions`**: Explicit conditions that must hold true before invocation.
   * **`postconditions`**: Explicit state guarantees established upon successful execution.
   * **`failure_modes`**: Enumerated domain errors, conditions, and required recovery behaviors.
   * **`governed_by`**: Governing architectural decisions (`decision://...`).
   * **`invariants`**: Executable guardrails (`constraint://...`).

2. **`DecisionSpec` (`decision://<domain>/<slug>`)**:
   * Structural architectural patterns (context, chosen pattern, positive/negative consequences, alternatives).

3. **`InvariantSpec` (`constraint://<domain>/<slug>`)**:
   * Executable rules (purity, boundary violations, data range assertions, state transition graphs).

---

## 3. Consequences

### Positive Consequences
- *(None recorded)*

### Negative Consequences / Trade-offs
- *(None recorded)*
