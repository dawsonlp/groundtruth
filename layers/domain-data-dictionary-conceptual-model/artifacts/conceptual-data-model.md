# Domain Data Dictionary Conceptual Data Model

## Document Status

- Status: draft
- Effective: no
- Provisional canonical reference: `CAT-CON/domain-data-dictionary@1`
- Model kind: `ConceptualDataModel`
- Governing definition: `DML-DEF` revision `19133fd`, principally `DML-CON` and `DML-SEM`
- Model family: provisional `CAT-FAMILY/domain-data-dictionary`
- Source component design: revision `5a0993d`
- DAMA verification baseline: user's 2010 DAMA-DMBOK edition
- DAMA page verification: pending

`CAT-FAMILY` and `CAT-CON` are provisional because the current canonical registry does not name the catalog's family or conceptual role. This model defines family membership as a catalog business concept governed by `DML-CON`; that placement remains reviewable and does not imply that `DML-DEF` needs a general family class.

## 1. Purpose

Define the business-significant information the Domain Data Dictionary must retain so that domain meaning can be refined into logical and physical data designs, deployed, observed, compared, maintained, and traced without losing authority or provenance.

This model describes the Domain Catalog repository as a subject of modeling. It does not describe a particular customer's operational business domain. Catalog records produced from this model are `CAT-DATA`; customer rows, documents, messages, and files described by cataloged models remain `BDM-DATA` outside the component.

## 2. Conceptual Scope

The model includes:

- business domains and shared semantic definitions;
- governing definition revisions;
- related model families, purposeful model revisions, and their elements;
- revision lineage, status, responsible agents, and provenance;
- explicit realization among artifacts and elements;
- physical targets, metadata profiles, and deployment environments;
- deployment packages, native artifacts, and execution attempts;
- observed physical state and metadata coverage; and
- intended-versus-observed comparison and maintenance disposition.

The model excludes:

- operational subject data (`BDM-DATA`);
- logical identifiers, datatypes, normalization, or record structures;
- relations, tables, columns, keys, foreign keys, indexes, or PostgreSQL constructs;
- API resources, operations, messages, protocols, or client-specific representations;
- executable transformation, validation, deployment, or collection algorithms; and
- authentication, authorization, user-interface, and infrastructure topology design.

## 3. Conceptual Modeling Conventions

- An **entity type** is a business-significant kind of thing the catalog must distinguish, not a table.
- A **business property** states meaningful information about an entity or relationship without selecting a datatype or storage representation.
- Cardinality uses `minimum..maximum`; `*` means unbounded. In the relationship table, each end states how many instances at that end may participate for one instance at the opposing end.
- A model kind is governed semantic classification. It is not one mutable `level` property that turns the same model revision from conceptual into logical or physical.
- Accepted revisions and captured observations are historical evidence. Later change creates new artifacts rather than rewriting the evidence.
- The logical model must make every conceptual realization or omission explicit.

## 4. Concept Areas

| Concept area | Purpose | Model C responsibility |
| --- | --- | --- |
| Domain semantics | Establish bounded business meaning reusable by models | Model Construction, Catalog Record Kernel |
| Model governance | Retain governing definitions, model families, revisions, elements, status, and lineage | Catalog Record Kernel, Model Construction, Conformance Validation |
| Realization and impact | Preserve why and how one artifact represents another | Realization and Impact |
| Physical target context | Interpret target-specific designs and observations | Target Capability Gateway |
| Deployment evidence | Retain immutable material and attempts around external changes | Deployment and Reconciliation |
| Observation and maintenance | Preserve actual-state evidence, coverage, differences, and disposition | Deployment and Reconciliation |
| Provenance and responsibility | Identify source, activity, evidence, and responsible human or software agents | Catalog Record Kernel across all capabilities |

## 5. Business Entity Types

Business properties below are intentionally untyped.

### 5.1 Shared semantic bindings

All concepts below belong to the `Data Domain` named **Domain Catalog**.

