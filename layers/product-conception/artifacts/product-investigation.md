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
- explicit correspondence between conceptual, logical, and physical data models;
- the derivation of generated artifacts; and
- the ownership and history needed to govern change.

## 3. Product Hypothesis

A governed catalog can reduce model drift by making domain elements, constraints, mappings, and transformation provenance first-class data.

The catalog would be authoritative for design intent. Generated artifacts would be reproducible outputs of that intent, not independent sources of truth. The first use case includes reading and comparing the selected target's implemented schema; accepting external changes as design authority or providing general bidirectional reconciliation remains a separate capability.

The initial proof should cover one end-to-end modeling flow and one implementation target. Supporting many targets, arbitrary subsystem behavior, or complete enterprise governance is not required to test the hypothesis.

### 3.1 First use case: DAMA-aligned data modeling

The first use case serves a data architect or data modeler progressing from business understanding through conceptual, logical, and physical data modeling. Its nomenclature and general approach must follow the DAMA Data Management Body of Knowledge (DAMA-DMBOK) and the DAMA Dictionary of Data Management carefully.

The current published reference is DAMA-DMBOK2R, second edition revised in 2024. DAMA provides a common body of knowledge and vocabulary rather than prescribing one modeling notation, tool, or implementation method. Any notation, normalization rules, or target-specific modeling technique adopted by this product must therefore be identified separately rather than attributed to DAMA without evidence.

For this investigation, the working model levels are:

- Conceptual data model: a business-oriented view of the subject area, its principal entities, relationships, meanings, and material business rules.
- Logical data model: a detailed, technology-independent expression of data requirements, including entities, attributes, identifiers, relationships, cardinality, domains, and applicable constraints.
- Physical data model: a technology-specific design for storing or exchanging the data, including structures and constraints appropriate to the selected target platform.

Progression between these models is an iterative design activity requiring data-architect judgment. The product may assist or generate candidates, but it must record the decisions and mappings involved rather than imply that conceptual meaning can be converted automatically and losslessly into implementation.

A physical data model describes intended target-specific design. It is not identical to a generated deployment artifact or to the schema observed in a running system. The first use case must preserve those distinctions so the intended physical model can be compared with what was actually implemented.

These working definitions correct evident conflicts in the initial product hypothesis, but they do not establish complete DAMA conformance. The detailed DMBOK2R and DAMA Dictionary texts are not present in this workspace and must be consulted before the data-modeling requirements or metamodel are approved.

### 3.2 DAMA alignment assessment

The investigation was already directionally aligned in its conceptual-to-logical-to-physical progression, technology-independent logical model, explicit rules, traceability, and target-specific physical design.

This revision corrects four conflicts or material ambiguities:

1. Conceptual, logical, and physical are now treated as related data models rather than per-element representation labels.
2. The physical data model is separated from generated deployment artifacts and the schema observed in an implemented system.
3. DAMA-aligned data-modeling constructs govern the first use case; the broader `Concept` abstraction is no longer assumed to be part of its core vocabulary.
4. Progression between models is treated as iterative, decision-bearing design rather than an automatic lossless transformation.

No incompatible implementation architecture has been selected because architecture and transformation technology remain deferred.

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

The product must distinguish domain semantics, data-modeling decisions, target-specific mappings, generated artifacts, observed implementations, and operational governance.

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

A bounded business subject area whose meaning and data requirements are being modeled. This use of `Domain` must remain distinct from an attribute's value domain.

### 5.3 Model element

A meaningful part of a data model. Initial model-element types are:

- Concept: an optional broader catalog idea whose meaning is independent of a particular implementation.
- Entity: a person, place, thing, event, or other subject about which data is represented.
- Attribute: a characteristic of an entity.
- Relationship: a meaningful association between entities.
- Constraint: a rule that determines model or data validity.
- Identifier: one or more attributes used to distinguish instances of an entity.
- Value domain: the permitted values and associated meaning for an attribute.

For the DAMA-aligned data-modeling use case, `Entity`, `Attribute`, `Relationship`, `Constraint`, `Identifier`, and `Value domain` form the initial vocabulary. `Concept` remains a possible broader catalog extension and must not replace established data-modeling terms inside this use case.

### 5.4 Data model levels

The product must distinguish three related data models:

- Conceptual data model: business meaning and subject-area structure.
- Logical data model: detailed data requirements without target-specific storage choices.
- Physical data model: a target-specific technical design.

These are models at different levels of abstraction, not merely layer labels attached independently to catalog items. Correspondence between their elements must be explicit.

### 5.5 Mapping and derivation

A mapping records correspondence between elements in different data-model levels. A derivation records how source models, transformation rules, and explicit design decisions produced a target model or generated artifact.

Mappings may be one-to-one, one-to-many, or many-to-many. Lossy or intentionally absent mappings must be identifiable rather than hidden.

Mappings and derivations support traceability; they do not remove the need for iterative modeling and human judgment.

### 5.6 Generated artifact

A reproducible output, such as a schema definition or implementation script, produced for a selected target from a validated physical data-model revision.

### 5.7 Implemented schema observation

An implemented schema observation records structures read from a selected target system at a stated time. It is evidence of realized implementation, not a replacement for the intended physical data model.

The first use case should relate observed structures to the physical and logical model elements they realize. The exact realization and conformance relationship semantics remain to be specified and tested against the concrete target.

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

The first use case selects data architects and data modelers as the primary users.

- Data architects and data modelers need to capture a conceptual data model, refine it into a logical data model, and design a physical data model without losing business meaning.
- Domain stakeholders need to recognize and validate the meaning expressed in the conceptual data model.
- Platform engineers need reproducible implementation artifacts with clear provenance.
- Governance stakeholders need ownership, auditability, and controlled publication.
- Workspace administrators need enforceable access boundaries.

The initial product should optimize this end-to-end data-modeling workflow. Broader governance workflows should follow demonstrated use.

## 8. Initial Product Scope

The smallest coherent product investigation includes:

1. Creating and editing a subject area and its conceptual data model.
2. Refining the conceptual data model into a logical data model.
3. Recording explicit mappings and design decisions between data-model levels.
4. Defining and validating a minimum set of constraints.
5. Refining a validated logical data model into a physical data model for one selected target.
6. Generating a reproducible implementation artifact from that physical data model.
7. Reading the implemented schema from the selected target and recording it as an observation.
8. Relating observed structures to the physical and logical model elements they realize.
9. Tracing generated and observed elements back to their source elements, decisions, and rules.
10. Recording revisions, provenance, ownership, and lifecycle state.
11. Exporting and importing the core catalog model without losing its semantics.
12. Isolating workspaces and enforcing basic read and edit permissions.
13. Presenting filtered perspectives without copying the underlying model.

Approval workflows, deployment environments, and arbitrary extensibility are not required for the initial proof.

## 9. Product Requirements

### 9.1 Catalog integrity

- PR-01: Every catalog item must have stable identity, type, provenance, ownership, lifecycle state, and revision information.
- PR-02: The catalog must reject references to inaccessible or nonexistent model elements.
- PR-03: Validation must distinguish structural errors, constraint violations, and transformation errors.
- PR-04: Validation failures must identify the affected catalog items and violated rules.

### 9.2 Modeling and correspondence

- PR-05: Users must be able to create and distinguish conceptual, logical, and physical data models using DAMA-aligned nomenclature.
- PR-06: Relationships must record their participants, meaning, and participation or cardinality rules where applicable.
- PR-07: Users must be able to define requiredness, uniqueness, referential, cardinality, and value-domain constraints.
- PR-08: Correspondence between elements in conceptual, logical, and physical data models must be recorded explicitly.
- PR-09: A downstream model element without a source mapping must be marked as intentionally independent or reported as incomplete.

### 9.3 Transformation and artifacts

- PR-10: The product must validate a logical data model before deriving a physical data model or generating an artifact.
- PR-11: Given the same model revision, transformation rules, configuration, and target version, generation must produce semantically equivalent output.
- PR-12: Physical data models and generated artifacts must identify the source model revisions, transformation version, explicit design decisions, and configuration that produced them.
- PR-13: Each generated element must be traceable to its source model elements and applicable rules.
- PR-14: Generation must not silently change the authoritative catalog model.
- PR-15: The product must distinguish intended physical data models, generated artifacts, and observed implemented schemas, and must record explicit relationships among them.

### 9.4 Governance

