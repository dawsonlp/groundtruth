# ADR 0002: Dual Declarative-Executable Constraint Representation 🏛️

- **URI**: `decision://arch/adr-0002-dual-declarative-executable-constraints`
- **Status**: `ACTIVE`

## 1. Context and Problem Statement
LLMs need high-level contextual summaries to understand design intent and avoid anti-patterns, while automated build systems and pre-commit pipelines need strict, deterministic, executable gates to block breaking changes. A purely text-based constraint system fails to stop invalid code, while purely programmatic code linters fail to guide LLM reasoning before generation.

## 2. Decision Outcome
Drivers

* Maximize AI agent code generation accuracy by injecting concise intent into prompt slices.
* Eliminate false positives/negatives at disk projection time by enforcing deterministic AST/structural validators.
* Provide actionable, automated remediation hints when constraints are violated.

## 3. Consequences

### Positive Consequences
- *(None recorded)*

### Negative Consequences / Trade-offs
- *(None recorded)*