- Each business entity type declares a same-named `ObjectClass`; the entity definition is the object-class definition.
- Each listed business property applies one of the reusable `PropertyConcept` entries below to that object class.
- That application creates a `DataElementConcept` named `<ObjectClass>.<PropertyConcept>`.
- Each data-element concept uses the conceptual domain listed below. Value domains, logical datatypes, and data elements are deferred to `CAT-LOG`.

| Property concept | Conceptual domain | Applies to business properties concerned with |
| --- | --- | --- |
| **Designation** | Intended designations | name; native name |
| **Definition** | Statements of meaning | definition |
| **Purpose** | Intended purposes | purpose |
| **Scope** | Declared boundaries and coverage | business scope; model scope; coverage scope |
| **Classification** | Permitted semantic categories | semantic kind; model kind; agent kind; artifact kind; environment kind; activity kind; difference kind; definition kind; fact kind; value classification; evaluation scope; native datatype designation |
| **Canonical Reference** | References to governed or external things | canonical reference; external identity; source; source path; content; execution; evidence; decision; transformation; resolution; locator; inventory reference; portable base reference |
| **Version Designation** | Version and revision designations | version; authority version; collector version; lineage; revision |
| **Authority** | Sources of semantic authority | authority; governing source |
| **Lifecycle State** | Permitted lifecycle and outcome states | family status; artifact status; package status; execution status; coverage status; disposition |
| **Evidence Fingerprint** | Evidence and content fingerprints | content digest; evidence digest |
| **Occurrence Time** | Points in time associated with activities | recorded time; attempted time; captured time; assessed time |
| **Rationale** | Explanations and decision reasoning | rationale; information-loss statement; non-OCL rationale |
| **Native Language** | Languages governing external artifact content | native language |
| **Expression Text** | Statements interpreted by a named language and scope | expression body |
| **Lexical Representation** | Target-owned lexical representations of values | lexical value |
| **Product Designation** | Product and technology designations | product; technology family |
| **Inventory Exception** | Items not covered by an assessment | uncovered items |

The logical refinement may split a broad property concept when different value meaning or integrity requires it. It must record that split as a realization rather than silently treating identical words as identical semantics.

### 5.2 Domain semantics and governance

| Entity type | Business definition | Material business properties |
| --- | --- | --- |
| **Data Domain** | A bounded area of business meaning and responsibility within which semantic definitions and model families are interpreted | name; definition; business scope |
| **Semantic Definition** | A reusable statement of business meaning used by model elements, including object classes, property concepts, data-element concepts, conceptual domains, value domains, or data elements | name; definition; semantic kind; governing source |
| **Governing Definition Revision** | An identified revision of a model that determines the permitted form and rules of another model, such as `CMOF-GOV` or `DML-DEF` | canonical reference; governing role; version; authority; content digest |
| **Model Family** | The purposeful collection of related model revisions that describe one business scope across conceptual, logical, physical, deployment, and observation concerns | name; purpose; business scope; family status |
| **Model Revision** | One immutable historical or evolving draft expression of a purposeful model, classified by its governed model kind | name; definition; purpose; scope; model kind; lineage; revision; artifact status |
| **Model Element** | A named, defined part owned by exactly one model revision and permitted by that model's kind | name; definition; element kind |
| **Expression Specification** | A dependent statement interpreted under one named language and evaluation scope, used for a constraint, derivation, query, guard, target expression, or other governed purpose; it has no independent authority or lifecycle | native language; expression body; evaluation scope; non-OCL rationale |

### 5.3 Realization and provenance

| Entity type | Business definition | Material business properties |
| --- | --- | --- |
| **Realization Set** | The complete declared refinement context connecting one source artifact revision to one more-concrete target artifact revision | purpose |
| **Realization Mapping** | A judgment-bearing statement that source items are realized, omitted, or that target items are introduced, including rationale | disposition; rationale; information-loss statement; transformation or procedure reference |
| **Responsible Agent** | A human, organization, software agent, AI agent, or automation accountable for a recorded catalog activity or assertion | name; agent kind; external identity reference |
| **Provenance Record** | Evidence of who or what created, changed, imported, transformed, accepted, deployed, collected, or assessed a catalog artifact and from which sources | activity kind; recorded time; source reference; evidence digest; rationale |

