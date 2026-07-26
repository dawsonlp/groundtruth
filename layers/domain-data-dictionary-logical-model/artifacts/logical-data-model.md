# Domain Data Dictionary Logical Data Model

## Document Status

- Status: draft
- Effective: no
- Provisional canonical reference: `CAT-LOG/domain-data-dictionary@1`
- Model kind: `LogicalDataModel`
- Governing definition: `DML-DEF` revision `19133fd`, principally `DML-LOG`, `DML-SEM`, and `DML-REA`
- Source conceptual model: `CAT-CON/domain-data-dictionary@1` at revision `73ed9df`
- PostgreSQL realization: deferred
- API realization: deferred

## 1. Purpose and Scope

Define the technology-neutral structures and integrity rules required to persist and reconstruct catalog governance, governed definitions, catalog models, realization, deployment evidence, observations, and comparisons.

The model includes typed catalog-governance records, reflective model content, logical identity, type binding, property occurrences, object references, recursive values, ordering, containment, and derived typed projections. It excludes PostgreSQL objects, API operations and messages, operational subject data, and implementation algorithms.

## 2. Logical Datatypes

| Logical datatype | Kind | Meaning |
| --- | --- | --- |
| `CatalogIdentifier` | Scalar identifier | Stable identifier of one authoritative catalog record or reflected object; physical syntax deferred |
| `Text` | Scalar text | Technology-neutral textual value |
| `Ordinal` | Scalar integer | Zero-based non-negative occurrence discriminator or value-node sibling position; it conveys semantic order only where the governing definition declares order |
| `LexicalValue` | Scalar text | Target-independent lexical representation interpreted by a cataloged datatype definition |
| `ContentReference` | Scalar text | Reference to externally retained content; location scheme deferred |
| `ExternalReference` | Scalar text | Reference to an identity, source, or activity outside the catalog; scheme and resolution are explicit in the value |
| `ExternalReferenceSet` | Collection | Unordered unique collection of `ExternalReference`; an empty collection records that no external source was supplied |
| `Instant` | Scalar temporal | Point on a time line; precision and physical representation deferred |
| `ValuePath` | Scalar path | Derived, target-independent position of a value node within one property occurrence; physical syntax deferred |
| `DigestAlgorithm` | Scalar text | Named digest algorithm |
| `DigestValue` | Scalar text | Digest value interpreted under its algorithm |
| `ContentDigest` | Record | `algorithm: DigestAlgorithm`, `value: DigestValue` |
| `ValueRole` | Enumeration | `root`, `recordField`, `collectionItem`, `mapEntry`, `mapKey`, `mapValue`, `choiceAlternative` |

`LexicalValue` is not permission to stringify away semantics. Its governing datatype definition determines parsing, equality, and canonicalization. Target-native facts retain the original lexical form even when a portable projection is also available.

## 3. Authoritative Logical Entity Types

The Catalog Record Kernel owns both typed catalog-governance records and a reflective representation of CMOF/DML model content. These forms do not duplicate one another: the typed records hold component-specific facts that `DML-DEF` does not define, while the reflective graph holds objects that are governed by CMOF classes.

### 3.1 Typed catalog-governance entities

#### `ModelFamily`

The purposeful catalog grouping that relates model revisions for one business scope. It is a `CAT-LOG` logical entity, not an addition to general `DML-DEF`.

Logical attributes:

- `modelFamilyIdentifier: CatalogIdentifier [1]`
- `name: Text [1]`
- `purpose: Text [1]`
- `businessScope: Text [1]`

Logical relationships:

- `domain: CatalogObject [1]`, whose governing CMOF class is `DataDomain`
- `familyStatus: CatalogObject [1]`, identifying a permitted governed status value
- `modelRevisions: CatalogObject [0..*]`, each governed by a concrete `DataModel` subclass

Preferred logical identifier:

- `modelFamilyIdentifier`

#### `ResponsibleAgent`

A catalog-identified human, organization, software agent, AI agent, or automation accountable for a recorded activity or assertion. It does not define authorization.

Logical attributes:

