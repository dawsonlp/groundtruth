# Worked Example: Commerce Data Across Abstractions

## Purpose

This example tests whether the draft language can preserve one subject's meaning from business concepts through alternative physical designs, deployment, observation, and maintenance. It is evidence for the transform, not part of the language definition.

It deliberately tests:

- entity types and relationships;
- a relationship that becomes an associative relation;
- logical and relational identifiers;
- tables, a view, columns, primary keys, foreign keys, and indexes;
- target-native relational metadata;
- a document collection, JSON shape, API message, and metadata-bearing object collection;
- alternative branches that do not pass through a relational-logical model;
- deployment material, observed state, drift, and maintenance revision;
- split and many-to-many realization;
- physical detail introduced without an upstream counterpart; and
- the distinction between an integrity constraint and an index.

## Shared Semantic Definitions

The commerce domain owns semantic definitions independently of any one model. They include object classes for `Customer`, `Order`, `Product`, and `Order-product inclusion`, plus data-element concepts such as customer number, order number, product code, ordered time, and inclusion quantity. Each data-element concept has a conceptual domain; each logical representation binds it to an appropriate value domain.

This semantic vocabulary is referenced by conceptual business properties and logical attributes. It is not recreated as column meaning in the physical model.

## Conceptual Model

Model: `Commerce Conceptual Model`

Business entity types:

- `Customer` — a party that places an order
- `Order` — a commercial request from a customer
- `Product` — an offered thing that can be ordered

Business relationships:

- `Customer places Order`
  - each `Order` is placed by exactly one `Customer`
  - a `Customer` may place zero or more `Order` occurrences
- `Order contains Product`
  - an `Order` contains one or more `Product` occurrences
  - a `Product` may occur in zero or more orders
  - semantic object class: `Order-product inclusion`
  - relationship property: `quantity`

The second relationship is modeled as a `BusinessRelationship` with ends and its own property. It is not forced into a binary CMOF association or prematurely called a table.

## Logical Model

Model: `Commerce Logical Model`

| Logical entity type | Attributes | Preferred identifier |
| --- | --- | --- |
| `Customer` | `customerNumber`, `customerName` | `customerNumber` |
| `SalesOrder` | `orderNumber`, `orderedAt`, `customerNumber` | `orderNumber` |
| `Product` | `productCode`, `productName` | `productCode` |
| `OrderLine` | `orderNumber`, `lineNumber`, `productCode`, `quantity` | `orderNumber + lineNumber` |

Logical relationships connect `SalesOrder` to `Customer`, `OrderLine` to `SalesOrder`, and `OrderLine` to `Product`. The `OrderLine` entity is an introduced logical structure that resolves the business relationship's repeatable product occurrences and carries `quantity`.

Logical constraint `Positive quantity`:

```text
language: ISO/IEC 19507:2012 OCL 2.3.1
scope: subjectData
body: context OrderLine inv PositiveQuantity: self.quantity > 0
```

This expression is executable only after the logical model's OCL environment maps its `OrderLine` entity and `quantity` attribute into an OCL classifier and property. The example makes that dependency explicit rather than treating OCL text as self-validating.

## Relational-Logical Model

Model: `Commerce Relational Model`

```text
CUSTOMER(
  CUSTOMER_NUMBER,
  CUSTOMER_NAME,
  candidate key (CUSTOMER_NUMBER)
)

SALES_ORDER(
  ORDER_NUMBER,
  ORDERED_AT,
  CUSTOMER_NUMBER,
  candidate key (ORDER_NUMBER),
  foreign key (CUSTOMER_NUMBER) -> CUSTOMER(CUSTOMER_NUMBER)
)

PRODUCT(
  PRODUCT_CODE,
  PRODUCT_NAME,
  candidate key (PRODUCT_CODE)
)

ORDER_LINE(
  ORDER_NUMBER,
  LINE_NUMBER,
  PRODUCT_CODE,
  QUANTITY,
  candidate key (ORDER_NUMBER, LINE_NUMBER),
  foreign key (ORDER_NUMBER) -> SALES_ORDER(ORDER_NUMBER),
  foreign key (PRODUCT_CODE) -> PRODUCT(PRODUCT_CODE)
)
```

These are relations and relation attributes. They have no database-product types, storage properties, or indexes.

