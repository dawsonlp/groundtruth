# GroundTruth Option B Data URI Addressing Grammar (ADR 0004)

This document defines the formal grammar, validation rules, and hierarchy structure for all **GroundTruth Canonical Data URIs** (`data://`).

---

## 1. The DAMA 4-Tier Semantic Addressing Scheme (Option B)

GroundTruth maps directly to ISO/IEC 11179 and DAMA DMBOK Information Architecture with universal Option B coordinates:

| Tier | Option B Canonical Format | Purpose | Example |
| :--- | :--- | :--- | :--- |
| **Conceptual** | `data://[tenant:]<solution>/conceptual/<term>@v1` | ISO/IEC 11179 Business Terms & Concepts | `data://tripartite:ecommerce/conceptual/customer_account@v1` |
| **Logical** | `data://[tenant:]<solution>/logical/<Entity>[.<Attr>]@v1` | Normalized Entities, Attributes, & FSMs | `data://tripartite:ecommerce/logical/Order.total_amount@v1` |
| **Physical** | `data://[tenant:]<solution>/physical/<engine>/<schema>/<table>@v1` | Projected Tables, Columns, & DDL | `data://tripartite:ecommerce/physical/postgres/ecommerce/orders@v1` |
| **Code Lookup** | `data://[tenant:]<solution>/codes/<domain_code>@v1` | Standardized Reference Lookup Tables | `data://tripartite:ecommerce/codes/order_status@v1` |

---

## 2. Formal Option B Data URI Grammar

```ebnf
DataURI          ::= "data://" Authority "/" Tier "/" EntityPath ( "@" Version )? ( "#" Fragment )?

Authority        ::= ( Tenant ":" )? Solution
Tenant           ::= [a-z0-9_-]+
Solution         ::= [a-z0-9_-]+
Tier             ::= "conceptual" | "logical" | "physical" | "codes"
EntityPath       ::= Identifier ( "/" Identifier )* ( "." Property )*
Version          ::= "latest" | "v" [0-9]+ ( "." [0-9]+ )? | [a-zA-Z0-9_.-]+
Fragment         ::= [a-zA-Z0-9_.-]+
```

---

## 3. Canonical 5-Tuple Resolution

Every Data URI resolves to a discrete 5-tuple:

$$\langle\text{data}, \text{Tenant}, \text{Solution}, \text{Version}, \text{Tier/Path}\rangle$$


---

## 4. Cross-Tier Mapping

Physical storage definitions declare which Logical entities they realize:

```
Physical Column (orders.total_cents)  ──[ REALIZES ]──>  Logical Attribute (Order.total_amount)
Logical Entity (sales/Order)          ──[ REALIZES ]──>  Conceptual Concept (sales/Order)
```