- `responsibleAgentIdentifier: CatalogIdentifier [1]`
- `name: Text [1]`
- `externalIdentityReference: ExternalReference [0..1]`

Logical relationships:

- `agentKind: CatalogObject [1]`, identifying a permitted governed agent-kind value

Preferred logical identifier:

- `responsibleAgentIdentifier`

#### `ProvenanceRecord`

An immutable catalog record of an activity affecting or asserting one or more reflected catalog objects.

Logical attributes:

- `provenanceRecordIdentifier: CatalogIdentifier [1]`
- `recordedTime: Instant [1]`
- `sourceReferences: ExternalReferenceSet [1]`
- `evidenceDigest: ContentDigest [0..1]`
- `rationale: Text [0..1]`

Logical relationships:

- `activityKind: CatalogObject [1]`, identifying a permitted governed activity-kind value
- `responsibleAgents: ResponsibleAgent [1..*]`
- `subjects: CatalogObject [1..*]`

Preferred logical identifier:

- `provenanceRecordIdentifier`

Provenance for a catalog-only governance record other than a reflected object remains an open conceptual question. This draft does not widen `subjects` through an invented logical supertype.

### 3.2 Reflective model-content entities

#### `CatalogObject`

A distinguishable CMOF/DML-governed object in the catalog. Definitions and model instances use the same entity type.

Logical attributes:

- `catalogObjectIdentifier: CatalogIdentifier [1]`

Logical relationships:

- `governingType: CatalogObject [1]`, whose represented object is a CMOF class
- `propertyOccurrences: PropertyOccurrence [0..*]` derived from `PropertyOccurrence::subject`

Preferred logical identifier:

- `catalogObjectIdentifier`

Examples include CMOF classes and properties, data domains, semantic definitions, model revisions, model elements, realization mappings, physical targets, deployment records, and observations. The examples are governed types, not hard-coded repository discriminators. Model families, responsible agents, and provenance records use the typed entities above because they are catalog-specific rather than CMOF/DML object types.

#### `PropertyOccurrence`

One occurrence of one property defined by the governing type of a subject object. Multivalued properties have several occurrences with distinct positions.

Logical attributes:

- `position: Ordinal [1]`

Logical relationships:

- `subject: CatalogObject [1]`
- `propertyDefinition: CatalogObject [1]`, whose represented object is an applicable CMOF property
- `referenceTarget: CatalogObject [0..1]`
- `valueNodes: ValueNode [0..*]` derived from `ValueNode::occurrence`
- `rootValue: ValueNode [0..1]` derived as the value node with no parent

Preferred logical identifier:

- `(subject, propertyDefinition, position)`

Exactly one of `referenceTarget` and `rootValue` is present. A single-valued property uses position zero. For an unordered multivalued property, position distinguishes occurrences but does not impose semantic order. Absence of a property is represented by absence of an occurrence, not by an untyped null value.

#### `ValueNode`

One node in the technology-neutral representation of a datatype value. Nodes are dependent on a property occurrence and have no catalog-object identity or independent lifecycle.

Logical attributes:

- `position: Ordinal [1]`
- `role: ValueRole [1]`
- `lexicalValue: LexicalValue [0..1]`
- `contentReference: ContentReference [0..1]`
- `contentDigest: ContentDigest [0..1]`
- `path: ValuePath [1] {derived}`

Logical relationships:

- `occurrence: PropertyOccurrence [1]`
- `parent: ValueNode [0..1]`
- `children: ValueNode [0..*]` derived from `ValueNode::parent`
- `datatypeDefinition: CatalogObject [1]`
- `fieldDefinition: CatalogObject [0..1]`

Preferred logical identifier:

- `(occurrence, path)`

`path` is derived from ancestor roles, field definitions, and positions. It exists to state logical identity and reconstruction order; its physical encoding is deferred.

## 4. Governing-Definition Interpretation

For a reflected `CatalogObject` with governing CMOF class `T`:

