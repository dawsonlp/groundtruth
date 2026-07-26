# CMOF Fit Assessment

## Result

The current language inventory exposes no blocking CMOF 2.5.1 expressiveness gap. CMOF can govern the structure of the data-modeling definition without containing data-modeling concepts itself.

This supports continuing with direct CMOF use as the working presumption. It does not yet settle the ADR because the definition has not been encoded in machine-readable CMOF, the normative production constraints have not been executed, and the DAMA inventory has not been verified page by page.

## Coverage Classification

| Required capability | CMOF representation | Classification | Qualification |
| --- | --- | --- | --- |
| Definition packages | `Package`, `PackageImport` | Native CMOF | Package merge is not required initially |
| Data-modeling types | `Class`, `DataType`, `Enumeration`, `Generalization` | Directly expressible | Data semantics come from this definition, not CMOF |
| Attributes, roles, multiplicity, containment | `Property` and multiplicity; composite aggregation | Native CMOF | CMOF constraints on defaults and composition apply |
| Model identity, purpose, scope, and boundary | `DataModel` class and properties | Directly expressible | These are project semantics |
| Conceptual, logical, relational-logical, and physical model kinds | Subclasses of `DataModel` | Directly expressible | The abstraction order is a definition constraint |
| Binary entity relationship | Reified relationship class with two end objects | Directly expressible | A CMOF `Association` is optional, not required |
| N-ary entity relationship | Reified relationship class with two or more end objects | Directly expressible | Required because CMOF associations have exactly two member ends |
| Relationship-associated properties or rules | Properties referencing the reified relationship as their subject | Directly expressible | Preserves relationship semantics without encoding tricks |
| Governing-model constraints | CMOF `Constraint` with OCL `OpaqueExpression` | Native CMOF | ISO/IEC 19507:2012 OCL 2.3.1 is selected; equivalent expressions and an evaluator remain to be supplied |
| Subject-model business, logical, and physical constraints | Instances of definition classes such as `BusinessConstraint` and `ForeignKeyConstraint` | Directly expressible | Correctly distinct from CMOF constraints |
| Semantic data concepts and value domains | Definition classes and properties | Directly expressible | ISO/IEC 11179 alignment requires normative-text verification |
| Relation, key, and foreign-key structure | Definition classes, ordered multivalued properties, and constraints | Directly expressible | Compatibility rules require a constraint expression |
| Table, view, column, physical type, constraint, and index | Definition classes and properties | Directly expressible | Vendor-specific semantics remain in later target profiles |
| Cross-model many-to-many realization | Reified `Realization` class and multivalued source/target properties | Directly expressible | This semantic is not native CMOF |
| Introduced or omitted realization detail | Realization disposition plus constraints | Directly expressible | This semantic is a project choice |
| Stable model-element identity | Inherited `identifier` property, eligible for `isID = true` | Directly expressible | CMOF permits only one ID property per class; catalog-wide lifecycle semantics are additional |
| Provenance | A future CMOF-conforming provenance class | Directly expressible | Not yet included because no concrete minimum has been established |
| Definition composition and extension | Package import plus generalization | Native CMOF | Package merge is available but not selected by default |

No inventory item currently falls into `semantically distorted` or `not expressible`. The n-ary relationship and realization cases are reified domain concepts, not workarounds: both have identity, properties, and rules independent of a bare link.

## CMOF Constraints That Affect the Definition

The local normative MOF 2.5.1 PDF establishes constraints that materially shape the draft:

- CMOF associations have exactly two member ends. N-ary data relationships therefore cannot be represented as one CMOF association.
- Every named element except a value specification must be named.
- A class can expose only one effective `isID` property.
- Association ends must be typed by classes.
- A constraint must constrain at least one element and use a non-empty `OpaqueExpression`.
- Composite aggregation is the supported ownership aggregation.
- Integer values used in a CMOF model are restricted to signed 32-bit range and strings to 65,535 characters.

The current Markdown projection is consistent with these constraints by inspection. That is weaker evidence than validating an XMI representation with the normative CMOF OCL files.

## Unneeded CMOF Surface

The first definition does not require:

- `Operation`, `Parameter`, or raised-exception behavior;
- active classes or behavioral modeling;
- `PackageMerge` for ordinary extension;
- enumeration attributes or operations;
- general instance specifications as a user-facing notation;
- factories, reflective operations, or lifecycle APIs in the language surface; or
- most UML notation and behavioral semantics.

Direct CMOF use does not require exposing these features to a data architect. The actual costs are narrower:

- a conforming implementation must understand the selected CMOF subset and normative constraints;
- CMOF's UML-kernel dependency makes the external standard larger than this language;
- the selected XMI validation representation and OCL constraint profile add tooling and version-compatibility obligations; and
- the binary-association restriction requires relationship reification for n-ary data semantics.

Defining a smaller project-specific MOF-conforming governing model would move these costs rather than eliminate them. The project would then own its subset semantics, its proof of MOF conformance, its versioning, and an additional conformance relationship. No current requirement justifies that extra governing layer.

## Relationship to UML

Direct CMOF use provides a real but limited UML benefit:

- the data-modeling definition and UML are both described using the same CMOF/UML structural kernel;
- standard class-diagram notation can render many definition structures without inventing a notation;
- CMOF-aware repositories and interchange tools have a plausible common representation; and
- an explicit mapping can relate data-model elements to UML elements using shared identity, property, type, and multiplicity concepts.

It does not make a data model a UML model, provide UML data-modeling semantics, or create mappings automatically. A project-specific CMOF-conforming governing model would retain shared ancestry but add a translation boundary before the data-modeling definition. On present evidence, direct CMOF gives the simpler and slightly better tooling relationship.

## Provisional Judgment

Continue using CMOF 2.5.1 directly unless one of the remaining validations produces a concrete counterexample. Do not add a project-specific governing model merely to hide unused CMOF concepts.

The final decision remains open until:

1. DAMA 2010 verification fixes the required semantic inventory;
2. normative ISO checks settle the adopted standard semantics;
3. the definition is represented in machine-readable CMOF/XMI;
4. both the normative CMOF production constraints and the definition's OCL constraints pass; and
5. the product owner accepts the abstraction and vocabulary choices.

## Evidence

- [OMG MOF 2.5.1 specification](https://www.omg.org/spec/MOF/2.5.1)
- [OMG MOF 2.5.1 machine-readable resources](https://www.omg.org/spec/MOF/machine-readable)
- Project-supplied copy: `supporting_documents/formal-19-10-01_omg_omf2.pdf` (read as evidence, not added by this transform)