## Physical Model

Model: `Commerce PostgreSQL Physical Model`

Target: PostgreSQL 17 for this example only. This illustrates a well-formed physical target and does not select a project implementation branch.

Role: `design`

Namespace: `commerce`

| Table | Columns | Integrity constraints | Indexes |
| --- | --- | --- | --- |
| `customer` | `customer_id bigint`, `customer_number text`, `customer_name text` | PK `customer_id`; UNIQUE `customer_number` | unique implementation index for the unique constraint, if reported by the platform |
| `sales_order` | `order_id bigint`, `order_number text`, `ordered_at timestamp`, `customer_id bigint` | PK `order_id`; UNIQUE `order_number`; FK `customer_id -> customer.customer_id` | non-unique `ix_sales_order_customer_id(customer_id)` |
| `product` | `product_id bigint`, `product_code text`, `product_name text` | PK `product_id`; UNIQUE `product_code` | unique implementation index for the unique constraint, if reported by the platform |
| `order_line` | `order_id bigint`, `line_number integer`, `product_id bigint`, `quantity integer` | PK `(order_id, line_number)`; FK `order_id -> sales_order.order_id`; FK `product_id -> product.product_id`; CHECK `quantity > 0` | non-unique `ix_order_line_product_id(product_id)` |

View:

- `customer_order_summary(customer_number, order_count)` derives a count of orders by customer.

The physical surrogate identifiers `customer_id`, `order_id`, and `product_id` are introduced physical decisions. The business identifiers remain as unique constraints. The foreign-key indexes are introduced access-path decisions and remain separate from the foreign-key constraints.

The `order_line` check uses a physical-target expression specification: language `PostgreSQL 17 SQL`, scope `physicalTarget`, body `quantity > 0`. It realizes the logical OCL constraint; the SQL text does not replace the logical rule as its source of meaning.

The target has separate portable SQL and PostgreSQL 17 metadata profiles. The PostgreSQL profile identifies an authoritative catalog inventory and can attach native facts such as relation persistence, generated-column state, access method, statistics, privileges, storage parameters, and product-specific object kinds. A coverage assessment cannot say `complete` merely because the four tables above were read; it must account for every accessible kind, property, and relationship in the declared inventory scope.

## Alternative Heterogeneous Physical Branches

These designs refine the same logical meaning without being descendants of the relational-logical model.

### Document-store branch

Physical model: `Commerce Document Physical Model`, role `design`

- `orders` is a `DocumentCollection`.
- Its `DataShape` contains order number, ordered time, a customer reference, and repeated line nodes with product code and positive quantity.
- The declared shape is represented by a JSON Schema Draft 2020-12 `SchemaDocument`; native keywords and references remain recoverable through the JSON Schema profile.
- Partition key, consistency, validation, indexing, and product-specific collection settings come from the named document-store profile, not from relational table classes.

### API branch

Physical model: `Commerce Order API Physical Model`, role `design`

- `Commerce Orders API` is an `ApiService`.
- `POST /orders` is an `ApiOperation` with request and response `ApiMessage` elements.
- The request message references the same order `DataShape`, with media type `application/json`.
- The OpenAPI 3.2.0 document is an `InterfaceDescription` in the design and is emitted as a distinct deployment artifact related by realization; the shared shape is a navigation projection, not a replacement for OpenAPI semantics.

### Stored-asset branch

Physical model: `Commerce Invoice Image Physical Model`, role `design`

- `invoice-images` is an unstructured `StoredAssetCollection` in object storage.
- Its content has no invented tabular or document shape.
- Location, media type, naming convention, retention, encryption, object tags, and provider-native properties are physical metadata.
- A separate metadata `DataShape` may describe the object tags and sidecar manifest without claiming that the image bytes have that structure.

These branches demonstrate that relational-logical refinement is useful for a relational target but is not a mandatory stage for document, interface, or stored-asset realization.

## Deployment, Observation, and Maintenance

The PostgreSQL physical design produces deployment package revision `commerce-pg-deploy/1` containing immutable DDL and migration artifacts with PostgreSQL SQL language identifiers, content references, and digests. Realization records connect each artifact to the physical design elements it creates or alters.

A successful deployment record for the production environment reports that revision 1 executed successfully. It does not prove that the resulting catalog matches the design.