`Responsible Agent` describes accountability and evidence, not authorization policy. `Provenance Record` and `Responsible Agent` are catalog business concepts required by the component design and `CAT-DATA` scope. They use the general entity and relationship machinery of `DML-CON`; their exact PROV-DM alignment remains pending.

### 5.4 Physical target and deployment context

| Entity type | Business definition | Material business properties |
| --- | --- | --- |
| **Physical Target** | A named product, protocol, format, or storage technology and version whose semantics govern a physical design or observation | product; version; technology family |
| **Target Metadata Profile** | A versioned account of the native element kinds, properties, relationships, and coverage inventory available for a physical target | authority; authority version; coverage scope; source inventory reference |
| **Target Metadata Definition** | One profile-owned definition of a native element kind, property, or relationship and the target semantics needed to interpret it | name; definition kind; native name; source path; value classification; portable base reference |
| **Target-Native Metadata Fact** | One designed or observed native value or relationship interpreted by a target metadata definition without pretending that it is universally portable | fact kind; lexical value; native datatype designation |
| **Deployment Environment** | A named place where artifacts may be deployed and physical state observed for one target | name; environment kind; external locator |
| **Deployment Package** | An immutable revisioned collection of native artifacts intended to realize one physical-design revision in one environment | name; revision; package status |
| **Deployment Artifact** | One executable or publishable target-owned item within a deployment package | artifact kind; native language; content reference; content digest |
| **Deployment Attempt** | Evidence that a particular immutable package was or will be applied to a particular environment | attempted time; execution status; execution reference |

### 5.5 Observation and maintenance evidence

| Entity type | Business definition | Material business properties |
| --- | --- | --- |
| **Observation Capture** | Evidence describing how and when an external environment was inspected to produce an observed physical-model revision | captured time; collector identity and version; source reference; evidence digest |
| **Metadata Coverage Assessment** | A bounded judgment about how completely an observed model represents the inventory declared by one target metadata profile | assessed time; coverage status; uncovered items; evidence reference |
| **Physical Comparison** | An assessment of one intended physical-design revision against one observed physical-model revision for a compatible target and environment | assessed time |
| **Physical Difference** | A material statement of equivalence, absence, unexpected presence, change, or unresolved correspondence between expected and observed elements | difference kind; disposition; rationale; resolution reference |

## 6. Business Relationships and Cardinalities

