# Domain Catalog Product Conception

## Document Status

This document records the top-level product conception. It is not an approved requirements specification, a use-case model, or a system architecture.

- Status: draft
- Product owner approval: pending
- Metamodel definition: preliminary
- Specialized definition model: deferred to the next refinement layer
- Architecture decisions: deferred

## 1. Purpose

Investigate a product that can describe how models are constructed, preserve their meaning, and record how one model is realized by another model or artifact closer to implementation.

The product is conceived as a governed catalog built on a self-describing, extensible metamodel. The metamodel supplies general means of expression and rules for constructing conforming models. Models created for particular uses supply the domain-specific vocabulary, rules, and transformations.

The product should make it possible to revise an earlier model and deliberately regenerate the affected downstream realizations without treating generated output as an independent source of truth.

## 2. Problem

Products are progressively refined through descriptions that differ in abstraction, purpose, and form. The relationships between those descriptions are often implicit. As a result:

- implementation may drift from intent;
- a downstream artifact may no longer reveal why it has its present form;
- a change may be applied at the wrong level of abstraction;
- generated work may be edited as though it were authoritative; and
- restarting from an earlier decision may require reconstructing knowledge that was never recorded.

The product hypothesis is that explicit models and explicit realization relationships can reduce this loss of meaning and make regeneration from an appropriate point practical.

## 3. Product Conception

The product would provide a metamodel that defines how to construct a valid model. Its general modeling concepts cover:

1. identifiable and typed things;
2. models and their composition;
3. typed relationships between things or models;
4. constraints and the scopes in which they apply;
5. conformance between a model and the model that governs its construction; and
6. transformations or realization relationships by which one model contributes to or is represented by another.

The metamodel is itself a model expressed using these concepts and conforming to its own rules. There should not be a separate, hidden modeling language required to describe the metamodel. How this self-description is bootstrapped or implemented is deferred.

The general metamodel is not itself a data model, software design model, or other use-case-specific definition. It should not embed the vocabulary or workflow of the first application simply because that application motivates its development.

This separation is central:

- the general metamodel defines the modeling machinery and conforms to itself;
- a specialized definition model conforms to the general metamodel and defines the vocabulary and rules for a particular class of models;
- a particular subject model conforms to that specialized definition model; and
- a realization relationship connects a model to a more concrete model or artifact that represents it.

A specialized definition model is therefore a model relative to the general metamodel above it and acts as a metamodel relative to the subject models below it. `Model` and `metamodel` describe roles in a conformance relationship, not necessarily different kinds of stored object.

## 4. Governing Principles

### 4.1 Meaning precedes representation

A downstream representation must not silently replace or redefine the meaning expressed by its source.

### 4.2 Relationships are explicit

Material correspondence, dependency, derivation, and realization relationships should be represented rather than inferred from names or file placement.

### 4.3 Authority is identifiable

The product should distinguish authoritative models, derived models or artifacts, and observations of things that exist outside the catalog.

### 4.4 Refinement is traceable

It should be possible to identify the sources, decisions, rules, and transformation context associated with a downstream result.

### 4.5 Regeneration starts at the layer of change

A change should be made in the earliest model that owns its meaning and then propagated through affected realizations. Downstream output should not be treated as the appropriate editing surface merely because it is concrete.

### 4.6 The metamodel remains use-case neutral

Vocabulary and behavior required by one application belong in a specialized definition model that conforms to the general metamodel unless evidence shows that they are general properties of all supported modeling.

### 4.7 The metamodel describes itself

The general metamodel must be expressible as a valid model governed by its own constructs and conformance rules.

### 4.8 Complexity requires evidence

New metamodel constructs should be introduced only when a concrete realization cannot be expressed coherently without them.

## 5. Preliminary Metamodel Direction

This conception identifies candidate responsibilities, not a settled metamodel.

### 5.1 Identifiable things

The catalog needs some general way to identify and type the things a model refers to. A thing may also carry provenance and revision information needed to interpret it. Which properties are universal has not yet been established.

### 5.2 Models

A model is a purposeful, coherent expression assembled from typed things, relationships, and constraints. A model has a stated context and should not be assumed to describe all aspects of its subject.

Whether models are themselves ordinary catalog things, a distinct construct, or both is unresolved. Their relative roles are not: a model can govern the construction of other models while conforming to a model above it.

### 5.3 Conformance

A model conforms to a governing model when it uses the kinds of things, relationships, and constraints that the governing model permits and satisfies the applicable rules for their use.

Conformance is not derivation or generation. It does not imply that the governing model determines the content of a conforming model. It establishes that the conforming model is a valid expression in the modeling language defined by the governing model.

The general metamodel conforms to itself. A specialized definition model conforms to the general metamodel. A particular subject model conforms to its specialized definition model.

### 5.4 Typed relationships

Relationships express meaning between things or models. Their type matters: correspondence, dependency, containment, derivation, and realization are not interchangeable.

The metamodel may need to permit specialized definition models to introduce additional relationship types and rules without promoting each of them into the metamodel itself.

### 5.5 Constraints

Constraints express conditions under which a model, relationship, or modeled subject is coherent for its stated purpose. The metamodel needs a general way to represent constraints while preserving their distinct scopes:

- metamodel constraints govern what constitutes a conforming model expression;
- specialized-definition constraints govern models created for a particular use case; and
- subject-model constraints describe conditions within the particular subject being modeled.

The constraint language, evaluation mechanism, and exact attachment rules remain undefined.

### 5.6 Transformation and realization

A transformation describes how a source model contributes to a target model or artifact. A realization relationship records the resulting correspondence without implying that every refinement is automatic or lossless.

Transformation, realization, and conformance are distinct. A model can conform to its governing model without having been generated from it. The product may need to represent human decisions, additions, omissions, and many-to-many correspondence as part of realization. The semantics will be established through concrete use cases rather than assumed here.

### 5.7 Provenance and authority

The catalog needs enough provenance to distinguish source, derived result, and external observation, and to determine which earlier decision should be changed when a downstream result is wrong.

This conception does not yet define ownership, lifecycle, permissions, versioning, or governance workflow. Those concerns may eventually require metamodel support, but their form should follow actual product needs.

## 6. Boundary of This Layer

This layer owns:

- the problem of preserving meaning through progressive refinement;
- the conception of an extensible metamodel and catalog;
- the self-conformance of the general metamodel;
- the relative roles of general metamodel, specialized definition model, and subject model;
- the distinction between conformance, transformation, and realization;
- the need for explicit realization, provenance, and authority; and
- principles against which later refinements can be assessed.

This layer does not own:

- data-modeling vocabulary or model levels;
- a concrete modeling workflow;
- validation behavior or diagnostics;
- generation, import, readback, or comparison behavior;
- a physical implementation target;
- user roles, permissions, workspaces, or approval workflows;
- storage, interfaces, deployment, or system architecture; or
- numbered product requirements and acceptance scenarios.

Those details require a more concrete model and evidence from the use case they support.

## 7. First Specialized Definition to Investigate

The first intended application is support for domain-based data architecture and data modeling in accordance with DAMA, from domain or conceptual understanding through logical and physical realization.

That application will be described by a DAMA-aligned data-modeling definition model. This definition model will conform to the general metamodel and will act as the metamodel for particular domain data models created with the product.

The general metamodel will govern how the definition model expresses types, relationships, constraints, composition, and conformance. The definition model will own the actual data-modeling vocabulary and semantic rules. Its candidate vocabulary may include `Domain`, `Model`, `Conceptual entity`, `Relationship`, `Constraint`, `Relation`, `Table`, `View`, `Column`, and `Index`, but their precise names, meanings, abstraction levels, and relationships are decisions for that definition model rather than this conception.

The data-modeling definition will follow DAMA nomenclature and approach carefully. DAMA-DMBOK2R and the DAMA Dictionary of Data Management are governing references for that definition. Any notation, technique, or product behavior not established by those sources must be identified as a separate design choice.

This statement selects a refinement target. It does not yet specify the target model or its product requirements.

## 8. Questions This Conception Must Resolve

1. What is the smallest set of metamodel constructs needed to express a coherent specialized definition model?
2. What minimum conformance rules allow the metamodel to describe itself and other models coherently?
3. How should self-description be bootstrapped and revised without introducing a second, implicit modeling language?
4. Which kinds of relationship belong in the general metamodel, and which should be defined by specialized definition models?
5. How should constraints be attached, interpreted, and scoped without choosing a constraint language too soon?
6. What does realization mean when refinement includes judgment, information loss, or information introduced downstream?
7. What provenance is necessary to restart safely from the model that owns a changed decision?
8. How can a specialized definition model introduce permitted types without silently changing the general metamodel?
9. Which apparent metamodel needs disappear when tested against a concrete data-modeling definition?

## 9. Decisions Deferred

- The concrete metatypes and type system.
- The treatment of model identity, composition, and versioning.
- The bootstrap and implementation mechanism for metamodel self-description.
- The mechanism by which conformance is evaluated.
- The constraint and transformation languages.
- Whether transformations are executable, descriptive, or both.
- Governance, access-control, and collaboration semantics.
- Persistence, API, user interface, and deployment architecture.
- All data-modeling-specific rules and product behavior.

## 10. Next Refinement

The next step is to make the preliminary general metamodel reviewable as a self-conforming model and use it to express a DAMA-aligned data-modeling definition model.

The repository workflow may describe the work that produces the next refinement layer as a transform. That process term does not change the semantic relationship between the two models: the data-modeling definition model conforms to the general metamodel; it is not generated or logically deduced from it.

That work should:

1. express the general metamodel using its own constructs and demonstrate its self-conformance;
2. take that metamodel and the relevant DAMA sources as distinct inputs;
3. define the data-modeling types, relationships, constraints, and model levels required by the use case;
4. show how the definition model conforms to the general metamodel;
5. demonstrate how a particular domain data model would conform to the definition model;
6. expose gaps or contradictions as proposed changes to the metamodel rather than silently extending it;
7. distinguish DAMA-grounded terminology from product design choices; and
8. leave implementation architecture and executable product requirements for later refinements.

Only after that model is reviewable should the project define the behavior of a product that supports it.

## 11. References for the First Specialized Definition

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
