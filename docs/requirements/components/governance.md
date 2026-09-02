# Component: GroundTruth Governance & Privacy Authority 📦

- **URI**: `component://groundtruth/governance`
- **Domain**: `groundtruth`
- **Lifecycle**: `ACTIVE`

## 1. Purpose and Responsibility
Data classification enforcement, PII/GDPR privacy tags, retention policies, and executable data quality validation rules.

## 2. Exported Public Capabilities
These capabilities represent the public operational interface exposed by this bounded context:

- **[Enforce Data Privacy Classification](../capabilities/governance/enforce-privacy-tagging.md)** (`req://governance/enforce-privacy-tagging`)
  *Intent*: Inspects and enforces privacy classification metadata (PII, Financial, Internal, Public) on all logical entity attributes.
- **[req://governance/evaluate-data-quality-rules](../capabilities/governance/evaluate-data-quality-rules.md)** (`req://governance/evaluate-data-quality-rules`)

## 3. Required External Dependencies
Capabilities required by this component that must be satisfied by external components:

- **Target Component**: `component://groundtruth/logical`
  - **Required Capability**: `req://logical/define-entity-schema`
  - **Rationale**: Privacy classifications attach directly to logical entity attributes.

## 4. Boundary Invariants & Guardrails
Enforced by automated pre-commit AST analysis to prevent architectural leakage:

- ⚠️ **Mandatory PII Classification on Customer Entities** (`constraint://groundtruth/mandatory-pii-classification`)
  *Remediation Hint*: Add privacy classification tag (e.g., tags=['PII', 'CONFIDENTIAL']) to the attribute definition.
