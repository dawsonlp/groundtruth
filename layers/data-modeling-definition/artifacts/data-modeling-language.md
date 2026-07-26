# Data-Modeling Language Definition

## Document Status

- Status: draft
- Effective: no
- Governing model: CMOF 2.5.1, presumed pending the follow-up ADR
- DAMA verification baseline: user's 2010 DAMA-DMBOK edition
- DAMA page verification: pending
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

## 2. Abstraction Boundaries

The abstraction belongs to a model. An element belongs to exactly one model and acquires its permitted vocabulary from that model's kind.

| Model kind | Purpose | Includes | Excludes |
| --- | --- | --- | --- |
| `ConceptualDataModel` | State business meaning and scope | Business entity types, business properties, relationships, cardinality, and business constraints | Relations, foreign keys, tables, columns, platform types, indexes |
| `LogicalDataModel` | State technology-neutral data structure and integrity | Logical entity types, attributes, identifiers, value domains, relationships, and logical constraints | Database products, storage objects, platform types, indexes |
| `RelationalLogicalDataModel` | State a logical model using the relational model | Relations, relation attributes, candidate keys, and relational foreign keys | Tables, storage options, platform data types, indexes |
| `PhysicalDataModel` | State realization in a named target environment | Namespaces, tables, views, columns, physical types, integrity constraints, and indexes | Unresolved business meaning or unnamed implementation targets |

A relation and a table are not synonyms. A relation is a logical value with a heading and relational constraints. A table is a physical database object in a target environment. A table may realize one relation, several relations, or part of a relation, and that correspondence is explicit.

## 3. CMOF Representation

The definition consists of CMOF packages named `Core`, `Semantics`, `Conceptual`, `Logical`, `Relational`, `Physical`, and `Realization`.

- Every type below is a CMOF `Class`, `DataType`, or `Enumeration`.
- Every field or role is a CMOF `Property` with the stated multiplicity.
- `owns` denotes a composite CMOF property.
- `extends` denotes CMOF `Generalization`.
- `{derived}` denotes a read-only navigation calculated from the named authoritative reverse reference, not separately stored membership.
- Each rule in section 11 is a CMOF `Constraint` whose specification is an `OpaqueExpression`.
- Subject-model constraints such as a foreign key are instances of language classes; they are not CMOF constraints governing the form of the language.

This Markdown is a review projection, not the machine-readable CMOF representation required for acceptance.

## 4. Core Package

### `IdentifiedElement` (abstract)

- `identifier: String [1]` — stable identity within the catalog
- `name: String [1]`
- `definition: String [1]`

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

## 5. Semantics Package

This package adopts the distinctions described by ISO/IEC 11179-31. Exact multiplicities remain subject to verification against the normative text.

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

## 6. Conceptual Package

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

- `expression: String [1]`
- `constrainedElements: ModelElement [1..*]`

A business rule that limits valid states or events in the modeled domain. Its expression language is not yet selected.

## 7. Logical Package

### `LogicalDatatype` extends `SemanticElement`

A technology-neutral datatype. Its eventual standard inventory and mapping semantics are expected to align with ISO/IEC 11404.

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

- `expression: String [1]`
- `constrainedElements: ModelElement [1..*]`

A technology-neutral integrity condition not completely represented by identity, optionality, or relationship cardinality.

## 8. Relational Package

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

## 9. Physical Package

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

- `definitionExpression: String [1]`

### `PhysicalDatatype` extends `IdentifiedElement`

- `target: PhysicalTarget [1]`, opposite `PhysicalTarget::datatypes`
- `declaration: String [1]`

### `Column` extends `PhysicalElement`

- `tabularObject: PhysicalTabularObject [1]`
- `datatype: PhysicalDatatype [1]`
- `nullable: Boolean [1]`
- `defaultExpression: String [0..1]`

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

- `expression: String [1]`

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

## 10. Realization Package