- PR-16: Users must not read or modify content outside workspaces they are authorized to access.
- PR-17: The catalog must record material changes to catalog items and their responsible actor.
- PR-18: Roles must support, at minimum, separate read and edit permissions.
- PR-19: Perspectives must reference existing catalog items rather than create competing authoritative copies.

### 9.5 Portability

- PR-20: Export followed by import must preserve the core model, mappings, constraints, and provenance required for interpretation.
- PR-21: Unsupported extension data must be reported rather than silently discarded.

## 10. Initial Validation Scenario

The first product proof should demonstrate the complete path with a small domain such as Customer, Order, and Product:

1. Define a conceptual data model whose entities, relationships, meanings, and business rules are recognizable to domain stakeholders.
2. Refine it into a technology-independent logical data model with attributes, identifiers, domains, cardinality, and constraints.
3. Record correspondence and explicit design decisions between conceptual and logical elements.
4. Validate the logical data model and expose a deliberate error with an actionable diagnostic.
5. Refine the logical data model into a physical data model for one selected target.
6. Generate and, if within the agreed proof boundary, instantiate an artifact for that target.
7. Read the implemented schema back from the target as an observation.
8. Relate observed structures to the physical, logical, and conceptual model elements they realize.
9. Detect at least one deliberate divergence between intended and observed structures.
10. Regenerate from the same inputs and obtain semantically equivalent output.
11. Export and re-import the catalog without losing modeled meaning or traceability.
12. Verify that a user from another workspace cannot access the model.

This scenario tests the product hypothesis without requiring a general-purpose modeling platform.

## 11. Explicitly Deferred Scope

- Support for every database, API, or serialization target.
- Executable plugins or arbitrary subsystem-defined behavior and policy.
- General bidirectional reconciliation beyond reading and comparing the selected initial target.
- Deployment, migration execution, or runtime control of generated artifacts.
- Rich approval workflow, branching, merging, and collaborative conflict resolution.
- Complete enterprise architecture governance.
- Natural-language model creation.
- Customer provisioning, billing, or a specific multi-tenant deployment model.
- Quantitative scale, latency, and availability targets until an initial workflow and operating context are selected.

Deferral means that the core model should avoid unnecessarily preventing these capabilities; it does not require designing for them now.

## 12. Decisions Made in This Investigation

- The catalog is authoritative for design intent; generated artifacts are derived outputs.
- The first use case follows DAMA nomenclature and general data-modeling practice, using DAMA-DMBOK2R and the DAMA Dictionary as governing references.
- Conceptual, logical, and physical are distinct data-model levels linked by explicit mappings, not per-element labels.
- A physical data model, a generated artifact, and an observed implemented schema are distinct objects.
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

1. Which concrete data-modeling workflow and current artifacts should the first use case replace or improve?
2. Which physical target provides the most useful first proof?
3. Must changes made outside the catalog ever become authoritative, or is generation intentionally one-way?
4. Is workspace isolation a security boundary between customers or an organizational boundary within one enterprise?
5. Which constraints are necessary to make the first transformation useful?
6. Is publication merely a lifecycle label, or must it require an approval workflow?
7. Do users need editable branches, or are revisions and non-authoritative perspectives sufficient initially?
8. Which modeling notation and target-appropriate normalization rules should the first proof adopt without incorrectly attributing them to DAMA?

## 15. Recommended Next Step

Consult the complete DAMA-DMBOK2R Data Modeling and Design material and the DAMA Dictionary, then resolve the product-owner questions and select the example subject area and physical target. Only then should this layer be refined into approved requirements and a concrete data-modeling use case.

## 16. References

- [DAMA-DMBOK official overview](https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/)
- [DAMA-DMBOK2R context diagrams and approved citation](https://dama.org/dmbok2r-infographics/)
- [DAMA Dictionary of Data Management official overview](https://dama.org/learning-resources/dama-dictionary-of-data-management/)
- DAMA International. *The DAMA Guide to the Data Management Body of Knowledge (DAMA-DMBOK2R).* 2nd ed., revised. Technics Publications, 2024.

## Sign-Off

- Author: Codex, acting as product-planning agent
- Disposition: submitted for product-owner review
- Product owner: pending
- Architect review: not started
- Date: 2026-07-25