1. every `PropertyOccurrence::propertyDefinition` is a CMOF property applicable to `T`, including inherited properties;
2. occurrence count satisfies the property's lower and upper multiplicity;
3. occurrence positions are unique for the subject and property;
4. ordered properties reconstruct in ascending position;
5. unordered unique properties contain no semantically equal duplicate;
6. reference targets conform to the property's class or enumeration type;
7. value roots conform to the property's datatype;
8. composite references establish ownership and do not create multiple owners or cycles; and
9. derived properties are computed from their authoritative opposite or derivation and are not stored as competing occurrences.

The governing CMOF/DML objects used for these checks are themselves catalog objects. Validation is therefore bound to the exact governing-definition revision, not to application code that happens to share a class name. Typed governance entities instead conform directly to the `CAT-LOG` attributes and relationships declared in section 3.1.

## 5. Recursive Value Rules

The datatype definition governs permitted node structure:

| Datatype kind | Required logical value form |
| --- | --- |
| Scalar or enumeration-free atomic datatype | One node bearing its placement role, with `lexicalValue` and no children |
| Record | Root plus one `recordField` child for each present field; each child names its field definition |
| Collection | Root plus ordered `collectionItem` children |
| Map | Root plus ordered `mapEntry` children; each entry has one `mapKey` and one `mapValue` child |
| Choice | Root plus exactly one `choiceAlternative` child naming the selected alternative definition |
| Opaque | One node bearing its placement role, with exactly one of `lexicalValue` or `contentReference` and an optional digest |

The root of an occurrence has role `root`. Every non-root node has exactly one parent in the same occurrence and a role describing its placement in that parent. The node graph is a finite tree. Sibling positions are unique within their role and parent. A record field occurs only as permitted by its record datatype definition. Atomic nodes have `lexicalValue` and no children. Structural nodes have children and no lexical or content-reference payload. Opaque nodes have exactly one content carrier; a digest supplements that carrier rather than replacing it.

## 6. Conceptual-to-Logical Realization

### 6.1 Entity realization

| `CAT-CON` entity | `CAT-LOG` realization |
| --- | --- |
| Data Domain | `CatalogObject` governed by `DataDomain` |
| Semantic Definition | `CatalogObject` governed by the applicable `DML-SEM` type |
| Governing Definition Revision | Governed artifact-root `CatalogObject` plus its composite object closure |
| Model Family | Typed authoritative `ModelFamily` entity |
| Model Revision | `CatalogObject` governed by the exact `DataModel` subtype |
| Model Element | `CatalogObject` governed by the exact `ModelElement` subtype |
| Expression Specification | Root `ValueNode` record tree on its owning subject's governed expression-property occurrence, governed by the `ExpressionSpecification` datatype; it has no independent `CatalogObject` identity |
| Realization Set | `CatalogObject` governed by `RealizationSet` |
| Realization Mapping | `CatalogObject` governed by `Realization` |
| Responsible Agent | Typed authoritative `ResponsibleAgent` entity |
| Provenance Record | Typed authoritative `ProvenanceRecord` entity |
| Physical Target | `CatalogObject` governed by `PhysicalTarget` |
| Target Metadata Profile | `CatalogObject` governed by `PhysicalMetadataProfile` |
| Target Metadata Definition | `CatalogObject` governed by the applicable native-definition type |
| Target-Native Metadata Fact | `CatalogObject` governed by `NativeMetadataValue` or `NativeMetadataRelationship` |
| Deployment Environment | `CatalogObject` governed by `DeploymentEnvironment` |
| Deployment Package | `CatalogObject` governed by `DeploymentPackage` |
| Deployment Artifact | `CatalogObject` governed by `DeploymentArtifact` |
| Deployment Attempt | `CatalogObject` governed by `DeploymentRecord` |
| Observation Capture | `CatalogObject` governed by `ObservationRecord` |
| Metadata Coverage Assessment | `CatalogObject` governed by `MetadataCoverageAssessment` |
| Physical Comparison | `CatalogObject` governed by `PhysicalComparison` |
| Physical Difference | `CatalogObject` governed by `PhysicalDifference` |

### 6.2 Property and relationship realization

