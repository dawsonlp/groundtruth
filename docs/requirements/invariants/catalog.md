# Executable Invariants & Guardrails Catalog 🛡️

> **Machine-executable rules enforced prior to code commit to prevent architectural drift, security violations, and illegal state transitions.**

---

| Invariant Title | URI | Rule Type | Target Scope | Remediation Hint |
| :--- | :--- | :--- | :--- | :--- |
| **Mandatory PII Classification on Customer Entities** | `constraint://groundtruth/mandatory-pii-classification` | `DATA_INTEGRITY` | `data://logical/customers/*` | Add privacy classification tag (e.g., tags=['PII', 'CONFIDENTIAL']) to the attribute definition. |
| **MOF Meta-Level Separation** | `constraint://groundtruth/mof-meta-level-separation` | `ARCHITECTURAL_BOUNDARY` | `data://conceptual/*, data://logical/*` | Separate operational runtime instance data (M0) from domain model definitions (M1) and metamodel rules (M2). |
| **Deterministic DDL Projection Purity** | `constraint://groundtruth/deterministic-ddl-purity` | `PURITY_BOUND` | `csi://groundtruth/physical/*` | Ensure column order, constraint naming, and index definitions are deterministically sorted. |
| **Finite State Machine Mutation Validity** | `constraint://groundtruth/state-machine-validity` | `STATE_MACHINE` | `data://logical/*/status` | Verify that transition is declared in entity state machine matrix before calling state update. |
| **Mandatory Plain-Language Business Definition** | `constraint://groundtruth/mandatory-business-definition` | `DATA_INTEGRITY` | `data://conceptual/*` | Add a descriptive business definition explaining the real-world business meaning of this term. |
