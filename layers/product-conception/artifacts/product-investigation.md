# Domain Catalog Product Conception

## Document Status

This document records the top-level product conception. It is not an approved requirements specification, a use-case model, or a system architecture.

- Status: draft
- Product owner approval: pending
- Metamodel definition: preliminary
- Use-case realization: deferred to the next refinement layer
- Architecture decisions: deferred

## 1. Purpose

Investigate a product that can describe models, preserve their meaning, and record how one model is realized by another model or artifact closer to implementation.

The product is conceived as a governed catalog built on an extensible metamodel. The metamodel supplies general means of expression; models created for particular uses supply the domain-specific vocabulary, rules, and transformations.

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

The product would provide a metamodel with which a use-case-specific model can define:

1. the kinds of things relevant to that use case;
2. the relationships and constraints that give those things meaning;
3. the models in which those things participate; and
4. the transformations or realization relationships by which one model produces or is represented by another.

The metamodel is not itself a data model, software design model, or other use-case model. It should not embed the vocabulary or workflow of the first application simply because that application motivates its development.

This separation is central:

- the metamodel defines the general expressive machinery;
- a use-case model realizes that machinery for a particular class of work; and
- product instances contain models expressed using that use-case model.

The exact boundary between these three levels remains to be tested and refined.

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

Vocabulary and behavior required by one application belong in a model that realizes the metamodel unless evidence shows that they are general properties of all supported modeling.

### 4.7 Complexity requires evidence

New metamodel constructs should be introduced only when a concrete realization cannot be expressed coherently without them.

## 5. Preliminary Metamodel Direction

This conception identifies candidate responsibilities, not a settled metamodel.

### 5.1 Identifiable things

The catalog needs some general way to identify and type the things a model refers to. A thing may also carry provenance and revision information needed to interpret it. Which properties are universal has not yet been established.

### 5.2 Models

A model is a purposeful, coherent expression assembled from typed things, relationships, and constraints. A model has a stated context and should not be assumed to describe all aspects of its subject.

Whether models are themselves ordinary catalog things, a distinct construct, or both is unresolved.

### 5.3 Typed relationships

Relationships express meaning between things or models. Their type matters: correspondence, dependency, containment, derivation, and realization are not interchangeable.

The metamodel may need to permit use-case models to introduce additional relationship types and rules without promoting each of them into the metamodel itself.

### 5.4 Constraints

Constraints express conditions under which a model or relationship is coherent for its stated purpose. The metamodel needs a place for constraints, but their language, scope, evaluation, and ownership remain undefined.

### 5.5 Transformation and realization

A transformation describes how a source model contributes to a target model or artifact. A realization relationship records the resulting correspondence without implying that every refinement is automatic or lossless.

The product may need to represent human decisions, additions, omissions, and many-to-many correspondence as part of realization. The semantics will be established through concrete use cases rather than assumed here.

### 5.6 Provenance and authority

The catalog needs enough provenance to distinguish source, derived result, and external observation, and to determine which earlier decision should be changed when a downstream result is wrong.

This conception does not yet define ownership, lifecycle, permissions, versioning, or governance workflow. Those concerns may eventually require metamodel support, but their form should follow actual product needs.

## 6. Boundary of This Layer

This layer owns:

- the problem of preserving meaning through progressive refinement;
- the conception of an extensible metamodel and catalog;
- the distinction between metamodel, use-case model, and product-instance model;
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

## 7. First Realization to Investigate

The first intended application is support for data architecture and data modeling from domain or conceptual understanding through logical and physical realization.

That application will be defined as a model that realizes this metamodel conception. It will introduce the data-modeling concepts, relationships, constraints, model levels, and refinement behavior that the use case requires. Those concepts are not assumed to be universal metamodel constructs.

The data-modeling realization will follow DAMA nomenclature and approach carefully. DAMA-DMBOK2R and the DAMA Dictionary of Data Management are governing references for that realization. Any notation, technique, or product behavior not established by those sources must be identified as a separate design choice.

This statement selects a refinement target. It does not yet specify the target model or its product requirements.

## 8. Questions This Conception Must Resolve

1. What is the smallest set of metamodel constructs needed to express a coherent use-case model?
2. What distinguishes a model, a model type, and an instance expressed by a model?
3. Which kinds of relationship belong in the metamodel, and which should be defined by use-case models?
4. How should constraints be attached, interpreted, and scoped without choosing a constraint language too soon?
5. What does realization mean when refinement includes judgment, information loss, or information introduced downstream?
6. What provenance is necessary to restart safely from the model that owns a changed decision?
7. How can a use-case model extend the metamodel without changing the meaning of existing models?
8. Which apparent metamodel needs disappear when tested against a concrete data-modeling realization?

## 9. Decisions Deferred

- The concrete metatypes and type system.
- The treatment of model identity, composition, and versioning.
- The constraint and transformation languages.
- Whether transformations are executable, descriptive, or both.
- Governance, access-control, and collaboration semantics.
- Persistence, API, user interface, and deployment architecture.
- All data-modeling-specific rules and product behavior.

## 10. Next Refinement

The next step is to specify a transformation from this conception to a DAMA-aligned data-modeling use-case model.

That work should:

1. take the preliminary metamodel responsibilities as inputs rather than silently changing them;
2. define the data-modeling concepts and relationships required by the use case;
3. show explicitly how each use-case construct realizes or extends a metamodel construct;
4. expose gaps or contradictions in the metamodel as feedback on the transformation;
5. distinguish DAMA-grounded terminology from product design choices; and
6. leave implementation architecture and executable product requirements for later refinements.

Only after that model is reviewable should the project define the behavior of a product that supports it.

## 11. References for the First Realization

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