- Model Family, Responsible Agent, and Provenance Record properties become the typed attributes in section 3.1.
- Domain scopes families becomes `ModelFamily::domain`; Family groups models becomes `ModelFamily::modelRevisions`.
- Agent is responsible for provenance becomes `ProvenanceRecord::responsibleAgents`; Provenance documents subject becomes `ProvenanceRecord::subjects`.
- Every property of a CMOF/DML-governed conceptual object becomes one or more governed value `PropertyOccurrence` objects.
- Every relationship end among CMOF/DML-governed objects becomes a governed reference `PropertyOccurrence`.
- A relationship carrying properties remains a reified `CatalogObject`; its ends are reference occurrences.
- Cardinality becomes governing property multiplicity plus logical constraints.
- Ordered conceptual or definition-owned collections use occurrence positions.
- Status, classification, and disposition values reference governed enumeration literals where the definition supplies them.
- Provenance subjects, realization endpoints, and physical difference endpoints remain explicit references rather than identifier text.

No conceptual entity or relationship is intentionally omitted. Most conceptual types share the `CatalogObject` logical entity, but their governing CMOF class preserves their distinct meaning. The three catalog-specific types remain explicit logical entities rather than being disguised as nonexistent metamodel classes.

## 7. Derived Typed Projections

A reflected-content typed projection is a read-only logical record derived from:

- one or more required governing types;
- named governing property definitions;
- a selected definition revision; and
- kernel objects and occurrences that pass validation.

Projection fields retain the source object and property identities used to produce them. A missing required property, incompatible type, or ambiguous occurrence is a diagnostic. It is not converted to a plausible default.

For each selected governed class, projection generation applies these rules:

1. the projection identifies the source `CatalogObject`, governing type, and governing-definition revision;
2. each applicable non-derived CMOF property becomes one projection field identified by that property definition, including inherited properties;
3. property multiplicity becomes scalar, optional, ordered collection, or unordered unique collection structure without weakening its bounds;
4. reference properties return catalog identity and may additionally resolve another typed projection;
5. datatype properties return a logical value reconstructed from their `ValueNode` tree;
6. derived properties are computed from their declared derivation and never read from a competing occurrence; and
7. display names are labels only—the governing object and property identifiers remain the binding authority.

Typed governance entities may be joined into capability read models but are not projections. Projection selection may cover the complete reflected entity inventory or a narrower Model C capability family. Selection changes query shape, not authoritative state or conformance rules.

## 8. Logical Integrity Rules

- `CATLOG-001`: Identifiers of `CatalogObject`, `ModelFamily`, `ResponsibleAgent`, and `ProvenanceRecord` share one globally unique, stable catalog-identifier namespace.
- `CATLOG-002`: Every reflected catalog object has exactly one governing CMOF class in the selected definition closure.
- `CATLOG-003`: Every property occurrence definition is applicable to its subject's governing type.
- `CATLOG-004`: `(subject, propertyDefinition, position)` is unique and `position` is non-negative.
- `CATLOG-005`: Exactly one of `referenceTarget` and `rootValue` is present.
- `CATLOG-006`: Occurrence counts, uniqueness, order, composition, and target/value types conform to the governing property definition.
- `CATLOG-007`: Every value node belongs to exactly one occurrence; every non-root node has one parent in that occurrence; value trees are finite and acyclic.
- `CATLOG-008`: `(occurrence, path)` uniquely identifies a value node and reconstructs stable sibling order.
- `CATLOG-009`: Each value node's structure, lexical or content payload, children, role, and field definition conform to the recursive value form selected by its cataloged datatype definition.
- `CATLOG-010`: Composite ownership gives an object at most one owner and creates no containment cycle.
- `CATLOG-011`: Accepted artifact closures contain no dangling references to draft or missing objects unless the governing definition explicitly permits an external reference.
- `CATLOG-012`: Accepted, superseded, and retired revisions and captured observations are immutable.
- `CATLOG-013`: Supersession and realization edges are acyclic and reference exact artifact revisions.
- `CATLOG-014`: Acceptance, import, transformation, deployment, observation, comparison, and disposition have required provenance and responsible-agent references.
- `CATLOG-015`: Intended and observed physical models remain distinguishable by governed type and role; comparison does not mutate either input.
- `CATLOG-016`: Deployment execution status is evidence about an attempt, not equivalence between intended and observed state.
- `CATLOG-017`: A target-native fact resolves to a definition in the active target/profile revision and retains its lexical representation.
- `CATLOG-018`: A typed projection is derived from kernel authority and cannot be updated independently.
- `CATLOG-019`: Export followed by import reconstructs object identity, type, property identity, multiplicity, order, reference, value structure, expressions, and revision relationships without semantic loss.
- `CATLOG-020`: No `CAT-DATA` construct stores operational `BDM-DATA` merely because a model describes it.
- `CATLOG-021`: Every model family references exactly one reflected `DataDomain`; every family member is a reflected concrete `DataModel`, belongs to exactly one family, and is interpreted in that family's domain.
- `CATLOG-022`: Every responsible agent references one permitted governed agent kind; its external identity is evidence, not authorization.
- `CATLOG-023`: Every provenance record is immutable, has one activity kind, one or more responsible agents, one or more reflected subjects, and a recorded time.
- `CATLOG-024`: Typed governance records and reflected model content do not duplicate the same authoritative fact; capability read models preserve the source identity of every combined field.

