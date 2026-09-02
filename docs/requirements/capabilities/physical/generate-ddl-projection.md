# Capability: Generate Deterministic Physical DDL Projection ⚡

- **URI**: `req://physical/generate-ddl-projection`
- **Bounded Context**: `physical`
- **Lifecycle**: `ACTIVE`

## 1. Human Purpose & Intent
Generates standard, zero-drift PostgreSQL CREATE TABLE and ALTER TABLE DDL statements from DAMA logical schemas.

## 2. Operational Contract

### Preconditions (Required State Prior to Execution)
- **Target logical entity must be validated and active**
  - Expression: `entity.lifecycle == 'ACTIVE'`

### Postconditions (Guaranteed State Upon Success)
- **Returns deterministic, idempotent DDL string with primary keys, foreign keys, and indexes**
  - Expression: `len(ddl_output.strip()) > 0`

### State Transitions
*No explicit state transitions.*

## 3. Explicit Failure Modes & Error Recovery
Formal error branches that must be handled by autonomous implementations:

| Error Name | Domain Error Code | Trigger Condition | Recovery Action |
| :--- | :--- | :--- | :--- |
| **`UnsupportedTypeMappingError`** | `PHYSICAL_001` | Logical attribute data type cannot be mapped to PostgreSQL dialect | Declare explicit physical type override |

## 4. Governance, Decisions & Invariant Guardrails
### Governing Architectural Decisions (ADRs)
- **decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance** (`decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance`)
### Active Invariant Guardrails
- ⚠️ **Deterministic DDL Projection Purity** (`constraint://groundtruth/deterministic-ddl-purity`)
  *Remediation*: Ensure column order, constraint naming, and index definitions are deterministically sorted.