| Relationship | First end | Second end | Business meaning |
| --- | --- | --- | --- |
| **Domain defines semantics** | Data Domain `1` | Semantic Definition `0..*` | Every semantic definition belongs to exactly one domain; a domain may begin without definitions |
| **Domain scopes families** | Data Domain `1` | Model Family `0..*` | Every model family is interpreted within exactly one domain; placement of this relationship in `CAT-CON` remains under review |
| **Family groups models** | Model Family `1` | Model Revision `0..*` | Every model revision belongs to exactly one family; a family may exist before its first model revision |
| **Definition governs model** | Governing Definition Revision `1` | Model Revision `0..*` | Every model revision identifies exactly one immediate governing-definition revision |
| **Model contains elements** | Model Revision `1` | Model Element `0..*` | Every model element is owned by exactly one model revision |
| **Semantic definition characterizes element** | Semantic Definition `0..*` | Model Element `0..*` | Applicable semantic definitions provide reusable meaning to model elements; exact required kinds depend on the governed model kind |
| **Subject owns expression** | Catalog artifact or Model Element `1` | Expression Specification `0..*` | Every expression belongs to exactly one governed subject and identifies the language and evaluation scope under which it is interpreted |
| **Model supersedes model** | Model Revision `0..*` predecessor | Model Revision `0..*` successor | Supersession records lineage without altering prior content and must remain acyclic |
| **Agent is responsible for provenance** | Responsible Agent `1..*` | Provenance Record `0..*` | Every provenance record identifies at least one responsible agent; an agent may participate in many records |
| **Provenance documents subject** | Provenance Record `1..*` | Catalog artifact or evidence item `0..*` | A record documents at least one subject; an artifact may have many provenance records |
| **Realization set connects artifacts** | Source Model Revision or Deployment Package `1` | Target Model Revision or Deployment Package `1` | One set names one distinct source and one more-concrete target; the refinement graph remains acyclic |
| **Realization set contains mappings** | Realization Set `1` | Realization Mapping `1..*` | Every mapping belongs to exactly one set and together the mappings state its coverage |
| **Mapping covers items** | Realization Mapping `0..*` | Source/target Model Element or Deployment Artifact `0..*` | A realized mapping has source and target items; introduced or omitted mappings have one empty side according to disposition; an item may participate in mappings across refinements |
| **Target provides profiles** | Physical Target `1` | Target Metadata Profile `1..*` | Every target has at least one profile; each profile interprets exactly one target/version |
| **Profile defines native vocabulary** | Target Metadata Profile `1` | Target Metadata Definition `0..*` | Every native definition belongs to exactly one profile and is meaningful only under that target, version, authority, and coverage scope |
| **Native fact uses definition** | Target Metadata Definition `1` | Target-Native Metadata Fact `0..*` | Every native fact resolves to exactly one definition in the active target metadata profile |
| **Native fact concerns physical element** | Target-Native Metadata Fact `0..*` | Physical Model Element `1..*` | A native value concerns one element; a native relationship concerns its governed source and target elements |
| **Target defines environments** | Physical Target `1` | Deployment Environment `0..*` | Every environment names exactly one target; a target may have no registered environment |
| **Physical model uses target** | Physical Target `1` | Physical Model Revision `0..*` | Every intended or observed physical model identifies exactly one target |
| **Package realizes design** | Intended Physical Model Revision `1` | Deployment Package `0..*` | Every package is produced from exactly one intended physical-design revision |
| **Package targets environment** | Deployment Environment `1` | Deployment Package `0..*` | Every package names exactly one target environment compatible with its physical design |
| **Package contains artifacts** | Deployment Package `1` | Deployment Artifact `1..*` | Every deployment artifact belongs to exactly one immutable package |
| **Attempt applies package** | Deployment Package `1` | Deployment Attempt `0..*` | Every attempt names exactly one package; a package may be attempted several times |
| **Attempt occurs in environment** | Deployment Environment `1` | Deployment Attempt `0..*` | Every attempt occurs in the package's named environment |
| **Observation captures environment** | Deployment Environment `1` | Observation Capture `0..*` | Every observation describes one environment at one point in time |
| **Observation produces observed model** | Observation Capture `1` | Observed Physical Model Revision `1` | Each observation produces one observed model and each observed model has one capture record |
| **Coverage assesses observation** | Observed Physical Model Revision `1` | Metadata Coverage Assessment `0..*` | Each assessment concerns one observed model and one active metadata profile |
| **Coverage uses profile** | Target Metadata Profile `1` | Metadata Coverage Assessment `0..*` | Every assessment identifies exactly one profile whose declared inventory and scope determine the meaning of coverage |
| **Comparison uses intended design** | Intended Physical Model Revision `1` | Physical Comparison `0..*` | Every comparison names one expected physical-design revision |
| **Comparison uses observation** | Observed Physical Model Revision `1` | Physical Comparison `0..*` | Every comparison names one observed physical-model revision for a compatible target and environment |
| **Comparison contains differences** | Physical Comparison `1` | Physical Difference `0..*` | Every difference belongs to exactly one comparison; an empty set means no material difference in scope |
| **Difference covers physical elements** | Physical Difference `0..*` | Intended and/or observed Model Element `0..*` | Expected and observed elements participate according to the difference kind; one element may appear in comparisons at different times |

