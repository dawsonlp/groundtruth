# Capability: Enforce Data Privacy Classification ⚡

- **URI**: `req://governance/enforce-privacy-tagging`
- **Bounded Context**: `governance`
- **Lifecycle**: `ACTIVE`

## 1. Human Purpose & Intent
Inspects and enforces privacy classification metadata (PII, Financial, Internal, Public) on all logical entity attributes.

## 2. Operational Contract

### Preconditions (Required State Prior to Execution)
- **Logical entity must declare classification on all sensitive attributes**
  - Expression: `all(has_classification(a) for a in entity.attributes if a.is_sensitive)`

### Postconditions (Guaranteed State Upon Success)
- **Generates compliance audit certificate and masking rules**
  - Expression: `certificate.is_valid == True`

### State Transitions
*No explicit state transitions.*

## 3. Explicit Failure Modes & Error Recovery
Formal error branches that must be handled by autonomous implementations:

| Error Name | Domain Error Code | Trigger Condition | Recovery Action |
| :--- | :--- | :--- | :--- |
| **`UnclassifiedSensitiveDataError`** | `GOVERNANCE_001` | Sensitive attribute lacks classification tag | Prompt data steward for PII/GDPR classification level |

## 4. Governance, Decisions & Invariant Guardrails
### Governing Architectural Decisions (ADRs)
- **decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance** (`decision://groundtruth/adr-0001-mof-and-dama-meta-model-conformance`)
### Active Invariant Guardrails
- ⚠️ **Mandatory PII Classification on Customer Entities** (`constraint://groundtruth/mandatory-pii-classification`)
  *Remediation*: Add privacy classification tag (e.g., tags=['PII', 'CONFIDENTIAL']) to the attribute definition.
