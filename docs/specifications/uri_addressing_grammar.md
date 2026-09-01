# GroundTruth URI Addressing Grammar

This document defines the formal grammar, validation rules, and hierarchy structure for all **GroundTruth Canonical URIs** (`data://`).

---

## 1. The DAMA Three-Tier Addressing Scheme

GroundTruth maps directly to the DAMA DMBOK Information Architecture hierarchy:

| Tier | Format | Purpose | Example |
| :--- | :--- | :--- | :--- |
| **Conceptual** | `data://conceptual/<domain>/<Concept>` | High-level business concepts & glossary terms | `data://conceptual/sales/Customer` |
| **Logical** | `data://logical/<domain>/<Entity>[.<Attr>]` | Normalized domain entities, types, and relations | `data://logical/sales/Order.total_amount` |
| **Physical** | `data://physical/<sys>/<db>/<schema>/<obj>[.<field>]` | Concrete storage tables, columns, topics, and payloads | `data://physical/postgres/public/orders.total_cents` |

---

## 2. Formal EBNF Grammar

```ebnf
DataURI          ::= "data://" Tier "/" DomainPath "/" EntityPath ( "#" Fragment )?

Tier             ::= "conceptual" | "logical" | "physical"
DomainPath       ::= [a-z0-9_]+ ( "/" [a-z0-9_]+ )*
EntityPath       ::= Identifier ( "." Property )*
Identifier       ::= [a-zA-Z0-9_-]+
Property         ::= [a-zA-Z0-9_-]+
Fragment         ::= [a-zA-Z0-9_-]+
```

---

## 3. Tier-Specific Addressing Rules

### A. Conceptual URIs (`data://conceptual/`)
* **Format**: `data://conceptual/<domain>/<BusinessTerm>`
* **Rules**:
  * Represents technology-agnostic business vocabulary.
  * PascalCase for concepts.
* **Examples**:
  * `data://conceptual/billing/Invoice`
  * `data://conceptual/supply_chain/Warehouse`

### B. Logical URIs (`data://logical/`)
* **Format**: `data://logical/<domain>/<Entity>[.<Attribute>]`
* **Rules**:
  * PascalCase for Entity names, snake_case for attributes.
  * Dot notation refers to entity attributes, relationship edges, or value properties.
* **Examples**:
  * `data://logical/sales/Order`
  * `data://logical/sales/Order.customer_id`
  * `data://logical/sales/Order.line_items`

### C. Physical URIs (`data://physical/`)
* **Format**: `data://physical/<system-type>/<db-or-cluster>/<schema-or-topic>/<object>[.<field>]`
* **Rules**:
  * System types include `postgres`, `mysql`, `snowflake`, `bigquery`, `kafka`, `s3`, `redis`.
* **Examples**:
  * `data://physical/postgres/prod_db/public/orders.total_cents`
  * `data://physical/kafka/event_broker/orders.v1/order_placed.proto#OrderPlacedPayload`
  * `data://physical/s3/lakehouse/parquet/sales/orders/data.parquet#order_id`

---

## 4. Cross-Tier Mapping

Physical storage definitions declare which Logical entities they realize:

```
Physical Column (orders.total_cents)  ──[ REALIZES ]──>  Logical Attribute (Order.total_amount)
Logical Entity (sales/Order)          ──[ REALIZES ]──>  Conceptual Concept (sales/Order)
```