`Physical Model Revision`, `Intended Physical Model Revision`, and `Observed Physical Model Revision` are governed categories of `Model Revision`, not separate mutable levels. Their technology-neutral categorical representation is a decision for `CAT-LOG`.

`Catalog artifact` is a conceptual category that includes revisioned model and deployment artifacts. `Evidence item` includes attempts, captures, assessments, comparisons, differences, and provenance-bearing results. Their exact logical supertype or association structure is deferred.

The realization endpoint unions, expression-owner category, evidence-subject category, and physical-model categories are logical-design decisions. The conceptual requirement is that the relationships are explicit, typed, complete, and do not depend on name matching.

## 7. Business Constraints

### Authority and revision

1. Every model revision identifies its exact governing-definition revision, domain, and model family.
2. An accepted, superseded, or retired model revision is immutable; change creates another revision with explicit lineage.
3. A governing definition stored in the catalog does not acquire authority to redefine its external or upstream source.
4. Model kind determines permitted content. A model revision cannot be converted from conceptual to logical or physical by changing a label.
5. Every authority-bearing acceptance, import, transformation, deployment, observation, and disposition has provenance and a responsible agent.
6. Every governed expression identifies its language, body, evaluation scope, and required rationale when OCL would otherwise have been expected.

### Meaning and realization

7. Every model element belongs to exactly one model revision and uses semantics available from its domain or explicitly imported domains.
8. Realization is explicit, many-to-many, and revision-specific. Names and structural similarity do not establish correspondence.
9. A realized mapping has source and target items; an introduced mapping has only target items; an omitted mapping has only source items.
10. Introduced and omitted mappings state a rationale.
11. Realization and supersession graphs remain acyclic.
12. Every source and target item in the declared scope is covered by a realization mapping or an explicit omission/introduction.
13. Every governed object, property value, ordered membership, expression, and relationship required by the represented definition can be reconstructed without invented, dropped, or reordered meaning.

### Deployment and external effects

14. A deployment package is immutable and identifies the exact intended physical-design revision, environment, target profile, and content digests used to produce it.
15. Deployment success is execution evidence, not proof that runtime state equals intended design.
16. A deployment attempt cannot change the accepted model or package it references.
17. Catalog commit and external infrastructure change are not treated as one atomic fact; unresolved attempts remain reconcilable by execution reference and observation.

### Observation and maintenance

18. An observed physical model describes external state and never silently becomes intended design.
19. An observation identifies environment, capture time, collector and version, source reference, evidence digest, and active target profile.
20. Every target-native metadata fact resolves to a definition in the active profile and retains its target-owned lexical representation.
21. A complete coverage assessment is valid only for its stated target, profile version, coverage scope, source inventory, access, and collection evidence.
22. A physical comparison identifies one intended and one observed physical revision for compatible targets and the same environment.
23. Accepting a discovered difference into design creates a new revision beginning at the earliest model that owns the meaning; it does not edit the observation or prior design.

### Repository and access boundary

24. The Domain Data Dictionary stores catalog definitions and evidence (`CAT-DATA`) and does not acquire operational subject data (`BDM-DATA`) merely because it describes that data.
25. PostgreSQL persistence must preserve the conceptual meaning but supplies no conceptual entity, relationship, or business rule in this model.
26. Human and machine clients will use the same application capability semantics; no client gains semantic authority through direct repository manipulation.
27. Authorization may differ by responsible agent, capability, artifact state, and environment without changing the meaning of the capability itself.

## 8. Relationship Map

