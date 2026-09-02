# Cross-Domain Traceability Matrix 🔗

> **Bidirectional traceability connecting Intent (`req://`), Decisions (`decision://`), Invariants (`constraint://`), Data (`data://`), and Code (`csi://`).**

---

| Capability | Bounded Context | Governing ADRs | Active Invariants | Satisfying Code Symbols (CodeMesh) |
| :--- | :--- | :--- | :--- | :--- |
| **[Generate Deterministic Physical DDL Projection](capabilities/physical/generate-ddl-projection.md)** | `physical` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/deterministic-ddl-purity` | *(Pending Implementation)* |
| **[Register Conceptual Business Term](capabilities/conceptual/register-business-term.md)** | `conceptual` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/mandatory-business-definition` | *(Pending Implementation)* |
| **[Trace Column-Level Data Provenance](capabilities/lineage/trace-column-provenance.md)** | `lineage` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | — | *(Pending Implementation)* |
| **[Verify Finite State Machine Transition](capabilities/logical/verify-state-transition.md)** | `logical` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/state-machine-validity` | *(Pending Implementation)* |
| **[Define Logical Entity Schema](capabilities/logical/define-entity-schema.md)** | `logical` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | — | *(Pending Implementation)* |
| **[Enforce Data Privacy Classification](capabilities/governance/enforce-privacy-tagging.md)** | `governance` | `decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance` | `constraint://groundtruth/mandatory-pii-classification` | *(Pending Implementation)* |
