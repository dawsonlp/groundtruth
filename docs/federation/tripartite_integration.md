# GroundTruth Tripartite Federation Integration

This guide specifies how **GroundTruth** (`data://`) interacts with **CodeMesh** (`csi://`) and **Northstar** (`req://`, `decision://`, `constraint://`) in the Tripartite Semantic Federation.

---

## 1. Cross-Domain Relational Grammar

GroundTruth provides the information semantics connected via typed relational edges:

```
Code Symbol (csi://)      ──[ CREATES ]───────────>  Logical Entity (data://logical/...)
Code Symbol (csi://)      ──[ READS ]─────────────>  Logical / Physical Entity (data://...)
Code Symbol (csi://)      ──[ WRITES ]────────────>  Physical Storage (data://physical/...)
Code Symbol (csi://)      ──[ VALIDATES ]─────────>  Logical Attribute (data://logical/...#attr)
Code Symbol (csi://)      ──[ SERIALIZES ]────────>  Physical Wire Schema (data://physical/...)
Code Symbol (csi://)      ──[ REPRESENTS ]────────>  Logical Entity (data://logical/...)
Logical Entity (data://)  ──[ CONSTRAINED_BY ]────>  Compliance Policy (policy://...)
Physical Object (data://) ──[ REALIZES ]──────────>  Logical Entity (data://logical/...)
```

---

## 2. Interaction Lifecycle

1. **Schema Authoring & Evolution**: An architect or data engineer updates a Logical entity in GroundTruth (e.g. modifying `Order.total_amount`).
2. **Reverse Impact Analysis**: GroundTruth queries CodeMesh's relational graph:
   * *"Which code symbols (`csi://...`) read or write `Order.total_amount`?"*
3. **Agent Blast-Radius Notification**: CodeMesh generates prompt context slices for only the impacted service methods, allowing agents to update consumers safely.
4. **Pre-Commit Invariant Enforcement**: CodeMesh checks proposed code against GroundTruth's range constraints and state machines before disk projection.
5. **Governance Compliance**: Northstar policies (e.g., PCI-DSS, GDPR) tag GroundTruth data entities (`RESTRICTED_PII`), blocking code that attempts to log sensitive attributes in clear text.
