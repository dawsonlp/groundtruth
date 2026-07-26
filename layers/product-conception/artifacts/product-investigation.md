# Domain Catalog Product Investigation

## Document Status

This document records an initial product hypothesis. It is not an approved requirements specification or an architecture.

- Status: draft
- Product owner approval: pending
- Architecture decisions: deferred

## 1. Purpose

Investigate a domain catalog that keeps business meaning, structured models, and generated implementation artifacts aligned.

The proposed product has one coherent responsibility: maintain an authoritative description of a domain and the explicit derivations that connect that description to implementation artifacts.

It would support three activities within that boundary:

1. Model domain meaning and structure.
2. Validate and transform models into selected implementation artifacts.
3. Govern access, ownership, lifecycle, and traceability within the catalog.

Deployment and runtime operation of generated artifacts are outside this boundary.

## 2. Problem

Organizations commonly maintain business concepts, logical data models, and implementation schemas as separate artifacts. Their meaning and constraints drift because the correspondence between them is incomplete, implicit, or manually maintained.

A useful product must therefore preserve:

- the meaning of domain concepts;
- the rules and constraints that make a model valid;
- explicit correspondence between conceptual, logical, and physical representations;
- the derivation of generated artifacts; and
- the ownership and history needed to govern change.

## 3. Product Hypothesis

A governed catalog can reduce model drift by making domain elements, constraints, mappings, and transformation provenance first-class data.

The catalog would be authoritative for design intent. Generated artifacts would be reproducible outputs of that intent, not independent sources of truth. Any future support for importing or reconciling externally changed artifacts is a separate capability.

The initial proof should cover one end-to-end modeling flow and one implementation target. Supporting many targets, arbitrary subsystem behavior, or complete enterprise governance is not required to test the hypothesis.

## 4. Governing Principles

### 4.1 Semantic fidelity

Implementation details must not silently replace or distort domain meaning.

### 4.2 Explicit rules

Material constraints, mappings, and transformations must be represented in the catalog rather than existing only in generated output or application code.

### 4.3 Traceable derivation

Each generated artifact must be traceable to the model elements, rules, transformation version, and catalog revision that produced it.

### 4.4 Clear authority

The catalog is authoritative for design intent. The product must identify derived data and must not imply bidirectional synchronization unless that behavior is explicitly defined.

### 4.5 Separation of concerns

The product must distinguish domain semantics, representation decisions, target-specific mappings, generated artifacts, and operational governance.

### 4.6 Least necessary complexity

The core model should contain only concepts required by the first validated workflows. New abstractions should be introduced in response to demonstrated needs.

### 4.7 Isolation by default

Content from one workspace must not be visible or mutable from another workspace unless sharing is explicitly supported and authorized.

## 5. Product Vocabulary

The following terms remove overlap from the initial proposal.

### 5.1 Catalog item (`Thing`)

A catalog item is any independently identified object managed by the catalog. All catalog items share metadata, not necessarily behavior:

- stable identifier;
- type;
- provenance;
- owner;
- creation and modification records;
- lifecycle state;
- revision information; and
- annotations.

`Thing` is a convenient name for this common contract, not a claim that all domain concepts have the same semantics or implementation.

### 5.2 Domain

A bounded subject area whose meaning and structure are being modeled.

### 5.3 Model element

A meaningful part of a domain model. Initial model-element types are:

- Concept: a business idea whose meaning is independent of a particular implementation.
- Entity: an identifiable subject represented in a structured model.
- Attribute: a characteristic of a concept or entity.
- Relationship: a typed association between model elements.
- Constraint: a rule that determines model or data validity.
- Identifier: a rule for distinguishing instances of an entity.
- Value domain: the permitted values and associated meaning for an attribute.

The distinction between a Concept and an Entity must be demonstrated by the initial use case before both become mandatory core types.

### 5.4 Representation

An expression of a model element at one of three levels:

- Conceptual: business meaning and domain language.
- Logical: structured entities, attributes, relationships, and constraints without target-specific storage choices.
- Physical: a target-specific realization.

A representation is not merely a label. Its correspondence to other representations must be explicit.

### 5.5 Mapping and derivation

A mapping records correspondence between representations. A derivation records how a source representation and transformation rule produced a target representation or artifact.

Mappings may be one-to-one, one-to-many, or many-to-many. Lossy or intentionally absent mappings must be identifiable rather than hidden.

### 5.6 Generated artifact

A reproducible output, such as a schema definition or implementation script, produced for a selected target from a validated model revision.

## 6. Operational Vocabulary

Operational concepts are independent dimensions and must not be used interchangeably.

### 6.1 Workspace

The initial ownership and access boundary for catalog content. Whether a workspace later maps to a customer tenant, organization, or project is a deployment decision.

### 6.2 Collection

An organizational grouping within a workspace. A collection is not an independent security boundary unless an access policy explicitly makes it one.

### 6.3 Perspective

A curated, non-authoritative view of existing catalog items for a particular audience or task. A perspective does not duplicate or fork the underlying model.

Branching and independently editable variants, if needed, require separate versioning semantics and are deferred.

### 6.4 Lifecycle state

The governance status of a catalog item or model revision, such as draft, reviewed, approved, or published.

### 6.5 Environment

A deployment or execution context, such as development, QA, UAT, or production. Environment is not a synonym for lifecycle state. Environment-specific deployment management is outside the initial product boundary.

### 6.6 Role and access policy

A role groups permitted actions. An access policy applies those permissions within a workspace or explicitly scoped collection.

## 7. Users and Outcomes

The investigation identifies several users but has not selected the primary initial user.

- Domain designers need to describe domain meaning without prematurely choosing storage mechanics.
- Data modelers need to refine domain meaning into a precise logical model.
- Platform engineers need reproducible implementation artifacts with clear provenance.
- Governance stakeholders need ownership, auditability, and controlled publication.
- Workspace administrators need enforceable access boundaries.

The initial product should optimize one end-to-end workflow shared by domain designers, data modelers, and implementers. Broader governance workflows should follow demonstrated use.

## 8. Initial Product Scope

The smallest coherent product investigation includes:

1. Creating and editing a domain and its model elements.
2. Recording conceptual and logical representations.
3. Recording explicit mappings between representations.
4. Defining and validating a minimum set of constraints.
5. Transforming a validated logical model into one selected physical target.
6. Generating a reproducible artifact for that target.
7. Tracing generated elements back to their source elements and rules.
8. Recording revisions, provenance, ownership, and lifecycle state.
9. Exporting and importing the core catalog model without losing its semantics.
10. Isolating workspaces and enforcing basic read and edit permissions.
11. Presenting filtered perspectives without copying the underlying model.

Approval workflows, deployment environments, and arbitrary extensibility are not required for the initial proof.

## 9. Product Requirements

### 9.1 Catalog integrity

- PR-01: Every catalog item must have stable identity, type, provenance, ownership, lifecycle state, and revision information.
- PR-02: The catalog must reject references to inaccessible or nonexistent model elements.
- PR-03: Validation must distinguish structural errors, constraint violations, and transformation errors.
- PR-04: Validation failures must identify the affected catalog items and violated rules.

### 9.2 Modeling and correspondence

- PR-05: Users must be able to define model elements and their conceptual or logical representations.
- PR-06: Relationships must record their participants, meaning, and participation or cardinality rules where applicable.
- PR-07: Users must be able to define requiredness, uniqueness, referential, cardinality, and value-domain constraints.
- PR-08: Correspondence between conceptual, logical, and physical representations must be recorded explicitly.
- PR-09: A representation without a source mapping must be marked as intentionally independent or reported as incomplete.

### 9.3 Transformation and artifacts