## 9. Initial OCL Projection

The following OCL is illustrative draft syntax and remains unvalidated:

```ocl
context PropertyOccurrence
inv NonNegativePosition:
  self.position >= 0

context PropertyOccurrence
inv ExactlyOnePayload:
  self.referenceTarget.oclIsUndefined()
  xor self.rootValue.oclIsUndefined()

context CatalogObject
inv UniquePropertyPositions:
  self.propertyOccurrences->isUnique(
    occurrence | Tuple {
      propertyDefinition = occurrence.propertyDefinition,
      position = occurrence.position
    }
  )

context ValueNode
inv RootHasNoParent:
  self.role = ValueRole::root implies self.parent.oclIsUndefined()

context ValueNode
inv NonRootHasParent:
  self.role <> ValueRole::root implies not self.parent.oclIsUndefined()
```

The machine-readable model must add and validate OCL for definition applicability, multiplicity, type conformance, composite ownership, acyclicity, value-tree shape, immutability, artifact closure, and projection derivation before this layer becomes effective.

## 10. PostgreSQL Realization Contract

The PostgreSQL realization transform and its artifacts must:

1. realize the three typed governance entities and three reflective-content entities without loss;
2. preserve composite identifiers and derived value paths or provide explicit equivalent realization;
3. enforce or validate payload exclusivity, ordering, references, and tree integrity;
4. bind every stored object and occurrence to exact definition revisions;
5. support atomic accepted-artifact closure and immutable historical evidence;
6. support recursive values and target-native lexical facts without treating JSON or text as ungoverned escape storage;
7. make typed projections replaceable and traceable to kernel objects;
8. inventory its own PostgreSQL metadata through a named profile;
9. deploy through `CAT-DEPLOY` and observe itself as `CAT-OBS`; and
10. demonstrate round-trip reconstruction of representative `CMOF-GOV`, `DML-DEF`, `CAT-CON`, and subject-model content.

PostgreSQL table, column, constraint, index, extension, partition, JSONB, and migration choices are intentionally absent from this logical model and owned by the realization transform.

## 11. Open Questions

1. Should reflected-content projections exist only as queries, or may the PostgreSQL realization materialize them with mandatory derivation provenance?
2. Which primitive lexical forms require canonicalization in `CAT-LOG`, and which remain governed entirely by their datatype definitions?
3. Must property occurrences themselves be addressable by external provenance, or is their composite logical identity sufficient?
4. How should an accepted artifact reference an accepted shared semantic object outside its own composite closure?
5. What minimum CMOF bootstrap package is required before the repository can validate its own loaded governing model?
6. Which logical constraints are enforced synchronously at command time versus reported by later validation, without changing their normative status?
7. Must provenance subjects include model families or responsible-agent records? If so, does `DML-DEF` need logical entity generalization, or should `CAT-LOG` introduce explicit subject relationships without inventing a universal supertype?
