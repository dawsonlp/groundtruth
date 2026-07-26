# Standards Evidence for the Data-Modeling Definition

## Status and Authority

This file records the investigation used to produce section 2 of `layers/data-modeling-definition/artifacts/data-modeling-language.md`.

It is transform evidence, not the authority for the selected standards profile. If this evidence reveals an error, revise the transform decision and regenerate the main artifact; do not maintain a competing standards decision here.

## Finding

No single identified ISO, OMG, W3C, or industry specification covers the complete language required across DAMA-oriented conceptual, logical, relational-logical, heterogeneous physical data modeling, deployment, and operational observation.

The official scopes divide the territory among metamodel definition, constraint expression, conceptual-schema modeling, semantic data registration, datatype definition, SQL, model registration, and interchange. The main artifact composes those concerns explicitly and marks project semantics where no selected standard supplies the whole relationship.

## Public Evidence Reviewed

| Source | Scope established by official public material | Limitation of current evidence |
| --- | --- | --- |
| OMG MOF 2.5.1 | Defines EMOF and CMOF metamodeling capabilities and provides normative machine-readable resources and production constraints | The draft language has not yet been encoded as CMOF/XMI or executed against those constraints |
| ISO/IEC 19508:2014 | Provides the current ISO-standardized MOF Core baseline | It predates OMG MOF 2.5.1; the version delta has not been assessed |
| ISO/IEC 19507:2012 | Defines OCL 2.3.1 and remains current after confirmation in 2022 | Equivalent OCL for the `DM-*` rules has not yet been written or executed |
| ISO/IEC/IEEE 31320-2:2012 | Defines IDEF1X97 for conceptual schemas; key style represents enterprise data structure and semantics | The paid normative text has not been mapped construct by construct to the draft language |
| ISO/IEC 11179-31:2023 | Covers data elements, data-element concepts, object classes, properties, conceptual domains, value domains, datatypes, and permissible values | Public material does not establish every inheritance, role, constraint, or multiplicity needed for a detailed conformance claim |
| ISO/IEC 11404:2007 | Separates conceptual, structural, and implementation datatype notions and addresses mappings | Its complete datatype catalogue and the replacement edition under development have not been analyzed |
| ISO/IEC 9075-2:2023 | Defines SQL data structures, operations, and integrity constraints | Detailed table, view, column, datatype, and constraint mappings require normative-text verification; public material does not establish a portable index model |
| ISO/IEC 9075-11:2023 | Defines SQL information and definition schemas used to describe an SQL implementation | It does not include every vendor catalog extension, privilege surface, statistic, storage option, or operational fact; complete coverage is target/version-specific |
| JSON Schema Draft 2020-12 | Current published JSON Schema meta-schema and Core/Validation specification family | A shared `DataShape` projection cannot replace native dialect keywords, references, annotations, and extension vocabularies |
| W3C XML Schema Definition Language 1.1 | Defines XML schema components, elements, attributes, types, identity constraints, and validation semantics | Detailed component mapping and XML-specific semantics cannot be inferred from generic tree structure alone |
| OpenAPI Specification 3.2.0 | Current published language-independent description for HTTP APIs, including operations, messages, media types, schemas, and extension points | It describes interface contracts, not the service's internal logical or physical storage model; native OpenAPI content must remain recoverable |
| W3C DCAT 3 | Defines interoperable catalog concepts for datasets, distributions, data services, and catalogs | It does not define detailed physical schemas, database catalogs, or storage-provider operational metadata |
| W3C PROV-DM | Defines a domain-independent provenance model for entities, activities, agents, derivation, and responsibility | Importing the full model would be premature; this layer needs an explicit alignment boundary for artifact, transformation, observation, and collection provenance |
| ISO/IEC 11179-35:2023 | Covers registration of models, metamodels, associated concepts, and mappings; excludes physical instantiation | A mapping from this language's realization records has not been demonstrated |
| ISO/IEC 19763-12:2015 with Amendment 1:2023 | Covers registration of information-requirement models and database-structure models | It is a registry metamodel rather than the modeling language itself |
| ISO/IEC 19509:2014 | Standardizes XMI 2.4.2, which is referenced by the MOF 2.5.1 specification | No XMI validation representation exists yet; the relational runtime repository requirement does not determine its schema or make XMI a persistence format |
| OMG UML 2.5.1 and ISO/IEC 19505-1:2012 | Supply the structural kernel and standardized UML infrastructure relevant to CMOF | The versions differ; shared structure does not provide data-modeling semantics or make subject data models UML models |
| OMG CWM 1.1 | Covers warehouse metadata interchange and publishes relational, datatype, key/index, expression, transformation, and other modules | Its resources are MOF 1.3/XMI 1.1-era and its warehouse surface is broader than this use case |
| User's 2010 DAMA-DMBOK edition | Selected source for DAMA nomenclature, abstraction, and practice | Exact edition statement and page evidence have not been supplied to the repository |