- PR-10: The product must validate a logical model before generating an artifact.
- PR-11: Given the same model revision, transformation rules, configuration, and target version, generation must produce semantically equivalent output.
- PR-12: Generated artifacts must identify the catalog revision, transformation version, and configuration that produced them.
- PR-13: Each generated element must be traceable to its source model elements and applicable rules.
- PR-14: Generation must not silently change the authoritative catalog model.

### 9.4 Governance

- PR-15: Users must not read or modify content outside workspaces they are authorized to access.
- PR-16: The catalog must record material changes to catalog items and their responsible actor.
- PR-17: Roles must support, at minimum, separate read and edit permissions.
- PR-18: Perspectives must reference existing catalog items rather than create competing authoritative copies.

### 9.5 Portability

- PR-19: Export followed by import must preserve the core model, mappings, constraints, and provenance required for interpretation.
- PR-20: Unsupported extension data must be reported rather than silently discarded.

## 10. Initial Validation Scenario

The first product proof should demonstrate the complete path with a small domain such as Customer, Order, and Product:

1. Define the concepts and their business meanings.
2. Define a logical model with entities, attributes, relationships, and constraints.
3. Record correspondence between conceptual and logical elements.
4. Validate the logical model and expose a deliberate error with an actionable diagnostic.
5. Generate an artifact for one selected physical target.
6. Trace each generated element to its logical and conceptual sources.
7. Regenerate from the same inputs and obtain semantically equivalent output.
8. Export and re-import the catalog without losing the modeled meaning or traceability.
9. Verify that a user from another workspace cannot access the model.

This scenario tests the product hypothesis without requiring a general-purpose modeling platform.

## 11. Explicitly Deferred Scope

- Support for every database, API, or serialization target.
- Executable plugins or arbitrary subsystem-defined behavior and policy.
- Bidirectional reconciliation with externally modified artifacts.
- Deployment, migration execution, or runtime control of generated artifacts.
- Rich approval workflow, branching, merging, and collaborative conflict resolution.
- Complete enterprise architecture governance.
- Natural-language model creation.
- Customer provisioning, billing, or a specific multi-tenant deployment model.
- Quantitative scale, latency, and availability targets until an initial workflow and operating context are selected.

Deferral means that the core model should avoid unnecessarily preventing these capabilities; it does not require designing for them now.

## 12. Decisions Made in This Investigation

- The catalog is authoritative for design intent; generated artifacts are derived outputs.
- Mappings and derivations are first-class catalog data.
- Lifecycle state and deployment environment are separate concepts.
- Workspace is the initial access boundary; tenant deployment semantics are deferred.
- Perspectives are non-authoritative views, not editable model copies.
- The first proof uses one transformation target.
- Common `Thing` semantics are limited to shared catalog metadata; domain-specific behavior is not assumed.

These decisions remain hypotheses until approved by the product owner.

## 13. Decisions Explicitly Deferred

- Storage technology and system architecture.
- User interface, API style, and integration mechanisms.
- Initial physical target and its supported feature subset.
- Transformation language or execution mechanism.
- Versioning granularity and branching model.
- Extension packaging, trust, compatibility, and execution model.
- Deployment topology and tenant model.

## 14. Questions for Product Owner

1. Who is the primary user for the first release, and what current artifact or manual process would this product replace?
2. Which physical target provides the most useful first proof?
3. Must changes made outside the catalog ever become authoritative, or is generation intentionally one-way?
4. Is workspace isolation a security boundary between customers or an organizational boundary within one enterprise?
5. Which constraints are necessary to make the first transformation useful?
6. Is publication merely a lifecycle label, or must it require an approval workflow?
7. Do users need editable branches, or are revisions and non-authoritative perspectives sufficient initially?

## 15. Recommended Next Step

Resolve the product-owner questions, then convert the approved answers and requirements into a bounded componentization exercise. Architecture should follow only after product authority, initial users, system boundary, and first transformation target are explicit.

## Sign-Off

- Author: Codex, acting as product-planning agent
- Disposition: submitted for product-owner review
- Product owner: pending
- Architect review: not started
- Date: 2026-07-25
