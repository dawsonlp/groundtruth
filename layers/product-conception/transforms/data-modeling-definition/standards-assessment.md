# Standards Assessment for the Data-Modeling Definition

## Finding

No single identified ISO standard defines the complete DAMA-style language required here across conceptual, logical, relational-logical, and physical data modeling.

There are standards for different parts of the territory. The coherent approach is to use CMOF as the formalism in which this language is defined, use DAMA 2010 to verify the abstraction levels and data-management approach, and adopt ISO semantics by concern. Combining those sources does not make the resulting language an ISO standard.

This assessment is based on official public specification pages and the complete OMG MOF 2.5.1 PDF supplied to the project. Paid normative ISO texts have not yet been reviewed, so claims of detailed conformance remain open.

## Source Classification

| Source | Concern actually standardized | Use in this definition | Boundary |
| --- | --- | --- | --- |
| OMG MOF 2.5.1, CMOF conformance point | A model for defining metamodels | Provisional governing model for the definition's packages, classes, properties, generalizations, datatypes, enumerations, associations, and constraints | Supplies no DAMA or database semantics |
| DAMA-DMBOK, user's 2010 edition | Data-management body of knowledge and data-modeling approach | Verification baseline for conceptual, logical, and physical abstraction and DAMA nomenclature | Not an ISO modeling-language standard; page evidence is pending |
| ISO/IEC/IEEE 31320-2:2012, IDEF1X97 | Syntax and semantics for a language representing conceptual schemas; its key style represents enterprise data structure and semantics | Normative candidate for entity, attribute, identifier, relationship, and cardinality semantics where compatible with DAMA | Does not cover target-specific physical structures such as indexes; detailed adoption awaits the normative text |
| ISO/IEC 11179-31:2023 | Registration of data elements, data-element concepts, object classes, properties, conceptual domains, value domains, datatypes, and permissible values | Semantic vocabulary connecting business meaning to logical data elements | Does not define conceptual/logical/physical model progression or physical database artifacts |
| ISO/IEC 11179-35:2023 | Registration of models, metamodels, associated concepts, and mappings | Alignment source for future catalog registration and mappings | Explicitly does not govern physical instantiation and does not define the models' own semantics |
| ISO/IEC 19763-12:2015 with Amendment 1:2023 | Registration of information-requirement models and database-structure models | Alignment source for future information-model registration | A registry metamodel, not a complete data-modeling language |
| ISO/IEC 11404:2007 | General-purpose datatypes and mappings among conceptual, structural, and implementation datatype notions | Candidate foundation for datatype categories and mappings | A replacement edition is under development; the current definition does not yet adopt its complete type inventory |
| ISO/IEC 9075-2:2023, SQL/Foundation | SQL data structures, operations, and integrity constraints | Normative candidate for portable SQL physical concepts such as tables, views, columns, and integrity constraints | Does not by its public description establish a portable physical-index model; target-platform specifications must govern indexes |
| OMG CWM 1.1 | Warehouse-oriented metadata interchange, including relational, keys/indexes, transformations, and other warehouse packages | Prior art for coverage comparison only | Published with MOF 1.3/XMI 1.1-era machine-readable resources, substantially broader than this use case, and not selected as the governing language |

## Decisions by Concern

### Model-definition formalism

Use CMOF 2.5.1 provisionally. A data-modeling construct is represented as a CMOF class or datatype; its roles and attributes are CMOF properties; inheritance is CMOF generalization; and well-formedness rules are CMOF constraints. This is a structural conformance claim only until a machine-readable model passes the normative CMOF constraints.

### Conceptual and logical modeling semantics

Use the user's DAMA 2010 edition to verify what belongs in each abstraction. Use IDEF1X semantics where they address the same concern and do not conflict with DAMA. The ISO page calls IDEF1X a language for a "conceptual schema"; that label is not automatically equated with this project's `ConceptualDataModel`. The standard's actual constructs must be mapped individually because its key-style schema may contain detail that this project classifies as logical.

### Shared data meaning

Adopt the ISO/IEC 11179-31 separation among:

- an object class;
- a property;
- the data-element concept formed from them;
- a conceptual domain of possible meanings;
- a value domain defining representations; and
- a data element binding meaning to a value domain.

These concepts prevent a column or logical attribute from becoming the sole authority for business meaning. Exact multiplicities and registration administration are deferred until the normative standard is available.

### Datatypes

Keep conceptual domains, logical value domains, and physical implementation types distinct. ISO/IEC 11404 is the candidate source for a standard datatype vocabulary and for explicit mappings between abstract and implementation types. The current draft defines the separation but does not reproduce or claim conformance to the ISO type catalogue.

### Physical SQL structures

Use ISO/IEC 9075-2 as the portable baseline for SQL physical structures and integrity constraints. A physical target also names a platform and version because products add types, expressions, storage choices, and access structures beyond the portable core.

An `Index` is modeled separately from `UniqueConstraint`, `PrimaryKeyConstraint`, and `ForeignKeyConstraint`. An index may support a constraint in a particular platform, but it does not acquire the constraint's data-integrity meaning merely by being unique or by sharing columns.

### Registration and mappings

Align future catalog behavior with ISO/IEC 11179-35 and ISO/IEC 19763-12. Do not make the definition inherit their registry administration machinery. The present `Realization` vocabulary describes semantic correspondence; a later catalog layer can map it into the registration standards.

## Why No Existing Standard Is Adopted Whole

IDEF1X is the closest identified ISO-standardized data-modeling language, but its official scope is conceptual schemas rather than the complete target-specific realization chain. ISO/IEC 11179 and ISO/IEC 19763 describe registries and shared metadata. SQL defines a database language rather than the upstream business model. CWM covers physical and warehouse metadata but brings warehouse, transformation, OLAP, and legacy MOF concerns that are not required here.

The project therefore is not inventing alternatives to existing standards indiscriminately. It is defining the missing composition and making every adopted or project-specific semantic boundary explicit.

## References

- [OMG MOF 2.5.1](https://www.omg.org/spec/MOF/2.5.1)
- [ISO/IEC/IEEE 31320-2:2012](https://www.iso.org/standard/60614.html)
- [ISO/IEC 11179-31:2023](https://www.iso.org/standard/78925.html)
- [ISO/IEC 11179-35:2023](https://www.iso.org/standard/81727.html)
- [ISO/IEC 19763-12:2015](https://www.iso.org/standard/61559.html)
- [ISO/IEC 11404:2007](https://www.iso.org/standard/39479.html)
- [ISO/IEC 9075-2:2023](https://www.iso.org/standard/76584.html)
- [OMG CWM 1.1](https://www.omg.org/spec/CWM/1.1)
