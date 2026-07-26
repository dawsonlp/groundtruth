# Worked Example: Commerce Data Across Abstractions

## Purpose

This example tests whether the draft language can preserve one subject's meaning from business concepts through a relational logical model to physical SQL structures. It is evidence for the transform, not part of the language definition.

It deliberately tests:

- entity types and relationships;
- a relationship that becomes an associative relation;
- logical and relational identifiers;
- tables, a view, columns, primary keys, foreign keys, and indexes;
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
| No upstream element | Index `ix_sales_order_customer_id` | introduced | Physical access path chosen for expected joins |
| No upstream element | View `customer_order_summary` | introduced | Physical read model for an anticipated query; not yet an upstream requirement |

The relational foreign key to a business-key attribute and the physical foreign key to a surrogate column do not correspond by name or direct column identity. Their realization record preserves the semantic relationship while also recording the introduced surrogate-key decision.

## Test Result

The draft language represents every exercised construct without adding a new governing-model primitive beyond CMOF. The example also exposes matters that later refinements must decide rather than hide:

- logical-to-physical generation needs human or target-profile decisions for names, datatypes, and surrogate keys;
- readback must distinguish declared constraints from implementation indexes;
- a physical view may be introduced without a current upstream requirement and should therefore be visible as an introduced realization; and
- datatype compatibility and expression semantics require a selected physical target profile.

This result is structural evidence only. It is not DAMA verification, executable SQL, or proof that the model passes CMOF production constraints.