## Consequences for This Transform

- The standard selections and their concern boundaries belong in the target artifact.
- The external MOF document and the normative CMOF model/compliance point require distinct references: `MOF-SPEC` defines `CMOF-GOV`; `DML-DEF` conforms to `CMOF-GOV`.
- Detailed conformance claims remain blocked where only public abstracts have been reviewed.
- The absence of one all-encompassing standard does not authorize unmarked invention; each project extension must identify the standards gap it bridges.
- CMOF, OCL, and XMI can be validated mechanically once the machine-readable representation exists.
- OCL can be the common side-effect-free language for model validation and subject constraints only if their different evaluation environments are defined explicitly.
- DAMA, IDEF1X, ISO/IEC 11179, ISO/IEC 11404, and ISO SQL require semantic mapping evidence as well as syntactic representation.
- Physical metadata completeness cannot be established by a fixed universal class inventory. It must be assessed against an authoritative metadata surface for a named target and version.
- Shared physical constructs should support cross-technology navigation, while native profiles preserve exact JSON Schema, XML Schema, OpenAPI, NoSQL, storage, and vendor-catalog semantics.
- No selected specification supplies a universal NoSQL metamodel. Document, key-value, wide-column, and graph technologies must not be collapsed into one supposed standard model.
- XMI and the required relational repository serve different purposes: XMI validates/interchanges the CMOF representation, while the repository is the deployed catalog realization and must round-trip it without semantic loss.

## References

- [OMG MOF 2.5.1](https://www.omg.org/spec/MOF/2.5.1)
- [ISO/IEC 19508:2014](https://www.iso.org/standard/61844.html)
- [ISO/IEC 19507:2012](https://www.iso.org/standard/57306.html)
- [ISO/IEC/IEEE 31320-2:2012](https://www.iso.org/standard/60614.html)
- [ISO/IEC 11179-31:2023](https://www.iso.org/standard/78925.html)
- [ISO/IEC 11179-35:2023](https://www.iso.org/standard/81727.html)
- [ISO/IEC 19763-12:2015](https://www.iso.org/standard/61559.html)
- [ISO/IEC 11404:2007](https://www.iso.org/standard/39479.html)
- [ISO/IEC 9075-2:2023](https://www.iso.org/standard/76584.html)
- [ISO/IEC 9075-11:2023](https://www.iso.org/standard/76586.html)
- [JSON Schema Draft 2020-12](https://json-schema.org/specification)
- [W3C XML Schema Definition Language 1.1, Part 1](https://www.w3.org/TR/xmlschema11-1/)
- [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html)
- [W3C Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/)
- [W3C PROV-DM](https://www.w3.org/TR/prov-dm/)
- [ISO/IEC 19509:2014](https://www.iso.org/standard/61845.html)
- [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1)
- [ISO/IEC 19505-1:2012](https://www.iso.org/standard/32624.html)
- [OMG CWM 1.1](https://www.omg.org/spec/CWM/1.1)
