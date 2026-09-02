# Capability: Trace Column-Level Data Provenance ⚡

- **URI**: `req://lineage/trace-column-provenance`
- **Bounded Context**: `lineage`
- **Lifecycle**: `ACTIVE`

## 1. Human Purpose & Intent
Traverses upstream sources and downstream transform targets for a specified logical attribute across the enterprise graph.

## 2. Operational Contract

### Preconditions (Required State Prior to Execution)
- **Target attribute URI must exist in logical data catalog**
  - Expression: `catalog.has_attribute(target_attribute_uri) == True`

### Postconditions (Guaranteed State Upon Success)
- **Returns directed acyclic graph of upstream sources and downstream projections**
  - Expression: `isinstance(lineage_graph, DirectedGraph)`

### State Transitions
*No explicit state transitions.*

## 3. Explicit Failure Modes & Error Recovery
Formal error branches that must be handled by autonomous implementations:

| Error Name | Domain Error Code | Trigger Condition | Recovery Action |
| :--- | :--- | :--- | :--- |
| **`UnknownAttributeError`** | `LINEAGE_001` | Attribute URI not found | Verify logical entity path and attribute name |

## 4. Governance, Decisions & Invariant Guardrails
### Governing Architectural Decisions (ADRs)
- **decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance** (`decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance`)
