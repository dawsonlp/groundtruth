# Data-Modeling Language Definition

## Document Status

- Status: draft
- Effective: no
- Governing model: CMOF 2.5.1, presumed pending the follow-up ADR
- Standards profile: incorporated in section 2
- DAMA verification baseline: user's 2010 DAMA-DMBOK edition
- DAMA page verification: pending
- ISO normative-text verification: pending where identified below
- Machine-readable CMOF validation: pending

This artifact defines the modeling language for the first application of Domain Catalog. It is intended to become a CMOF-conforming model that acts as the governing model for particular data models. It is not a product requirements document, validator design, database schema, or user-interface design.

## 1. Governing Relationships

```text
CMOF 2.5.1
    governs the valid form of
this data-modeling language definition
    governs the valid form of
particular conceptual, logical, relational-logical, and physical data models
```

`Conforms to` means that a model uses permitted element types and satisfies this definition's rules. It does not mean that the model was generated from its governing model.

`Realizes` relates a more concrete model to meaning in an upstream model. Realization does not imply equivalence, automation, or absence of added decisions.

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
| [ISO/IEC 11179-35:2023](https://www.iso.org/standard/81727.html) | Alignment required | Registration of models, metamodels, concepts, and mappings | Does not define the models' internal semantics or physical instantiation |
| [ISO/IEC 19763-12:2015 with Amendment 1:2023](https://www.iso.org/standard/61559.html) | Alignment required | Registration of information-requirement and database-structure models | A registry metamodel, not the data-modeling language |
| [ISO/IEC 19509:2014, XMI](https://www.iso.org/standard/61845.html) | Selected validation representation; production pending | The XMI 2.4.2 representation referenced by MOF 2.5.1 | Does not select product persistence or require XMI as the eventual runtime interchange format |
| [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1) and [ISO/IEC 19505-1:2012](https://www.iso.org/standard/32624.html) | Alignment required for notation and interchange; version delta pending | Shared structural kernel and standard class-diagram presentation | A data model governed here is not thereby a UML model, and the ISO publication predates OMG UML 2.5.1 |
| [OMG CWM 1.1](https://www.omg.org/spec/CWM/1.1) | Informative | Relational, datatype, key/index, expression, transformation, and warehouse-model coverage precedent | Warehouse-oriented, MOF 1.3/XMI 1.1-era, and not imported as this language's metamodel |
| User's 2010 DAMA-DMBOK edition | Verification baseline | Conceptual, logical, and physical abstraction; DAMA nomenclature and practice | Not a formal metamodel or substitute for the standards assigned above |

### 2.1 Precedence and conflict rules

1. A standard governs only the concern assigned to it in the table.
2. CMOF governs whether this definition is a valid metamodel; the adopted data standards govern the meanings expressed by CMOF classes and properties.
3. DAMA 2010 governs the intended data-modeling abstraction and approach. It does not override a formal standard silently; any conflict must be recorded and resolved explicitly.
4. A target-platform specification may specialize the physical package but must preserve portable SQL meaning and identify every extension.
5. OCL is the default for every constraint, derivation, query, guard, or pre/postcondition expressible over modeled state. A non-OCL expression must identify the owning language and either be intrinsic target syntax or state why OCL is insufficient.
6. `Project choice` is used only where the adopted sources leave a gap or where this language deliberately composes them.
7. A pending verification item prevents a detailed conformance claim but does not move the standards decision back into transform evidence.

### 2.2 OCL usage profile

OCL is applied at two distinct evaluation planes:

1. **Definition and model validation.** The OCL context is a CMOF class in this language, such as `LogicalEntityType` or `ForeignKeyConstraint`. These expressions validate whether a particular data model conforms to this definition. All `DM-*` rules and derived navigation properties belong here.
2. **Subject-data validation.** The OCL context is a classifier defined by a particular conceptual or logical model, such as that model's `OrderLine`. These expressions constrain occurrences described by the model. This use is valid only when an OCL evaluation environment maps the model-defined entity types, attributes, relationships, datatypes, and values into OCL classifiers and properties.

OCL may also provide queries, guards, and pre/postconditions to a later transformation language. Because OCL is side-effect free, it does not by itself specify how a target model is created or mutated.

SQL view definitions, column defaults, and check expressions retain the language of their `PhysicalTarget`. OCL can validate their surrounding model and can be the upstream logical constraint they realize, but translating OCL into target SQL is a separate, explicit realization decision.

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
| Relations, relation attributes, candidate keys, and relational foreign keys | DAMA 2010 and IDEF1X where applicable | A relational-logical model is explicitly separate from a physical database model |
| Tables, views, columns, primary/unique/foreign-key/check constraints | ISO/IEC 9075-2 | Physical target and version make implementation semantics explicit |
| Indexes | Target-platform specification; CWM as informative precedent | Core `Index` preserves the distinction between access path and integrity constraint |
| Cross-model realization and registration mapping | ISO/IEC 11179-35 and ISO/IEC 19763-12 alignment | Many-to-many realization, introduction, omission, rationale, and coverage rules are project semantics |

## 3. Abstraction Boundaries

The abstraction belongs to a model. An element belongs to exactly one model and acquires its permitted vocabulary from that model's kind.

| Model kind | Purpose | Includes | Excludes |
| --- | --- | --- | --- |
| `ConceptualDataModel` | State business meaning and scope | Business entity types, business properties, relationships, cardinality, and business constraints | Relations, foreign keys, tables, columns, platform types, indexes |
| `LogicalDataModel` | State technology-neutral data structure and integrity | Logical entity types, attributes, identifiers, value domains, relationships, and logical constraints | Database products, storage objects, platform types, indexes |
| `RelationalLogicalDataModel` | State a logical model using the relational model | Relations, relation attributes, candidate keys, and relational foreign keys | Tables, storage options, platform data types, indexes |
| `PhysicalDataModel` | State realization in a named target environment | Namespaces, tables, views, columns, physical types, integrity constraints, and indexes | Unresolved business meaning or unnamed implementation targets |

A relation and a table are not synonyms. A relation is a logical value with a heading and relational constraints. A table is a physical database object in a target environment. A table may realize one relation, several relations, or part of a relation, and that correspondence is explicit.

## 4. CMOF Representation

The definition consists of CMOF packages named `Core`, `Semantics`, `Conceptual`, `Logical`, `Relational`, `Physical`, and `Realization`.

- Every type below is a CMOF `Class`, `DataType`, or `Enumeration`.
- Every field or role is a CMOF `Property` with the stated multiplicity.
- `owns` denotes a composite CMOF property.
- `extends` denotes CMOF `Generalization`.
- `{derived}` denotes a read-only navigation calculated from the named authoritative reverse reference, not separately stored membership.
- Each rule in section 12 is a CMOF `Constraint` whose specification is an OCL `OpaqueExpression`.
- Every derived property has an OCL derivation in the machine-readable definition.
- Subject-model constraints such as a foreign key are instances of language classes; they are not CMOF constraints governing the form of the language.

This Markdown is a review projection, not the machine-readable CMOF representation required for acceptance.

## 5. Core Package

### `IdentifiedElement` (abstract)

- `identifier: String [1]` — stable identity within the catalog
- `name: String [1]`
- `definition: String [1]`

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

### `DataModel` (abstract) extends `IdentifiedElement`

- `domain: DataDomain [1]`
- owns `elements: ModelElement [0..*]`
- `purpose: String [1]`
- `scope: String [1]`

### Model subclasses

- `ConceptualDataModel` extends `DataModel`
- `LogicalDataModel` extends `DataModel`
- `RelationalLogicalDataModel` extends `LogicalDataModel`
- `PhysicalDataModel` extends `DataModel`
  - owns `target: PhysicalTarget [1]`

The subclass is the single authority for abstraction. There is no separately editable `level` property.

### `ModelElement` (abstract) extends `IdentifiedElement`

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

### `LogicalDatatype` extends `SemanticElement`

A technology-neutral datatype using the ISO/IEC 11404 distinction between conceptual, structural, and implementation datatype notions. The exact standard type inventory remains pending.

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

This package adopts ISO/IEC 9075-2 as the portable SQL baseline for tables, views, columns, datatypes, and integrity constraints. Every target-specific extension is interpreted under the named `PhysicalTarget` rather than attributed to portable SQL.

### `PhysicalTarget` extends `IdentifiedElement`

- `product: String [1]`
- `version: String [1]`
- owns `datatypes: PhysicalDatatype [0..*]`

The platform and version against which physical meaning is interpreted.

### `PhysicalElement` (abstract) extends `ModelElement`

- `physicalName: String [1]`

### `DatabaseNamespace` extends `PhysicalElement`

- `tabularObjects: PhysicalTabularObject [0..*] {derived from PhysicalTabularObject::namespace}`

### `PhysicalTabularObject` (abstract) extends `PhysicalElement`

- `namespace: DatabaseNamespace [1]`
- `columns: Column [1..*] {derived from Column::tabularObject}`

### `Table` extends `PhysicalTabularObject`

- `constraints: TableConstraint [0..*] {derived from TableConstraint::table}`
- `indexes: Index [0..*] {derived from Index::table}`

### `View` extends `PhysicalTabularObject`

- `definition: ExpressionSpecification [1]`

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

Expression indexes, included columns, partitions, file placement, and vendor-specific options are deferred until a physical target requires them.

## 11. Realization Package

This package must remain mappable to the model and mapping registration concepts of ISO/IEC 11179-35 and ISO/IEC 19763-12. Its many-to-many disposition and coverage semantics are project extensions, not claims that either registration standard defines realization this way.

### `RealizationSet` extends `IdentifiedElement`

- `sourceModel: DataModel [1]`
- `targetModel: DataModel [1]`
- owns `realizations: Realization [1..*]`

### `Realization` extends `IdentifiedElement`

- `disposition: RealizationDisposition [1]`
- `sourceElements: ModelElement [0..*] {unique}`
- `targetElements: ModelElement [0..*] {unique}`
- `rationale: String [0..1]`
- `transformationReference: String [0..1]`

`transformationReference` identifies a transformation specification or human procedure. It is not an OCL body. A later transformation definition may use OCL for its queries, guards, and pre/postconditions while using an appropriate transformation language for target creation.

### `RealizationDisposition` enumeration

- `realized` — source meaning is represented by one or more target elements
- `introduced` — target detail is introduced at this abstraction
- `omitted` — source meaning is deliberately not represented in the target

`Realization` is a class rather than a CMOF association because the correspondence is many-to-many and has disposition, rationale, and rule semantics of its own.

## 12. Well-Formedness Rules

The rules below are normative prose in this draft. Their machine-readable form shall use ISO/IEC 19507:2012 OCL 2.3.1 wherever the required state is modeled and shall be equivalent to the prose before the layer can become effective. Every exception is identified below rather than left implicit.

### Cross-model rules

- `DM-001`: Every `ModelElement` is owned by exactly one `DataModel`.
- `DM-002`: A model owns only model elements permitted by its exact model kind and references semantic elements only from its domain or imported domains.
- `DM-003`: A physical model has exactly one named `PhysicalTarget`.
- `DM-004`: A conceptual or logical model contains no `PhysicalElement`, `PhysicalDatatype`, or `Index`.
- `DM-005`: Definitions and names are non-empty; model-element identifiers are unique within their containing model and semantic-element identifiers within their domain.
- `DM-006`: Every expression specification has a non-empty language and body and declares exactly one evaluation scope.
- `DM-007`: Every `DM-*` constraint and derived property is expressed in OCL with `scope = definitionModel` in the machine-readable definition.
- `DM-008`: A non-OCL expression either occupies syntax intrinsically owned by a physical target or supplies a non-empty `nonOclRationale`.

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

### Relational rules

- `DM-201`: Relation attribute names are unique within a relation.
- `DM-202`: Every candidate-key attribute belongs to its key's relation; at most one candidate key is preferred.
- `DM-203`: A relational foreign key's referencing attributes belong to its relation.
- `DM-204`: A relational foreign key maps once, in order, to every attribute of its referenced candidate key.
- `DM-205`: Mapped relation attributes have compatible value domains.

### Physical rules

- `DM-301`: Physical names are unique among like-kind elements in the target namespace required by the platform.
- `DM-302`: Every physical tabular object belongs to its referenced namespace, and every column belongs to its referenced tabular object.
- `DM-303`: Every constraint column belongs to the constraint's table.
- `DM-304`: A table has at most one primary-key constraint.
- `DM-305`: A foreign key references a primary-key or unique constraint and maps once, in order, to every referenced column.
- `DM-306`: Referencing and referenced columns have target-compatible physical datatypes, and every physical datatype belongs to the physical model's target.
- `DM-307`: Every index key column belongs to the indexed table; an index contains no duplicate key column.
- `DM-308`: A view has a non-empty definition expression.
- `DM-309`: A unique index does not satisfy a required logical uniqueness realization unless a corresponding primary-key or unique constraint is also modeled.
- `DM-310`: A view definition, column default, or physical check constraint has `scope = physicalTarget` and names the expression language or dialect governed by its physical target.
- `DM-311`: When a physical expression implements an upstream business or logical constraint, their realization record identifies that correspondence; target syntax does not silently replace upstream meaning.

### Realization rules

- `DM-401`: A realization set's target is strictly later in the order `ConceptualDataModel`, non-relational `LogicalDataModel`, `RelationalLogicalDataModel`, `PhysicalDataModel`. A realization may skip an intermediate kind deliberately.
- `DM-402`: `realized` has at least one source and one target; `introduced` has no source and at least one target; `omitted` has at least one source and no target.
- `DM-403`: Every source element belongs to the realization set's source model and every target element belongs to its target model.
- `DM-404`: Introduced and omitted realizations require a rationale.
- `DM-405`: Every target element is covered by a realized or introduced record, and every source element is covered by a realized or omitted record.
- `DM-406`: Realization never transfers identity implicitly; each model element retains its own identifier and correspondence remains explicit.
- `DM-407`: A transformation reference identifies a transformation or human procedure rather than containing an OCL mutation body. OCL may specify its model queries, guards, and pre/postconditions.

## 13. Definition Boundary

This layer owns the vocabulary and well-formedness of data models. It does not yet define:

- modeling workflow, approval, collaboration, or user roles;
- diagnostics or validator behavior;
- automatic conceptual-to-logical or logical-to-physical generation;
- database introspection or readback behavior;
- external rule languages, target expression grammars, and transformation languages beyond the adopted OCL usage profile;
- product persistence and runtime interchange beyond the XMI validation representation;
- a product API or user interface; or
- vendor-specific physical options.

Those are decisions for later refinements after this language and its governing CMOF choice are accepted.

## 14. Verification State

The standards are part of this language definition now; the outstanding work is verification, not selection by implication.

- CMOF is the presumed governing model pending the follow-up ADR and executable production-constraint validation.
- OCL 2.3.1 is the default wherever its side-effect-free model semantics apply; equivalent encodings of the `DM-*` rules and derived properties remain to be written.
- The definition-model and subject-data OCL evaluation environments remain to be specified and validated separately.
- ISO/IEC 11179-31 concepts are adopted, while exact inheritance, role names, and multiplicities await normative-text checking.
- IDEF1X compatibility is required for overlapping constructs, while its conceptual-schema terminology must be mapped rather than copied onto DAMA model levels.
- ISO/IEC 11404 governs datatype separation, while the standard type catalogue and datatype mappings remain incomplete.
- ISO/IEC 9075-2 governs the portable physical SQL subset, while detailed construct mapping remains incomplete.
- ISO/IEC 11179-35 and ISO/IEC 19763-12 mappings remain to be demonstrated.
- The OMG MOF 2.5.1 to ISO/IEC 19508:2014 version delta has not been assessed, so ISO MOF conformance is not claimed.
- ISO/IEC 19509 XMI output has not been produced, so representation conformance is not claimed; XMI is not yet a product runtime requirement.
- DAMA alignment remains a hypothesis until checked against exact pages in the user's 2010 edition.
- Realization coverage rules, the explicit relational-logical stage, and the relation/table separation are project composition decisions subject to product-owner review.
