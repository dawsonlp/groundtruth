# ADR 0001: First-Principles Information Dependencies and Abstraction Focus for Ontology Design 🏛️

- **URI**: `decision://arch/adr-0001-first-principles-information-dependencies-for-ontology-design`
- **Status**: `ACTIVE`

## 1. Context and Problem Statement
Software engineering tooling and methodologies are encumbered by historical taxonomies designed around legacy human operational and physical constraints:
* **Project Management Taxonomies**: Agile/Jira hierarchies (`Epic` $\to$ `Feature` $\to$ `Story` $\to$ `Task`) were invented for human sprint capacity planning, team velocity estimation, and task assignment. They carry **zero mathematical or semantic value** for compiling software or validating data integrity.
* **Physical Text & Filesystem Taxonomies**: Source files, line offsets, and directory groupings were designed around operating system file abstractions and compiler memory limits in the 1970s.
* **Ad-hoc Database Artifacts**: Raw SQL DDL tables and migration scripts conflate persistent storage mechanics with high-level conceptual business semantics.

When building an **AI-Native Software Architecture**—where autonomous AI agents and human architects collaborate to design, synthesize, verify, and maintain complex systems—these inherited ontologies introduce massive semantic loss, impedance mismatches, and prompt bloat.

An AI agent tasked with building or refactoring a capability cannot extract formal computation or data requirements from "3 story points on an Epic." It requires **exact, typed information dependencies**.

---

## 2. Decision Outcome
: The First-Principles Ontology Principle

Across all projects under the Tripartite Federation (`codemesh`, `groundtruth`, `northstar`), every ontology, domain model, and abstraction layer must be designed strictly according to **first-principles information dependencies**:

```
                       ┌──────────────────────────────────────────────┐
                       │          HUMAN INTENT ELICITATION            │
                       │ (What the human architect/user needs to do)  │
                       └──────────────────────┬───────────────────────┘
                                              │
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │          FIRST-PRINCIPLES ONTOLOGY           │
                       │       (Real Information Dependencies)        │
                       └──────────────┬────────────────┬──────────────┘
                                      │                │
            ┌─────────────────────────┴────┐      ┌────┴─────────────────────────┐
            ▼                              ▼      ▼                              ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐
│          NORTHSTAR           │  │         GROUNDTRUTH          │  │           CODEMESH           │
│      (Intent & Policy)       │  │        (Data & State)        │  │        (Computation)         │
│                              │  │                              │  │                              │
│ • CapabilitySpec             │  │ • Conceptual Models          │  │ • Canonical Symbol IDs (csi) │
│ • Pre/Postconditions         │  │ • Logical Entities & Attrs   │  │ • Typed Symbol Contracts     │
│ • Failure Modes & Errors     │  │ • State Transition Matrices  │  │ • AST Implementations        │
│ • Architectural Rationale    │  │ • Physical Storage DDL/Wire  │  │ • Relational Call Graphs     │
│ • Executable Guardrails      │  │ • Privacy Classifications    │  │ • Zero-Diff Projections      │
└──────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘
```

### 2.1 The Core Information Primitives

Every system capability is decomposed into its fundamental information-theoretic components:

1. **The Business Goal / Capability (`Intent`)**:
   * *What business outcome is being accomplished?*
2. **The Operated Entities (`Data`)**:
   * *What business nouns are created, read, mutated, or deleted?*
3. **The Operational Contract (`Preconditions & Postconditions`)**:
   * *What state must be guaranteed before execution?*
   * *What state is guaranteed upon successful execution?*
4. **The Failure Modes (`Error Contracts`)**:
   * *What alternative outcomes and domain errors can occur, and under what conditions?*
5. **The Architectural Decisions (`ADRs & Rationale`)**:
   * *Which structural patterns and technical trade-offs were selected to implement this capability, and why?*
6. **The Invariant Guardrails (`Executable Constraints & Policies`)**:
   * *What rules (purity, architectural boundaries, data ranges, security policies) must never be breached?*

---

## 3. Consequences

### Positive Consequences
- *(None recorded)*

### Negative Consequences / Trade-offs
- *(None recorded)*
