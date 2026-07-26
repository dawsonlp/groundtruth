# Data-Modeling Language Definition

## Document Status

- Status: draft
- Effective: no
- Governing model: CMOF 2.5.1, presumed pending the follow-up ADR
- Standards profile: incorporated in section 2
- DAMA verification baseline: user's 2010 DAMA-DMBOK edition
- DAMA page verification: pending
- External normative-text verification: pending where identified below
- Machine-readable CMOF validation: pending

This artifact defines the modeling language for the first application of Domain Catalog. It is intended to become a CMOF-conforming model that acts as the governing model for particular data models. Those models may progress from conceptual meaning through logical and technology-specific physical design, deployment, observation, and maintenance.

The language is technology-neutral at its core but must have a lossless physical repository realization in a relational database. That repository is the deployed representation of the language and its instances; it is distinct from the subject databases, APIs, schemas, and stored assets described by the catalog. This artifact constrains that future repository realization but is not itself its database schema, validator design, or user-interface design.

## 1. Governing Relationships

```text
CMOF 2.5.1
    governs the valid form of
this data-modeling language definition
    governs the valid form of
particular conceptual, logical, relational-logical, and heterogeneous physical data models
    whose elements may be realized by
deployment artifacts and observed deployed resources
```

`Conforms to` means that a model uses permitted element types and satisfies this definition's rules. It does not mean that the model was generated from its governing model.

`Realizes` relates a more concrete model or deployment artifact to meaning in an upstream artifact. Realization does not imply equivalence, automation, or absence of added decisions. Observation records what is found in a deployed environment; it is not silently treated as the authoritative design.

## 2. Standards Profile and Authority

This section is the authority for how external standards constrain this language. The transform's `standards-assessment.md` records the investigation that produced the profile; it is evidence rather than a second definition.

The status terms mean:

- **Governing** — the standard defines the valid form of this language definition.
- **Adopted** — the language uses the identified semantics for the stated concern.
- **Alignment required** — the language retains an explicit mapping boundary but does not import the standard's complete metamodel.
- **Informative** — the source is prior art and creates no conformance obligation.
- **Verification pending** — adoption is a design decision, but detailed conformance must not be claimed until the normative text or executable constraints have been checked.