```text
Data Domain ----defines----> Semantic Definition
     |
     +----scopes----> Model Family ----groups----> Model Revision
                                               |        |
Governing Definition Revision ----governs------+        +----contains----> Model Element

Model Revision / Deployment Package
                |
                +---- Realization Set ----contains----> Realization Mapping
                                                         |
                                                         +----covers----> Model Element / Deployment Artifact

Physical Target ----provides----> Target Metadata Profile
       |                              |
       |                              +----defines----> Target Metadata Definition ----interprets----> Target-Native Metadata Fact
       +----defines----> Deployment Environment

Intended Physical Model ----produces----> Deployment Package ----contains----> Deployment Artifact
                                                   |
                                                   +----attempted as----> Deployment Attempt

Deployment Environment ----captured by----> Observation Capture ----produces----> Observed Physical Model
                                                                                       |
Intended Physical Model --------compared with-------------------------------------------+
                                      |
                                      v
                              Physical Comparison ----contains----> Physical Difference

Responsible Agent ----accountable for----> Provenance Record ----documents----> catalog artifacts and evidence
```

## 9. Traceability to Governing Models and Responsibilities

| Conceptual concern | Governing representation or motivating source | Status |
| --- | --- | --- |
| Data Domain | `DataDomain` | Direct |
| Semantic Definition | `DML-SEM` semantic element classes | Direct; exact standard multiplicities still pending upstream |
| Governing Definition Revision | `RefinementArtifact`, canonical registry, conformance relationships | Composed from defined concepts |
| Model Revision | `DataModel`, `RefinementArtifact`, model subclasses | Direct |
| Model Element | `ModelElement` | Direct |
| Expression Specification | `ExpressionSpecification` and OCL usage profile | Direct |
| Model Family | `BDM-FAMILY` registry prose plus `DML-CON` business-entity machinery | Downstream catalog concept; placement remains reviewable |
| Realization Set and Mapping | `DML-REA` | Direct |
| Physical Target and Profile | `DML-PHY` | Direct |
| Target Metadata Definition and Fact | `NativeElementKindDefinition`, `NativePropertyDefinition`, `NativeRelationshipKindDefinition`, `NativeMetadataValue`, `NativeMetadataRelationship` | Conceptual grouping of direct physical-definition constructs |
| Deployment Environment, Package, Artifact, Attempt | `DML-PHY`, `DML-DEP` | Direct |
| Observation, Coverage, Comparison, Difference | `DML-OBS` | Direct |
| Responsible Agent and Provenance Record | `CAT-DATA` scope, `DML-CON`, and PROV-DM alignment | Valid catalog concepts; exact standard mapping pending |
| Conceptual and logical catalog role references | `CAT-PHY` repository chain | Gap: canonical registry omits `CAT-FAMILY`, `CAT-CON`, and `CAT-LOG` |

No PostgreSQL or API concept is required to complete the conceptual inventory.

## 10. Required Logical Refinement

The next `CAT-LOG` artifact must determine, without changing this model's meaning:

- logical entities and their identifiers;
- logical attributes, datatypes, optionality, and value domains;
- representation of model and element kinds without a mutable abstraction-level label;
- representation of artifact, element, and provenance subject categories;
- ordered many-to-many realization participation;
- revision lineage and immutable-state integrity;
- logical structures for native metadata definitions and values;
- expression content and evaluation-scope representation;
- logical constraints equivalent to every business constraint above; and
- explicit realization coverage from every conceptual entity, property, and relationship.

The logical model must not yet select PostgreSQL structures or API message shapes. Those belong to later physical and interface refinements.

## 11. Open Questions for Review

1. Is `Model Family` the correct catalog business term and boundary for grouping all purposeful models for one scope, or should `CAT-CON` use a more precise term?
2. Does every model revision belong to exactly one family, or is legitimate cross-family membership required?
3. Are `Responsible Agent` and `Provenance Record` sufficient at the conceptual level, or must source material, decisions, and activities be separate entity types?
4. Must validation assessments be retained as authoritative catalog evidence, or are reproducible diagnostics sufficient?
5. Which lifecycle transitions require explicit human acceptance rather than authorization policy or automation?
6. Is an empty accepted model valid for any model kind, or only while it remains a draft?
7. Should a metadata coverage assessment belong to the observation capture, the observed model, or both through one explicit assessment context?

These questions are inputs to product-owner review and the logical transform. They do not authorize hidden logical or physical assumptions in this conceptual layer.
