# Component: GroundTruth Physical Projection Engine 📦

- **URI**: `component://groundtruth/physical`
- **Domain**: `groundtruth`
- **Lifecycle**: `ACTIVE`

## 1. Purpose and Responsibility
Deterministic physical DDL projection generators for PostgreSQL, Parquet, JSON Schema, and database migration scripts.

## 2. Exported Public Capabilities
These capabilities represent the public operational interface exposed by this bounded context:

- **[Generate Deterministic Physical DDL Projection](../capabilities/physical/generate-ddl-projection.md)** (`req://physical/generate-ddl-projection`)
  *Intent*: Generates standard, zero-drift PostgreSQL CREATE TABLE and ALTER TABLE DDL statements from DAMA logical schemas.
- **[req://physical/validate-schema-migration](../capabilities/physical/validate-schema-migration.md)** (`req://physical/validate-schema-migration`)

## 3. Required External Dependencies
Capabilities required by this component that must be satisfied by external components:

- **Target Component**: `component://groundtruth/logical`
  - **Required Capability**: `req://logical/define-entity-schema`
  - **Rationale**: Physical schemas are generated directly from DAMA logical entity definitions.

## 4. Boundary Invariants & Guardrails
Enforced by automated pre-commit AST analysis to prevent architectural leakage:

- ⚠️ **Deterministic DDL Projection Purity** (`constraint://groundtruth/deterministic-ddl-purity`)
  *Remediation Hint*: Ensure column order, constraint naming, and index definitions are deterministically sorted.
