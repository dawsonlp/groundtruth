# Component: GroundTruth Lineage & Provenance Tracker 📦

- **URI**: `component://groundtruth/lineage`
- **Domain**: `groundtruth`
- **Lifecycle**: `ACTIVE`

## 1. Purpose and Responsibility
Column-level data provenance graphs, pipeline transform tracking, and audit lineage traversal.

## 2. Exported Public Capabilities
These capabilities represent the public operational interface exposed by this bounded context:

- **[Trace Column-Level Data Provenance](../capabilities/lineage/trace-column-provenance.md)** (`req://lineage/trace-column-provenance`)
  *Intent*: Traverses upstream sources and downstream transform targets for a specified logical attribute across the enterprise graph.
- **[req://lineage/register-transform-pipeline](../capabilities/lineage/register-transform-pipeline.md)** (`req://lineage/register-transform-pipeline`)

## 3. Required External Dependencies
Capabilities required by this component that must be satisfied by external components:

- **Target Component**: `component://groundtruth/logical`
  - **Required Capability**: `req://logical/define-entity-schema`
  - **Rationale**: Lineage vertices bind to logical entity attributes.

## 4. Boundary Invariants & Guardrails
Enforced by automated pre-commit AST analysis to prevent architectural leakage:

*No specific boundary invariants.*