A later introspection produces `Commerce PostgreSQL Observation 2026-07-26`, a physical model with `role = observed`, the production environment, capture time, collector identity, active PostgreSQL metadata profile, and native catalog facts. A comparison finds:

| Expected state | Observed state | Difference | Initial disposition |
| --- | --- | --- | --- |
| index `ix_order_line_product_id` | absent | `missing` | `correctDeployment` |
| no `order_line.fulfillment_note` column | column exists | `unexpected` | `pending` |
| check `quantity > 0` | check `quantity >= 0` | `changed` | `correctDeployment` |

If `fulfillment_note` is a legitimate new business fact, maintenance does not edit the observed model into the design. It starts a new revision at the conceptual or logical artifact that owns that meaning, then produces new physical and deployment revisions. If it is unauthorized drift, the intended design remains unchanged and corrective deployment material is generated. Either disposition preserves the evidence of what was observed.

## Realization Records

The complete example realization set covers every element as required by `DM-405`. Representative records are shown below:

| Source | Target | Disposition | Rationale |
| --- | --- | --- | --- |
| Business entity `Customer` | Logical entity `Customer` | realized | Preserve the business subject as a logical structure |
| Business entity `Order` | Logical entity `SalesOrder` | realized | Avoid collision with reserved or ambiguous implementation terms without changing meaning |
| Relationship `Order contains Product` and property `quantity` | Logical entity `OrderLine` and its relationships | realized | Reify the repeatable relationship and its property |
| Logical entity `Customer` | Relation `CUSTOMER` | realized | Relational representation |
| Logical preferred identifier `customerNumber` | Relational candidate key `CUSTOMER_NUMBER` | realized | Preserve business identity |
| Relation `CUSTOMER` | Table `customer` | realized | Physical table realization |
| Candidate key `CUSTOMER_NUMBER` | Unique constraint `customer_number` | realized | Enforce the business identifier physically |
| No upstream element | Column `customer_id` and PK `customer_id` | introduced | Target-local surrogate identity |
| Relational FK `SALES_ORDER.CUSTOMER_NUMBER` | Physical FK `sales_order.customer_id` | realized | Referential meaning is preserved despite use of surrogate columns |
| Logical constraint `Positive quantity` | Physical check `order_line.quantity > 0` | realized | Preserve the logical rule while translating it into target SQL |
| No upstream element | Index `ix_sales_order_customer_id` | introduced | Physical access path chosen for expected joins |
| No upstream element | View `customer_order_summary` | introduced | Physical read model for an anticipated query; not yet an upstream requirement |
| Logical `SalesOrder` structure | Document collection `orders` and JSON shape | realized | Alternative document realization without a relational-logical intermediary |
| Logical order-create interaction data | API request and response messages | realized | Expose the subject through a typed HTTP data interface |
| Physical PostgreSQL design elements | DDL and migration artifacts | realized | Deploy target-specific design material |

The relational foreign key to a business-key attribute and the physical foreign key to a surrogate column do not correspond by name or direct column identity. Their realization record preserves the semantic relationship while also recording the introduced surrogate-key decision.

## Test Result

The draft language represents every exercised construct without adding a new governing-model primitive beyond CMOF. The example also exposes matters that later refinements must decide rather than hide:

- logical-to-physical generation needs human or target-profile decisions for names, datatypes, and surrogate keys;
- OCL can express the logical constraint, but subject-data evaluation requires an explicit classifier and property mapping;
- readback must distinguish declared constraints from implementation indexes;
- metadata completeness is meaningful only against a named target/profile inventory and collection evidence;
- shared shapes enable cross-technology navigation but cannot replace native JSON Schema, XML Schema, OpenAPI, or vendor metadata;
- successful deployment, intended design, and observed state are different facts;
- maintenance needs revision lineage and explicit drift disposition rather than in-place mutation;
- a physical view may be introduced without a current upstream requirement and should therefore be visible as an introduced realization; and
- datatype compatibility and expression semantics require a selected physical target profile.

This result is structural evidence only. It is not DAMA verification, executable SQL, proof of complete PostgreSQL catalog coverage, proof that the non-relational profiles round-trip native specifications, proof of repository round-trip, or proof that the model passes CMOF production constraints.