| Standard or reference | Status in this language | Concern incorporated | Authority boundary |
| --- | --- | --- | --- |
| [OMG MOF 2.5.1, CMOF](https://www.omg.org/spec/MOF/2.5.1) | Governing; acceptance pending | Packages, classes, datatypes, enumerations, properties, multiplicity, composition, generalization, constraints, identifiers, and reflection | Defines the form of this language, not data-modeling meaning |
| [ISO/IEC 19508:2014, MOF Core](https://www.iso.org/standard/61844.html) | Alignment required; version delta pending | ISO-standardized MOF baseline | Predates the selected OMG MOF 2.5.1; ISO and OMG conformance must not be treated as identical without a delta assessment |
| [ISO/IEC 19507:2012, OCL 2.3.1](https://www.iso.org/standard/57306.html) | Default constraint and query language wherever its side-effect-free model semantics apply; encoding pending | `DM-*` rules, derived values, model queries, guards, and business/logical constraints over a defined subject-data environment | Does not replace SQL syntax, external facts, temporal state that is not modeled, or procedural transformation bodies |
| [ISO/IEC/IEEE 31320-2:2012, IDEF1X97](https://www.iso.org/standard/60614.html) | Adopted for overlapping schema semantics; normative-text verification pending | Entity types, attributes, identifiers, relationships, relationship ends, and cardinality | Its term `conceptual schema` is not assumed to equal this language's `ConceptualDataModel`; constructs are mapped individually |
| [ISO/IEC 11179-31:2023](https://www.iso.org/standard/78925.html) | Adopted semantic vocabulary; multiplicity verification pending | Object classes, properties, data-element concepts, conceptual domains, value domains, datatypes, and data elements | Registry administration is not imported into the modeling language |
| [ISO/IEC 11404:2007](https://www.iso.org/standard/39479.html) | Adopted datatype framework; type catalogue pending | Separation of conceptual, structural, and implementation datatype notions and explicit datatype mappings | Does not define business meaning or target-product types |
| [ISO/IEC 9075-2:2023, SQL/Foundation](https://www.iso.org/standard/76584.html) | Adopted portable physical baseline; normative-text verification pending | Tables, views, columns, physical datatypes, and SQL integrity constraints | Target products govern extensions and physical access structures such as indexes |
| [ISO/IEC 9075-11:2023, SQL/Schemata](https://www.iso.org/standard/76586.html) | Adopted relational metadata baseline; normative-text verification pending | Information and definition schemas used to describe SQL implementations | Vendor catalogs and product extensions remain governed by the named target profile |
| [JSON Schema Draft 2020-12](https://json-schema.org/specification) | Alignment required | JSON structure, validation vocabulary, dialect identification, and references | A JSON Schema document is a physical schema artifact; it does not replace conceptual or logical meaning |
| [W3C XML Schema Definition Language 1.1](https://www.w3.org/TR/xmlschema11-1/) | Alignment required | XML element, attribute, type, occurrence, identity, and validation metadata | XML Schema structures are represented through a target profile rather than generalized into all data models |
| [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html) | Alignment required | HTTP API services, operations, messages, media types, and schema references | Describes an API contract and its data surfaces, not the internal data model or implementation of the service |
| [W3C Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/) | Alignment required | Dataset, distribution, data service, and catalog interchange concepts | Does not define detailed physical schemas or product-specific operational metadata |
| [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | Alignment required | Provenance of artifacts, observations, transformations, and responsible agents | This draft adopts only the provenance boundary needed for traceability; it does not import the complete PROV model |
| [ISO/IEC 11179-35:2023](https://www.iso.org/standard/81727.html) | Alignment required | Registration of models, metamodels, concepts, and mappings | Does not define the models' internal semantics or physical instantiation |
| [ISO/IEC 19763-12:2015 with Amendment 1:2023](https://www.iso.org/standard/61559.html) | Alignment required | Registration of information-requirement and database-structure models | A registry metamodel, not the data-modeling language |
| [ISO/IEC 19509:2014, XMI](https://www.iso.org/standard/61845.html) | Selected validation representation; production pending | The XMI 2.4.2 representation referenced by MOF 2.5.1 | Does not define the runtime relational repository schema or require XMI as the runtime persistence format |
| [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1) and [ISO/IEC 19505-1:2012](https://www.iso.org/standard/32624.html) | Alignment required for notation and interchange; version delta pending | Shared structural kernel and standard class-diagram presentation | A data model governed here is not thereby a UML model, and the ISO publication predates OMG UML 2.5.1 |
| [OMG CWM 1.1](https://www.omg.org/spec/CWM/1.1) | Informative | Relational, datatype, key/index, expression, transformation, and warehouse-model coverage precedent | Warehouse-oriented, MOF 1.3/XMI 1.1-era, and not imported as this language's metamodel |
| User's 2010 DAMA-DMBOK edition | Verification baseline | Conceptual, logical, and physical abstraction; DAMA nomenclature and practice | Not a formal metamodel or substitute for the standards assigned above |

### 2.1 Precedence and conflict rules

1. A standard governs only the concern assigned to it in the table.
2. CMOF governs whether this definition is a valid metamodel; the adopted data standards govern the meanings expressed by CMOF classes and properties.
3. DAMA 2010 governs the intended data-modeling abstraction and approach. It does not override a formal standard silently; any conflict must be recorded and resolved explicitly.
4. A target-platform or format specification may specialize the physical package. It must preserve any applicable portable meaning and identify the profile, version, and native extensions under which each physical fact is interpreted.
5. OCL is the default for every constraint, derivation, query, guard, or pre/postcondition expressible over modeled state. A non-OCL expression must identify the owning language and either be intrinsic target syntax or state why OCL is insufficient.
6. `Project choice` is used only where the adopted sources leave a gap or where this language deliberately composes them.
7. There is no assumed universal NoSQL, API, or storage metamodel. Shared constructs belong in the physical core; technology-specific kinds, properties, and links belong in explicit metadata profiles.
8. A pending verification item prevents a detailed conformance claim but does not move the standards decision back into transform evidence.

### 2.2 OCL usage profile

OCL is applied at two distinct evaluation planes:

1. **Definition and model validation.** The OCL context is a CMOF class in this language, such as `LogicalEntityType` or `ForeignKeyConstraint`. These expressions validate whether a particular data model conforms to this definition. All `DM-*` rules and derived navigation properties belong here.
2. **Subject-data validation.** The OCL context is a classifier defined by a particular conceptual or logical model, such as that model's `OrderLine`. These expressions constrain occurrences described by the model. This use is valid only when an OCL evaluation environment maps the model-defined entity types, attributes, relationships, datatypes, and values into OCL classifiers and properties.

OCL may also provide queries, guards, and pre/postconditions to a later transformation language. Because OCL is side-effect free, it does not by itself specify how a target model is created or mutated.

SQL view definitions, column defaults, checks, JSON/XML schema constraints, API-description expressions, and other target-owned rules retain the language of their `PhysicalTarget`. OCL can validate their surrounding model and can be the upstream logical constraint they realize, but translating OCL into target syntax is a separate, explicit realization decision.

Rules requiring external observations, event history, or time not represented in the model are not falsely declared OCL-executable. They carry a non-OCL rationale until their required state is modeled or another governing rule language is selected.

### 2.3 Construct traceability

| Language concern | Primary source | Project composition or extension |
| --- | --- | --- |
| Definition packages, types, properties, inheritance, containment, and constraints | OMG CMOF 2.5.1; ISO/IEC 19508 alignment | Package boundaries, the selected CMOF subset, and explicit treatment of the OMG/ISO version delta |
| `DM-*` rules, derived navigation, model queries, and expressible subject constraints | ISO/IEC 19507 OCL | Prose is currently authoritative until equivalent OCL and both evaluation environments are committed and validated |
| `ExpressionSpecification` and evaluation scope | OCL, ISO SQL, and named target languages | One wrapper records the language, body, evaluation plane, and reason for any non-OCL exception |
| `ObjectClass`, `PropertyConcept`, `DataElementConcept`, `ConceptualDomain`, `ValueDomain`, `DataElement` | ISO/IEC 11179-31 | Domain ownership and imports connect the standard vocabulary to particular models |
| Business entity types, properties, relationships, ends, cardinality, and identifiers | DAMA 2010 and ISO/IEC/IEEE 31320-2 | Separate conceptual and logical model kinds; reified n-ary relationships |
| Logical, structural, and physical datatype separation | ISO/IEC 11404 and ISO/IEC 11179-31 | Explicit realization between value domains and target datatypes remains to be completed |
| Record, collection, map, choice, and opaque logical structures | ISO/IEC 11404 structural datatype direction; exact mapping pending | Technology-neutral composition supports structured, semi-structured, and deliberately opaque content without importing target schema languages |
| Relations, relation attributes, candidate keys, and relational foreign keys | DAMA 2010 and IDEF1X where applicable | A relational-logical model is explicitly separate from a physical database model |
| Tables, views, columns, primary/unique/foreign-key/check constraints | ISO/IEC 9075-2 | The relational physical profile preserves the distinction between portable SQL and target extensions |
| Relational catalog and implementation metadata | ISO/IEC 9075-11 and the named product catalog | Coverage is assessed against a target/version inventory; unstandardized kinds, properties, and links remain explicit profile metadata |
| JSON and XML schema documents and shapes | JSON Schema 2020-12 and W3C XML Schema 1.1 | A shared shape kernel supports navigation while the native schema profile remains authoritative for exact semantics |
| HTTP API data surfaces | OpenAPI 3.2.0 | Services, operations, messages, media types, and schema references are physical data interfaces |
| Datasets, distributions, data services, and stored assets | DCAT 3 plus named storage profiles | Object, file, blob, or block-storage metadata is target-relative; unstructured content is described by metadata rather than falsely given tabular structure |
| Provenance and operational observations | PROV-DM alignment | Design authority, generated artifacts, external observation, collection time, and maintenance disposition remain distinct |
| Indexes | Target-platform specification; CWM as informative precedent | Core `Index` preserves the distinction between access path and integrity constraint |
| Cross-artifact realization and registration mapping | ISO/IEC 11179-35 and ISO/IEC 19763-12 alignment | Many-to-many realization across models and deployment artifacts, introduction, omission, rationale, and coverage rules are project semantics |

## 3. Abstraction and Lifecycle Boundaries

The abstraction belongs to a model. An element belongs to exactly one model and acquires its permitted vocabulary from that model's kind. Physical design, deployment material, and observation are separate artifacts because intended state, executable material, and actual state can differ.

| Model kind | Purpose | Includes | Excludes |
| --- | --- | --- | --- |
| `ConceptualDataModel` | State business meaning and scope | Business entity types, business properties, relationships, cardinality, and business constraints | Relations, foreign keys, tables, columns, platform types, indexes |
| `LogicalDataModel` | State technology-neutral data structure and integrity | Logical entity types, attributes, identifiers, relationships, constraints, and scalar, record, collection, map, choice, or opaque value structures | Database products, storage objects, platform types, indexes |
| `RelationalLogicalDataModel` | State a logical model using the relational model | Relations, relation attributes, candidate keys, and relational foreign keys | Tables, storage options, platform data types, indexes |
| `PhysicalDataModel` with `role = design` | State technology-specific detailed design for one named target | Relational structures; NoSQL structures; API contracts; JSON or XML schemas; data files, objects, blobs, or block-storage descriptions; physical constraints and access structures; target-native metadata | Unresolved business meaning, unnamed implementation targets, deployment execution, or claims about observed state |
| `DeploymentPackage` | Hold executable or publishable material that realizes a physical design | DDL, migrations, schema documents, API descriptions, configuration, and other target-owned artifacts plus integrity digests | Conceptual or logical authority and unverified claims about deployed state |
| `PhysicalDataModel` with `role = observed` | Record a point-in-time inventory read from a deployed environment | Discovered resources, structures, native metadata, collection provenance, and unresolved target extensions | Intended design authority or an implicit declaration that drift is acceptable |
| `PhysicalComparison` | Compare intended and observed physical state for maintenance | Missing, unexpected, changed, and equivalent correspondences with dispositions | Mutation of either source model or replacement of upstream design decisions |

A relation and a table are not synonyms. A relation is a logical value with a heading and relational constraints. A table is a physical database object in a target environment. A table may realize one relation, several relations, or part of a relation, and that correspondence is explicit.

Nor is a logical entity necessarily realized as a table. It may be realized as a document collection, key-value entry, column family, graph structure, API message, JSON or XML shape, file set, object collection, or several such artifacts. Refinement is a directed acyclic graph rather than a fixed four-step pipeline: a branch may omit the relational-logical stage or produce several alternative physical designs.

Maintenance creates new revisioned artifacts. It does not overwrite the historical design or reinterpret an observation as intent. A material change begins at the earliest model that owns the changed meaning and produces new downstream realizations, deployment material, observations, and comparisons.

## 4. CMOF and Repository Representation

The definition consists of CMOF packages named `Core`, `Semantics`, `Conceptual`, `Logical`, `Relational`, `Physical`, `Deployment`, `Observation`, and `Realization`.

- Every type below is a CMOF `Class`, `DataType`, or `Enumeration`.
- Every field or role is a CMOF `Property` with the stated multiplicity.
- `owns` denotes a composite CMOF property.
- `extends` denotes CMOF `Generalization`.
- `redefines` denotes CMOF property redefinition that narrows an inherited role without creating a second authority.
- `{derived}` denotes a read-only navigation calculated from the named authoritative reverse reference, not separately stored membership.
- Each structural rule in section 14 is a CMOF `Constraint` whose specification is an OCL `OpaqueExpression`; rules that compare the catalog to an external metadata surface also require identified collection or validation evidence.
- Every derived property has an OCL derivation in the machine-readable definition.
- Subject-model constraints such as a foreign key are instances of language classes; they are not CMOF constraints governing the form of the language.

This Markdown is a review projection, not the machine-readable CMOF representation required for acceptance.

### 4.1 Required relational repository realization

The production catalog is expected to deploy this language and its instances as a physical relational database artifact. The later repository design must provide a lossless, bidirectional representation of:

- every CMOF package, class, datatype, enumeration, property, generalization, constraint, and expression in this definition;
- every domain, semantic element, model, model element, physical metadata profile, deployment artifact, observation, comparison, and realization record;
- stable identity, revision lineage, artifact status, provenance, ordered collections, multiplicity, and explicit cross-artifact correspondence; and
- both portable typed constructs and target-native metadata whose exact semantics are owned by a named product, standard, dialect, or format version.

The machine-readable CMOF model remains the semantic authority. The relational repository schema realizes it and must support round-trip reconstruction without inventing, dropping, or changing meaning. The repository schema is itself a subject physical model governed by this language, so its tables, constraints, indexes, deployment artifacts, and observed runtime state can be cataloged and related back to the CMOF definition.

XMI remains a validation and interchange representation. It is not a competing source of truth and does not preclude a relational runtime repository. Selecting the database product, repository schema pattern, migration mechanism, and executable DDL belongs to a later refinement.

## 5. Core Package

### `IdentifiedElement` (abstract)

- `identifier: String [1]` — stable identity within the catalog
- `name: String [1]`
- `definition: String [1]`

### `RefinementArtifact` (abstract) extends `IdentifiedElement`

- `lineageIdentifier: String [1]`
- `revisionIdentifier: String [1]`
- `status: ArtifactStatus [1]`
- `supersedes: RefinementArtifact [0..*] {unique}`

A revisioned unit that can participate as the source or target of refinement. `identifier` identifies the particular catalog object; `lineageIdentifier` connects revisions of the same evolving artifact. Revisions remain distinct catalog objects, and supersession does not mutate historical content.

### `ArtifactStatus` enumeration

- `draft`
- `accepted`
- `superseded`
- `retired`

### `RealizableElement` (abstract) extends `IdentifiedElement`

An element that can participate in explicit many-to-many realization. `ModelElement` and `DeploymentArtifact` are its concrete families.

### `ExpressionSpecification` (DataType)

- `language: String [1]`
- `body: String [1]`
- `scope: ExpressionScope [1]`
- `nonOclRationale: String [0..1]`

An expression declares its governing language and evaluation plane. `nonOclRationale` is required when OCL could reasonably have been expected but cannot express the required semantics.

### `ExpressionScope` enumeration

- `definitionModel` — evaluates the structure of a model against this definition
- `subjectData` — evaluates occurrences described by a particular conceptual or logical model
- `physicalTarget` — uses syntax and semantics owned by the named physical target
- `external` — depends on state not represented in the model

### `DataDomain` extends `IdentifiedElement`

- owns `semanticElements: SemanticElement [0..*]`
- `imports: DataDomain [0..*] {unique}`

A bounded area of business meaning and responsibility in which data models and shared semantic definitions are interpreted.

### `DataModel` (abstract) extends `RefinementArtifact`

- `domain: DataDomain [1]`
- owns `elements: ModelElement [0..*]`
- `purpose: String [1]`
- `scope: String [1]`

### Model subclasses

- `ConceptualDataModel` extends `DataModel`
- `LogicalDataModel` extends `DataModel`
- `RelationalLogicalDataModel` extends `LogicalDataModel`

`PhysicalDataModel` is declared in section 10 because its properties belong to the Physical package. The subclass is the single authority for abstraction. There is no separately editable `level` property.

### `ModelElement` (abstract) extends `RealizableElement`

- `model: DataModel [1]`, opposite `DataModel::elements`

## 6. Semantics Package

This package adopts the ISO/IEC 11179-31 distinctions identified in section 2. Exact multiplicities remain subject to normative-text verification.

### `SemanticElement` (abstract) extends `IdentifiedElement`

- `domain: DataDomain [1]`, opposite `DataDomain::semanticElements`

### `ObjectClass` extends `SemanticElement`

A set of ideas, abstractions, or things about which data is recorded.

### `PropertyConcept` extends `SemanticElement`

A characteristic that can be applied to an object class.

### `DataElementConcept` extends `SemanticElement`

- `objectClass: ObjectClass [1]`
- `property: PropertyConcept [1]`
- `conceptualDomain: ConceptualDomain [1]`

Meaning formed by applying a property to an object class, independently of representation.

### `ConceptualDomain` extends `SemanticElement`

The domain of possible meanings associated with a data-element concept.

### `ValueDomain` extends `SemanticElement`

- `conceptualDomain: ConceptualDomain [1]`
- `logicalDatatype: LogicalDatatype [1]`
- `unitOfMeasure: String [0..1]`

A permitted representation of values in a conceptual domain.

### `DataElement` extends `SemanticElement`

- `concept: DataElementConcept [1]`
- `valueDomain: ValueDomain [1]`

The binding of data meaning to a permitted value representation.

## 7. Conceptual Package

This package combines the DAMA 2010 conceptual abstraction with the overlapping IDEF1X entity, relationship, end, and cardinality semantics assigned in section 2. The mapping must be verified construct by construct before IDEF1X conformance is claimed.

### `BusinessEntityType` extends `ModelElement`

- `objectClass: ObjectClass [1]`
- `properties: BusinessProperty [0..*] {derived from BusinessProperty::subject}`

A business-significant kind of thing about which the domain needs to retain information. It denotes a type, not a particular business object.

### `BusinessProperty` extends `ModelElement`

- `subject: ModelElement [1]`
- `concept: DataElementConcept [1]`

A business-significant characteristic of a `BusinessEntityType` or `BusinessRelationship`. It does not specify a column or implementation datatype.

### `BusinessRelationship` extends `ModelElement`

- owns `ends: BusinessRelationshipEnd [2..*]`
- `objectClass: ObjectClass [0..1]`
- `properties: BusinessProperty [0..*] {derived from BusinessProperty::subject}`

A business association among two or more entity types. It is reified so it can be n-ary and can carry its own meaning or properties.

### `BusinessRelationshipEnd` extends `IdentifiedElement`

- `relationship: BusinessRelationship [1]`
- `entityType: BusinessEntityType [1]`
- `minimumCardinality: Integer [1]`
- `maximumCardinality: UnlimitedNatural [1]`

### `BusinessConstraint` extends `ModelElement`

- `specification: ExpressionSpecification [1]`
- `constrainedElements: ModelElement [1..*]`

A business rule that limits valid states or events in the modeled domain. It uses OCL with `scope = subjectData` when the required facts and state are represented by the model. External or unmodeled temporal dependencies require an explicit exception rationale.

## 8. Logical Package

### `LogicalDatatype` (abstract) extends `SemanticElement`

A technology-neutral datatype using the ISO/IEC 11404 distinction between conceptual, structural, and implementation datatype notions. The exact standard type inventory remains pending.

### `LogicalScalarDatatype` extends `LogicalDatatype`

A scalar value category such as text, number, boolean, date/time, or identifier, independent of a target declaration.

### `LogicalRecordDatatype` extends `LogicalDatatype`

- owns `fields: LogicalField [1..*]`

### `LogicalField` extends `IdentifiedElement`

- `record: LogicalRecordDatatype [1]`
- `dataElement: DataElement [1]`
- `required: Boolean [1]`

### `LogicalCollectionDatatype` extends `LogicalDatatype`

- `elementType: LogicalDatatype [1]`
- `ordered: Boolean [1]`
- `unique: Boolean [1]`

### `LogicalMapDatatype` extends `LogicalDatatype`

- `keyType: LogicalDatatype [1]`
- `valueType: LogicalDatatype [1]`

### `LogicalChoiceDatatype` extends `LogicalDatatype`

- `alternatives: LogicalDatatype [2..*] {ordered, unique}`

### `LogicalOpaqueDatatype` extends `LogicalDatatype`

- `mediaType: String [0..1]`

An opaque value whose internal content is not structurally modeled at the logical level. Its surrounding entity and metadata remain modelable; opacity is explicit rather than treated as missing tabular structure.

These structural datatypes allow logical models to express nested records, repeated values, dictionaries, alternatives, and opaque content without importing JSON Schema, XML Schema, API, or storage-product vocabulary. Recursive structures are permitted through datatype references and require cycle-safe validation and serialization.

### `LogicalEntityType` extends `ModelElement`

- `objectClass: ObjectClass [1]`
- `attributes: LogicalAttribute [1..*] {derived from LogicalAttribute::entityType}`
- `identifiers: LogicalIdentifier [1..*] {derived from LogicalIdentifier::entityType}`

A normalized or otherwise purposefully structured logical representation of data, independent of a database product.

### `LogicalAttribute` extends `ModelElement`

- `entityType: LogicalEntityType [1]`
- `dataElement: DataElement [1]`
- `required: Boolean [1]`

### `LogicalIdentifier` extends `ModelElement`

- `entityType: LogicalEntityType [1]`
- `attributes: LogicalAttribute [1..*] {ordered, unique}`
- `preferred: Boolean [1]`

A set of logical attributes whose values identify an occurrence of a logical entity type. It is not a physical primary-key constraint.

### `LogicalRelationship` extends `ModelElement`

- owns `ends: LogicalRelationshipEnd [2..*]`

### `LogicalRelationshipEnd` extends `IdentifiedElement`

- `relationship: LogicalRelationship [1]`
- `entityType: LogicalEntityType [1]`
- `minimumCardinality: Integer [1]`
- `maximumCardinality: UnlimitedNatural [1]`

### `LogicalConstraint` extends `ModelElement`

- `specification: ExpressionSpecification [1]`
- `constrainedElements: ModelElement [1..*]`

A technology-neutral integrity condition not completely represented by identity, optionality, or relationship cardinality.

## 9. Relational Package

This package expresses relational-logical structure independently of a database product. DAMA 2010 governs the abstraction; IDEF1X governs overlapping schema semantics after normative verification. Physical SQL constructs remain in section 10.

### `Relation` extends `ModelElement`

- `attributes: RelationAttribute [1..*] {derived from RelationAttribute::relation}`
- `candidateKeys: CandidateKey [1..*] {derived from CandidateKey::relation}`
- `foreignKeys: RelationalForeignKey [0..*] {derived from RelationalForeignKey::relation}`

A logical relation schema. Its possible values are relations; duplicate tuples are not part of its logical semantics.

### `RelationAttribute` extends `ModelElement`

- `relation: Relation [1]`
- `dataElement: DataElement [1]`
- `required: Boolean [1]`

### `CandidateKey` extends `ModelElement`

- `relation: Relation [1]`
- `attributes: RelationAttribute [1..*] {ordered, unique}`
- `preferred: Boolean [1]`

### `RelationalForeignKey` extends `ModelElement`

- `relation: Relation [1]`
- `referencedKey: CandidateKey [1]`
- owns `attributeMappings: RelationAttributeMapping [1..*] {ordered}`

### `RelationAttributeMapping` extends `IdentifiedElement`

- `foreignKey: RelationalForeignKey [1]`
- `referencingAttribute: RelationAttribute [1]`
- `referencedAttribute: RelationAttribute [1]`

## 10. Physical Package

This package describes technology-specific data designs and observations. Its core is not relational: relational databases, document and other NoSQL stores, APIs, schema documents, and stored structured, semi-structured, or unstructured assets are physical profiles of the same language.

Portable typed classes are used where semantics are stable across targets. A named metadata profile supplies native element kinds, properties, and links where a standard or product exposes additional metadata. Consequently, “complete physical metadata” is a testable claim only for a stated target, version, profile, and source inventory; it is not a claim that one fixed class list contains every present and future platform feature.

### `PhysicalDataModel` extends `DataModel`

- `target: PhysicalTarget [1]`
- `role: PhysicalModelRole [1]`
- `environment: DeploymentEnvironment [0..1]`

### `PhysicalModelRole` enumeration

- `design` — intended target-specific structure
- `observed` — point-in-time description collected from an environment

### `PhysicalTarget` extends `IdentifiedElement`

- `product: String [1]`
- `version: String [1]`
- `technologyFamily: String [1]`
- owns `datatypes: PhysicalDatatype [0..*]`
- owns `metadataProfiles: PhysicalMetadataProfile [1..*]`

The platform, protocol, format, or storage technology and version against which physical meaning is interpreted.

### `DeploymentEnvironment` extends `IdentifiedElement`

- `target: PhysicalTarget [1]`
- `locator: String [1]`
- `environmentKind: String [1]`

### `PhysicalMetadataProfile` extends `IdentifiedElement`

- `target: PhysicalTarget [1]`, opposite `PhysicalTarget::metadataProfiles`
- `authority: String [1]`
- `authorityVersion: String [1]`
- `coverageScope: String [1]`
- `sourceInventoryReference: String [1]`
- owns `elementKinds: NativeElementKindDefinition [0..*]`
- owns `propertyDefinitions: NativePropertyDefinition [0..*]`
- owns `relationshipKinds: NativeRelationshipKindDefinition [0..*]`

A versioned interpretation profile for a standard, vendor catalog, API-description language, schema language, or storage service. `sourceInventoryReference` identifies the authoritative metadata surface against which coverage can be checked.

### `NativeElementKindDefinition` extends `IdentifiedElement`

- `profile: PhysicalMetadataProfile [1]`
- `nativeName: String [1]`
- `portableBaseType: String [0..1]`

### `NativePropertyDefinition` extends `IdentifiedElement`

- `profile: PhysicalMetadataProfile [1]`
- `appliesTo: NativeElementKindDefinition [1]`
- `nativeName: String [1]`
- `valueType: String [1]`
- `sourcePath: String [1]`

### `NativeRelationshipKindDefinition` extends `IdentifiedElement`

- `profile: PhysicalMetadataProfile [1]`
- `nativeName: String [1]`
- `sourceKind: NativeElementKindDefinition [1]`
- `targetKind: NativeElementKindDefinition [1]`

### `PhysicalElement` (abstract) extends `ModelElement`

- `physicalName: String [1]`
- `qualifiedName: String [1]`
- `nativeKind: NativeElementKindDefinition [0..1]`
- owns `metadataValues: NativeMetadataValue [0..*]`

### `NativeMetadataValue` extends `IdentifiedElement`

- `element: PhysicalElement [1]`
- `definition: NativePropertyDefinition [1]`
- `lexicalValue: String [1]`
- `datatypeName: String [1]`

The lexical value preserves the target's representation. Its profile definition supplies the source path and semantics; consumers must not infer meaning from the property name alone.

### `NativePhysicalElement` extends `PhysicalElement`

- `container: PhysicalElement [0..1]`

Represents a target-native metadata object for which the portable physical vocabulary has no honest equivalent.

### `NativeMetadataRelationship` extends `PhysicalElement`

- `kind: NativeRelationshipKindDefinition [1]`
- `source: PhysicalElement [1]`
- `target: PhysicalElement [1]`

### `PhysicalContainer` (abstract) extends `PhysicalElement`

- `parent: PhysicalContainer [0..1]`

### `PhysicalDataAsset` (abstract) extends `PhysicalElement`

- `container: PhysicalContainer [0..1]`
- `location: String [0..1]`
- `mediaType: String [0..1]`
- `format: String [0..1]`
- `shape: DataShape [0..1]`

A resource that exposes or stores data. Its content may be structured, semi-structured, or unstructured; absence of a data shape is meaningful and does not imply tabular structure.

### `DataShape` extends `PhysicalElement`

- `language: String [1]`
- `languageVersion: String [1]`
- `nodes: ShapeNode [1..*] {derived from ShapeNode::shape}`

### `ShapeNode` extends `PhysicalElement`

- `shape: DataShape [1]`
- `parent: ShapeNode [0..1]`
- `path: String [1]`
- `nodeKind: String [1]`
- `datatype: PhysicalDatatype [0..1]`
- `minimumOccurrences: Integer [1]`
- `maximumOccurrences: UnlimitedNatural [1]`
- owns `constraints: ExpressionSpecification [0..*]`

`DataShape` and `ShapeNode` provide common navigation across JSON Schema, XML Schema, API messages, and inferred document/file structures. Their native metadata profile remains authoritative for keywords and semantics that the shared shape does not preserve directly.

### Relational physical profile

The relational profile adopts ISO/IEC 9075-2 for portable SQL structures and ISO/IEC 9075-11 for information and definition metadata. A product profile adds every vendor catalog kind, property, relationship, access structure, storage option, statistic, privilege, and operational fact in its declared coverage scope.

### `DatabaseCatalog` extends `PhysicalContainer`

### `DatabaseNamespace` extends `PhysicalContainer`

- `catalog: DatabaseCatalog [0..1]`
- `tabularObjects: PhysicalTabularObject [0..*] {derived from PhysicalTabularObject::container}`

### `PhysicalTabularObject` (abstract) extends `PhysicalDataAsset`

- `columns: Column [1..*] {derived from Column::tabularObject}`

Its `container` is a `DatabaseNamespace`.

### `Table` extends `PhysicalTabularObject`

- `constraints: TableConstraint [0..*] {derived from TableConstraint::table}`
- `indexes: Index [0..*] {derived from Index::table}`

### `View` extends `PhysicalTabularObject`

- `definition: ExpressionSpecification [1]`

### `MaterializedView` extends `PhysicalTabularObject`

- `definition: ExpressionSpecification [1]`
- `refreshSpecification: ExpressionSpecification [0..1]`

### `PhysicalDatatype` extends `IdentifiedElement`

- `target: PhysicalTarget [1]`, opposite `PhysicalTarget::datatypes`
- `declaration: String [1]`

### `Column` extends `PhysicalElement`

- `tabularObject: PhysicalTabularObject [1]`
- `datatype: PhysicalDatatype [1]`
- `nullable: Boolean [1]`
- `default: ExpressionSpecification [0..1]`

### `TableConstraint` (abstract) extends `PhysicalElement`

- `table: Table [1]`

### `PrimaryKeyConstraint` extends `TableConstraint`

- `columns: Column [1..*] {ordered, unique}`

### `UniqueConstraint` extends `TableConstraint`

- `columns: Column [1..*] {ordered, unique}`

### `ForeignKeyConstraint` extends `TableConstraint`

- `referencedKey: TableConstraint [1]`
- owns `columnMappings: ForeignKeyColumnMapping [1..*] {ordered}`

The referenced constraint must be a primary-key or unique constraint.

### `ForeignKeyColumnMapping` extends `IdentifiedElement`

- `foreignKey: ForeignKeyConstraint [1]`
- `referencingColumn: Column [1]`
- `referencedColumn: Column [1]`

### `CheckConstraint` extends `TableConstraint`

- `specification: ExpressionSpecification [1]`

### `Index` extends `PhysicalElement`

- `table: Table [1]`
- `unique: Boolean [1]`
- owns `keyParts: IndexKeyPart [1..*] {ordered}`

An index is an access structure. `unique = true` describes the index behavior in the target platform; it does not replace a `UniqueConstraint` or `PrimaryKeyConstraint` as the authority for logical integrity.

### `IndexKeyPart` extends `IdentifiedElement`

- `index: Index [1]`
- `column: Column [1]`
- `direction: SortDirection [1]`

### `SortDirection` enumeration

- `ascending`
- `descending`

### `Sequence`, `Routine`, `RoutineParameter`, `Trigger`, and `Partition`

These are concrete `PhysicalElement` classes in the relational profile. Their portable properties and exact containment remain pending ISO SQL normative-text verification. Target-only metadata attaches through the active metadata profile rather than being discarded or falsely standardized.

### Document and NoSQL physical profiles

The following are concrete `PhysicalDataAsset` classes:

- `DocumentCollection`
- `KeyValueCollection`
- `ColumnFamily`
- `GraphStore`

They use `DataShape` when a declared or inferred structure is available. Keys, partitioning, indexes, consistency settings, graph labels, edge kinds, validation rules, and other target features are represented by typed constructs when standardized here and otherwise by the named metadata profile. “NoSQL” is not treated as one data model.

### Schema-document physical profile

### `SchemaDocument` extends `PhysicalDataAsset`

- `schemaLanguage: String [1]`
- `schemaVersion: String [1]`
- `documentReference: String [1]`

JSON Schema and XML Schema documents are first-class physical artifacts. Their definitions and references can be retained natively while a `DataShape` provides common cross-technology navigation. Other schema languages may use the same boundary through their own profiles.

### API physical profile

### `ApiService` extends `PhysicalContainer`

- `baseAddress: String [1]`
- `operations: ApiOperation [0..*] {derived from ApiOperation::service}`

### `InterfaceDescription` extends `PhysicalDataAsset`

- `service: ApiService [1]`, redefines `PhysicalDataAsset::container`
- `descriptionLanguage: String [1]`
- `descriptionVersion: String [1]`
- `documentReference: String [1]`

### `ApiOperation` extends `PhysicalDataAsset`

- `service: ApiService [1]`, redefines `PhysicalDataAsset::container`
- `method: String [1]`
- `pathTemplate: String [1]`
- `messages: ApiMessage [0..*] {derived from ApiMessage::operation}`

### `ApiMessage` extends `PhysicalElement`

- `operation: ApiOperation [1]`
- `direction: MessageDirection [1]`
- `statusCode: String [0..1]`
- `mediaType: String [1]`
- `shape: DataShape [0..1]`

### `MessageDirection` enumeration

- `request`
- `response`
- `event`

OpenAPI is the first aligned HTTP API profile. Other interface-description or event-schema languages can be added as named profiles without changing conceptual or logical constructs.

### Stored-asset physical profile

### `StoredAssetCollection` extends `PhysicalDataAsset`

- `storageKind: String [1]`
- `contentKind: ContentKind [1]`
- `compression: String [0..1]`
- `encoding: String [0..1]`

### `ContentKind` enumeration

- `structured`
- `semiStructured`
- `unstructured`

This class covers collections in file, object, blob, or block-backed storage. A structured or semi-structured collection may reference a declared or inferred `DataShape`. An unstructured collection is described through location, media type, format, operational metadata, and any separately modeled metadata shape; the language does not invent structure in the content itself.

## 11. Deployment Package

Deployment is not another model abstraction. It packages target-owned material produced from an intended physical design and records attempts to apply that material to an environment.

### `DeploymentPackage` extends `RefinementArtifact`

- `sourceModel: PhysicalDataModel [1]`
- `targetEnvironment: DeploymentEnvironment [1]`
- owns `artifacts: DeploymentArtifact [1..*]`

### `DeploymentArtifact` extends `RealizableElement`

- `package: DeploymentPackage [1]`, opposite `DeploymentPackage::artifacts`
- `artifactKind: String [1]`
- `language: String [1]`
- `contentReference: String [1]`
- `contentDigest: String [1]`

An executable or publishable artifact such as DDL, a migration, a JSON or XML schema, an OpenAPI description, a storage definition, or target configuration. The content remains target-owned syntax and is related explicitly to the physical design elements it realizes.

### `DeploymentRecord` extends `IdentifiedElement`

- `package: DeploymentPackage [1]`
- `environment: DeploymentEnvironment [1]`
- `attemptedAt: String [1]`
- `status: DeploymentStatus [1]`
- `executionReference: String [1]`

### `DeploymentStatus` enumeration

- `planned`
- `running`
- `succeeded`
- `failed`
- `rolledBack`

## 12. Observation Package

Observation records external state without granting it design authority. An introspection, schema import, API-description import, or storage inventory produces a new `PhysicalDataModel` with `role = observed` and collection provenance.

### `ObservationRecord` extends `IdentifiedElement`

- `observedModel: PhysicalDataModel [1]`
- `environment: DeploymentEnvironment [1]`
- `capturedAt: String [1]`
- `collector: String [1]`
- `collectorVersion: String [1]`
- `sourceReference: String [1]`
- `evidenceDigest: String [1]`

The record describes how external state was collected. It establishes provenance for the observation but does not assert completeness; that is the separate responsibility of a metadata coverage assessment.

### `MetadataCoverageAssessment` extends `IdentifiedElement`

- `observedModel: PhysicalDataModel [1]`
- `profile: PhysicalMetadataProfile [1]`
- `assessedAt: String [1]`
- `status: CoverageStatus [1]`
- `uncoveredItems: String [0..*]`
- `evidenceReference: String [1]`

### `CoverageStatus` enumeration

- `complete`
- `incomplete`
- `unknown`

`complete` means complete only for the profile's declared `coverageScope` and `sourceInventoryReference`. It requires evidence that every metadata kind, property, and relationship in that inventory is represented by a portable construct or native profile definition and that collection accounts for every accessible value in scope.

### `PhysicalComparison` extends `IdentifiedElement`

- `expectedModel: PhysicalDataModel [1]`
- `observedModel: PhysicalDataModel [1]`
- `assessedAt: String [1]`
- owns `differences: PhysicalDifference [0..*]`

### `PhysicalDifference` extends `IdentifiedElement`

- `comparison: PhysicalComparison [1]`
- `kind: DifferenceKind [1]`
- `expectedElements: PhysicalElement [0..*] {unique}`
- `observedElements: PhysicalElement [0..*] {unique}`
- `disposition: DifferenceDisposition [1]`
- `rationale: String [0..1]`
- `resolutionReference: String [0..1]`

### `DifferenceKind` enumeration

- `equivalent`
- `missing`
- `unexpected`
- `changed`
- `unresolved`

### `DifferenceDisposition` enumeration

- `pending`
- `acceptIntoDesign`
- `correctDeployment`
- `ignoreWithRationale`
- `resolved`

An accepted production difference does not mutate the old design. It triggers a new revision beginning at the earliest artifact that owns the intended change, followed by new realizations and deployment material.

## 13. Realization Package

This package must remain mappable to the model and mapping registration concepts of ISO/IEC 11179-35 and ISO/IEC 19763-12. Its many-to-many disposition and coverage semantics are project extensions, not claims that either registration standard defines realization this way.

### `RealizationSet` extends `IdentifiedElement`

- `sourceArtifact: RefinementArtifact [1]`
- `targetArtifact: RefinementArtifact [1]`
- owns `realizations: Realization [1..*]`

### `Realization` extends `IdentifiedElement`

- `disposition: RealizationDisposition [1]`
- `sourceElements: RealizableElement [0..*] {unique}`
- `targetElements: RealizableElement [0..*] {unique}`
- `rationale: String [0..1]`
- `transformationReference: String [0..1]`

`transformationReference` identifies a transformation specification or human procedure. It is not an OCL body. A later transformation definition may use OCL for its queries, guards, and pre/postconditions while using an appropriate transformation language for target creation.

### `RealizationDisposition` enumeration

- `realized` — source meaning is represented by one or more target elements
- `introduced` — target detail is introduced at this abstraction
- `omitted` — source meaning is deliberately not represented in the target

`Realization` is a class rather than a CMOF association because the correspondence is many-to-many and has disposition, rationale, and rule semantics of its own. A realization graph may branch, converge, or skip a conventional stage, but it must remain acyclic.

## 14. Well-Formedness Rules

The rules below are normative prose in this draft. Their machine-readable form shall use ISO/IEC 19507:2012 OCL 2.3.1 wherever the required state is modeled and shall be equivalent to the prose before the layer can become effective. Every exception is identified below rather than left implicit.

### Cross-model rules

- `DM-001`: Every `ModelElement` is owned by exactly one `DataModel`.
- `DM-002`: A model owns only model elements permitted by its exact model kind and references semantic elements only from its domain or imported domains.
- `DM-003`: A physical model has exactly one named `PhysicalTarget` with at least one metadata profile.
- `DM-004`: A conceptual or logical model contains no `PhysicalElement`, `PhysicalDatatype`, or `Index`.
- `DM-005`: Definitions and names are non-empty; model-element identifiers are unique within their containing model and semantic-element identifiers within their domain.
- `DM-006`: Every expression specification has a non-empty language and body and declares exactly one evaluation scope.
- `DM-007`: Every `DM-*` constraint and derived property whose required state is represented in the definition model is expressed in OCL with `scope = definitionModel` in the machine-readable definition. A rule requiring comparison with an external metadata inventory identifies the validation procedure and evidence instead of claiming false OCL executability.
- `DM-008`: A non-OCL expression either occupies syntax intrinsically owned by a physical target or supplies a non-empty `nonOclRationale`.
- `DM-009`: Refinement-artifact revision identifiers are unique within a lineage; every superseded revision has the same lineage identifier, while each revision retains a unique catalog-object identifier. `supersedes` and realization relationships are acyclic and never mutate superseded content.

### Conceptual and logical rules

- `DM-101`: A business or logical relationship has at least two ends, and each end refers to an entity type in the same model.
- `DM-102`: End cardinality has a non-negative minimum and a maximum not less than its minimum.
- `DM-103`: Every logical identifier uses attributes assigned to its identified entity type.
- `DM-104`: Every logical entity type has at least one identifier, and at most one is preferred.
- `DM-105`: A value domain and its data-element concept refer to the same conceptual domain, and every referenced semantic element belongs to the data model's domain or a directly or transitively imported domain.
- `DM-106`: A business property's subject is a business entity type or business relationship in the same conceptual model.
- `DM-107`: A business entity type's properties use data-element concepts for its object class. A relationship with properties names an object class, and its properties use concepts for that object class.
- `DM-108`: A logical attribute's data-element concept uses the object class named by its logical entity type.
- `DM-109`: A business or logical constraint uses OCL with `scope = subjectData` when its required state is modeled. Its context and referenced properties resolve through the subject model's defined OCL evaluation environment; otherwise it records why OCL is insufficient.
- `DM-110`: A logical record has uniquely named fields; a collection has one element type; a map has one key and value type; a choice has at least two distinct alternatives; and recursive datatype graphs are explicit and serializable without infinite containment.

### Relational rules

- `DM-201`: Relation attribute names are unique within a relation.
- `DM-202`: Every candidate-key attribute belongs to its key's relation; at most one candidate key is preferred.
- `DM-203`: A relational foreign key's referencing attributes belong to its relation.
- `DM-204`: A relational foreign key maps once, in order, to every attribute of its referenced candidate key.
- `DM-205`: Mapped relation attributes have compatible value domains.

### Physical rules

- `DM-301`: Qualified physical names are unique among like-kind elements in the naming scope defined by the active target profile.
- `DM-302`: Every contained physical element belongs to a valid container in the same physical model; every relational tabular object belongs to a database namespace and every column to its tabular object.
- `DM-303`: Every constraint column belongs to the constraint's table.
- `DM-304`: A table has at most one primary-key constraint.
- `DM-305`: A foreign key references a primary-key or unique constraint and maps once, in order, to every referenced column.
- `DM-306`: Referencing and referenced columns have target-compatible physical datatypes, and every physical datatype belongs to the physical model's target.
- `DM-307`: Every index key column belongs to the indexed table; an index contains no duplicate key column.
- `DM-308`: A view has a non-empty definition expression.
- `DM-309`: A unique index does not satisfy a required logical uniqueness realization unless a corresponding primary-key or unique constraint is also modeled.
- `DM-310`: A view definition, column default, or physical check constraint has `scope = physicalTarget` and names the expression language or dialect governed by its physical target.
- `DM-311`: When a physical expression implements an upstream business or logical constraint, their realization record identifies that correspondence; target syntax does not silently replace upstream meaning.
- `DM-312`: Every native kind, property, relationship, and value resolves to a definition in a metadata profile owned by the physical model's target; its source and target element kinds conform to that definition.
- `DM-313`: An observed physical model names exactly one deployment environment and observation record, and both identify the same model and environment. A design physical model has neither an observation record nor a claim about observed state.
- `DM-314`: A portable typed property and a native metadata value describing the same target fact have one declared authority and do not silently carry contradictory values.
- `DM-315`: Every data-shape node belongs to its shape and physical model, has a unique path within that shape, and has a non-negative minimum and maximum not less than its minimum.
- `DM-316`: A schema document and interface description identify their exact language and version. API messages and structured or semi-structured assets reference only shapes in the same model; cross-model reuse is represented by realizing a local shape from the external shape rather than by an untracked reference.
- `DM-317`: An unstructured stored-asset collection may have a metadata shape but must not claim a content shape unless that structure is evidenced.
- `DM-318`: A metadata coverage assessment may be `complete` only when `uncoveredItems` is empty and its evidence checks the exact target, profile version, coverage scope, source inventory, access limitations, and collection result. The external inventory comparison is a validation procedure rather than an OCL-only claim.

### Deployment and observation rules

- `DM-501`: A deployment package's source is a physical design model for the same target as its environment, and every deployment artifact is covered by a realization from that design or has an introduced rationale.
- `DM-502`: Every deployment artifact identifies target-owned language, content reference, and integrity digest; a deployment record identifies the exact immutable package revision attempted.
- `DM-503`: A successful deployment record is evidence that execution reported success, not proof that observed state equals intended state.
- `DM-601`: A physical comparison uses a design model as expected state and an observed model as actual state for compatible targets and the same deployment environment.
- `DM-602`: Every expected and observed physical element in the comparison scope is covered by an `equivalent`, `missing`, `unexpected`, `changed`, or `unresolved` difference record.
- `DM-603`: `acceptIntoDesign` requires a resolution reference to a new revision at the earliest artifact that owns the accepted meaning; `ignoreWithRationale` requires a rationale.

### Realization rules

- `DM-401`: A realization set's source and target are distinct artifact revisions, and adding the edge from source to target does not create a cycle. The transform or human decision states why the target is more concrete for its purpose; no fixed universal stage sequence is assumed.
- `DM-402`: `realized` has at least one source and one target; `introduced` has no source and at least one target; `omitted` has at least one source and no target.
- `DM-403`: Every source element belongs to the realization set's source artifact and every target element belongs to its target artifact.
- `DM-404`: Introduced and omitted realizations require a rationale.
- `DM-405`: Every target element is covered by a realized or introduced record, and every source element is covered by a realized or omitted record.
- `DM-406`: Realization never transfers identity implicitly; each model or deployment element retains its own identifier and correspondence remains explicit.
- `DM-407`: A transformation reference identifies a transformation or human procedure rather than containing an OCL mutation body. OCL may specify its model queries, guards, and pre/postconditions.

## 15. Definition Boundary

This layer owns the vocabulary and well-formedness needed to describe conceptual, logical, heterogeneous physical, deployment, and observed data artifacts. It also owns the semantic requirements that make a lossless relational repository realization possible.

It defines what an import, deployment, observation, coverage assessment, and maintenance comparison must represent. It does not yet define the software behavior or executable mechanisms that perform them:

- modeling workflow, approval, collaboration, or user roles;
- diagnostics or validator behavior;
- automatic conceptual-to-logical or logical-to-physical generation;
- database, API, schema, or storage introspection connectors and readback algorithms;
- external rule languages, target expression grammars, and transformation languages beyond the adopted OCL usage profile;
- the concrete relational repository schema, database product, migration mechanism, runtime API, or operational topology;
- a product API or user interface; or
- exhaustive portable classes for every vendor option when the option is more honestly preserved through a named metadata profile.

Those are decisions for later refinements after this language and its governing CMOF choice are accepted. A later implementation may specialize the language, but it may not narrow the supported subject technologies to relational databases or discard target-native metadata without revising this layer explicitly.

## 16. Verification State

The standards are part of this language definition now; the outstanding work is verification, not selection by implication.

- CMOF is the presumed governing model pending the follow-up ADR and executable production-constraint validation.
- OCL 2.3.1 is the default wherever its side-effect-free model semantics apply; equivalent encodings of the `DM-*` rules and derived properties remain to be written.
- The definition-model and subject-data OCL evaluation environments remain to be specified and validated separately.
- ISO/IEC 11179-31 concepts are adopted, while exact inheritance, role names, and multiplicities await normative-text checking.
- IDEF1X compatibility is required for overlapping constructs, while its conceptual-schema terminology must be mapped rather than copied onto DAMA model levels.
- ISO/IEC 11404 governs datatype separation, while the standard type catalogue and datatype mappings remain incomplete.
- ISO/IEC 9075-2 governs the portable physical SQL subset, while detailed construct mapping remains incomplete.
- ISO/IEC 9075-11 governs the portable relational metadata baseline, while a target/version coverage inventory and vendor-catalog mappings remain to be demonstrated.
- JSON Schema 2020-12, XML Schema 1.1, and OpenAPI 3.2.0 alignment mappings remain to be constructed and tested with representative recursive, polymorphic, and referenced schemas.
- DCAT 3 and PROV-DM alignment is selected for catalog interchange and provenance boundaries, but no conformance claim is made.
- Document, key-value, wide-column, graph, schema-document, API, and stored-asset profiles are structural commitments whose exact portable inventories remain incomplete.
- A complete-metadata claim must be demonstrated independently for each target, version, profile, coverage scope, and accessible source inventory; no universal completeness claim is made.
- ISO/IEC 11179-35 and ISO/IEC 19763-12 mappings remain to be demonstrated.
- The OMG MOF 2.5.1 to ISO/IEC 19508:2014 version delta has not been assessed, so ISO MOF conformance is not claimed.
- ISO/IEC 19509 XMI output has not been produced, so representation conformance is not claimed; XMI is a validation/interchange form rather than the selected runtime repository.
- The required relational repository realization has not been designed or round-trip tested. Its future acceptance requires reconstructing the CMOF definition and representative instances without semantic loss.
- DAMA alignment remains a hypothesis until checked against exact pages in the user's 2010 edition.
- Realization coverage rules, optional relational-logical refinement, relation/table separation, lifecycle artifacts, and heterogeneous physical profiles are project composition decisions subject to product-owner review.