### `RealizationSet` extends `IdentifiedElement`

- `sourceModel: DataModel [1]`
- `targetModel: DataModel [1]`
- owns `realizations: Realization [1..*]`

### `Realization` extends `IdentifiedElement`

- `disposition: RealizationDisposition [1]`
- `sourceElements: ModelElement [0..*] {unique}`
- `targetElements: ModelElement [0..*] {unique}`
- `rationale: String [0..1]`
- `transformationRule: String [0..1]`

### `RealizationDisposition` enumeration

- `realized` — source meaning is represented by one or more target elements
- `introduced` — target detail is introduced at this abstraction
- `omitted` — source meaning is deliberately not represented in the target

`Realization` is a class rather than a CMOF association because the correspondence is many-to-many and has disposition, rationale, and rule semantics of its own.

## 11. Well-Formedness Rules

### Cross-model rules

- `DM-001`: Every `ModelElement` is owned by exactly one `DataModel`.
- `DM-002`: A model owns only model elements permitted by its exact model kind and references semantic elements only from its domain or imported domains.
- `DM-003`: A physical model has exactly one named `PhysicalTarget`.
- `DM-004`: A conceptual or logical model contains no `PhysicalElement`, `PhysicalDatatype`, or `Index`.
- `DM-005`: Definitions and names are non-empty; model-element identifiers are unique within their containing model and semantic-element identifiers within their domain.

### Conceptual and logical rules

- `DM-101`: A business or logical relationship has at least two ends, and each end refers to an entity type in the same model.
- `DM-102`: End cardinality has a non-negative minimum and a maximum not less than its minimum.
- `DM-103`: Every logical identifier uses attributes assigned to its identified entity type.
- `DM-104`: Every logical entity type has at least one identifier, and at most one is preferred.
- `DM-105`: A value domain and its data-element concept refer to the same conceptual domain, and every referenced semantic element belongs to the data model's domain or a directly or transitively imported domain.
- `DM-106`: A business property's subject is a business entity type or business relationship in the same conceptual model.
- `DM-107`: A business entity type's properties use data-element concepts for its object class. A relationship with properties names an object class, and its properties use concepts for that object class.
- `DM-108`: A logical attribute's data-element concept uses the object class named by its logical entity type.

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

### Realization rules

- `DM-401`: A realization set's target is strictly later in the order `ConceptualDataModel`, non-relational `LogicalDataModel`, `RelationalLogicalDataModel`, `PhysicalDataModel`. A realization may skip an intermediate kind deliberately.
- `DM-402`: `realized` has at least one source and one target; `introduced` has no source and at least one target; `omitted` has at least one source and no target.
- `DM-403`: Every source element belongs to the realization set's source model and every target element belongs to its target model.
- `DM-404`: Introduced and omitted realizations require a rationale.
- `DM-405`: Every target element is covered by a realized or introduced record, and every source element is covered by a realized or omitted record.
- `DM-406`: Realization never transfers identity implicitly; each model element retains its own identifier and correspondence remains explicit.

## 12. Definition Boundary

This layer owns the vocabulary and well-formedness of data models. It does not yet define:

- modeling workflow, approval, collaboration, or user roles;
- diagnostics or validator behavior;
- automatic conceptual-to-logical or logical-to-physical generation;
- database introspection or readback behavior;
- a constraint-expression language;
- CMOF serialization or repository storage;
- a product API or user interface; or
- vendor-specific physical options.

Those are decisions for later refinements after this language and its governing CMOF choice are accepted.

## 13. Standard and Project-Choice Marking

The basis of each construct is recorded in the transform's `standards-assessment.md`. Until normative-text checks are complete:

- CMOF structural mappings are provisional conformance claims;
- ISO-aligned semantics are candidates, not certified conformance;
- DAMA alignment is a hypothesis awaiting exact 2010 page verification; and
- realization coverage rules and the exact separation of relation from table are explicit project choices subject to product-owner review.
