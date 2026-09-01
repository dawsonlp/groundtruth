# GroundTruth: Information & Data Authority Specification

> **Domain Role**: The single source of truth for **Information Semantics** (structure, business meaning, relationships, constraints, and physical schemas of enterprise data).

---

## 1. Mission & Domain Boundary

**GroundTruth** manages what data *is*, what it *means*, and how it *persists*, completely orthogonal to the programming languages or compute engines executing against it.

### Authority Separation:
* **GroundTruth Owns**: Entity definitions, business glossary terms, domain attributes, relationships, cardinalities, constraints, data classifications, schema versions, and physical schema definitions (SQL DDL, Protobuf, Avro, JSON Schema).
* **CodeMesh Owns**: Computation representations (Python classes, dataclasses, ORMs, functions, serializers, repositories, queries, algorithms).
* **Northstar Owns**: Intent, requirements, ADRs, and governance policies.
* **Boundary Rule**: CodeMesh *never* invents canonical data semantics; it maps computational symbols to canonical entities defined by GroundTruth.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GROUNDTRUTH ONTOLOGY                            │
├────────────────────────────────────────────────────────────────────────┤
│ 1. CONCEPTUAL LAYER: Business Glossary & High-Level Domain Concepts    │
│    data://conceptual/sales/Customer                                    │
│    data://conceptual/sales/Order                                       │
│                                  │                                     │
│                                  ▼ (REALIZES)                          │
│ 2. LOGICAL LAYER: Normalized Domain Entities, Attributes & Relations   │
│    data://logical/sales/Order                                          │
│    ├── order_id: UUID [PK]                                             │
│    ├── customer_id: UUID [FK -> Customer]                              │
│    ├── total_amount: Money { amount: Decimal, currency: ISO_4217 }     │
│    └── status: OrderStatus [PENDING, PAID, SHIPPED, CANCELLED]         │
│                                  │                                     │
│                                  ▼ (MAPPED_TO)                         │
│ 3. PHYSICAL LAYER: Storage Structures, Wire Protocols & Topics         │
│    data://physical/postgres/public/orders                              │
│    data://physical/kafka/sales-events/order_created.proto#OrderEvent   │
│    data://physical/redis/sessions/cart_cache                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Canonical Addressing & Identifier Specification

GroundTruth exposes deterministic, immutable URIs using the `data://` scheme:

### A. Conceptual URIs
* **Format**: `data://conceptual/<domain>/<BusinessConcept>`
* **Examples**:
  * `data://conceptual/billing/Invoice`
  * `data://conceptual/logistics/Consignment`

### B. Logical URIs
* **Format**: `data://logical/<domain>/<Entity>[.<Attribute>]`
* **Examples**:
  * `data://logical/sales/Order`
  * `data://logical/sales/Order.total_amount`
  * `data://logical/sales/Order.items` (Relationship attribute)

### C. Physical URIs
* **Format**: `data://physical/<system-type>/<cluster-or-db>/<schema-or-topic>/<object>[.<field>]`
* **Examples**:
  * `data://physical/postgres/primary_db/public/orders.total_cents`
  * `data://physical/kafka/production_broker/orders.v1/order_placed.proto#OrderPlacedPayload`
  * `data://physical/s3/lakehouse_bucket/parquet/sales/orders/part_001.parquet#order_id`

---

## 3. Functional Requirements

### FR-1: DAMA Three-Tier Hierarchy Preservation
1. GroundTruth must maintain strict parent-child mappings from Conceptual $\to$ Logical $\to$ Physical.
2. An entity must not bypass the Logical model: physical database tables and Kafka topics must declare which Logical entity/attributes they realize.
3. CodeMesh computation must link to the appropriate tier:
   * **Domain Services & Business Logic** link to **Logical Entities** (`CREATES`, `READS`, `VALIDATES`).
   * **Persistence Repositories & SQL Drivers** link to **Physical Objects** (`WRITES`, `SERIALIZES`).

### FR-2: Cross-Model Code Linkage Verbs
GroundTruth supports incoming relational edges from CodeMesh symbols (`csi://...`):

| Cross-Domain Verb | Source | Target | Meaning |
| :--- | :--- | :--- | :--- |
| `CREATES` | Code Symbol (`csi://...`) | Logical Entity | The function instantiates or generates a new business entity. |
| `READS` | Code Symbol (`csi://...`) | Logical / Physical Entity | The code reads attributes from an entity or storage table. |
| `WRITES` | Code Symbol (`csi://...`) | Physical Storage / Wire | The code mutates or persists records into a physical store. |
| `VALIDATES` | Code Symbol (`csi://...`) | Logical Attribute / Invariant | The code checks domain rules or integrity constraints on an attribute. |
| `SERIALIZES` | Code Symbol (`csi://...`) | Physical Wire Protocol | The code converts logical memory structures into wire formats. |
| `REPRESENTS` | Code Symbol (`csi://...`) | Logical Entity | A class/dataclass is the computational in-memory model of a logical entity. |

### FR-3: Schema Evolution & Compatibility Engine
1. **Semantic Diffing**: When data entities change, GroundTruth computes structured semantic diffs (`AttributeAdded`, `AttributeRemoved`, `TypeNarrowed`, `NullabilityChanged`, `EnumVariantAdded`).
2. **Compatibility Rules**: GroundTruth classifies changes by compatibility tier:
   * *Fully Compatible*: Adding an optional attribute with a default value.
   * *Backward Breaking*: Renaming an attribute, deleting an attribute, or making an optional attribute mandatory.
   * *Forward Breaking*: Adding required attributes to producer payloads.
3. **Change Event Broadcast**: Emits semantic change notifications containing affected URIs to enable CodeMesh to run instant **cross-model blast-radius calculations**.

### FR-4: Data Classification, Privacy & Governance
1. Every logical attribute and physical field supports governance tagging:
   * **Sensitivity**: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED_PII`, `PCI_FINANCIAL`.
   * **Data Residency**: `EU_ONLY`, `US_EAST`, `GLOBAL`.
   * **Retention Policy**: `TTL_90_DAYS`, `INDEFINITE`, `LEGAL_HOLD`.
2. CodeMesh and Northstar use these tags to trigger **policy guardrails** (e.g., rejecting code that logs `RESTRICTED_PII` in plain text).

### FR-5: Invariant & Semantic Integrity Declarations
1. GroundTruth expresses machine-readable entity invariants:
   * **Range Constraints**: `0.0 <= discount_percentage <= 1.0`
   * **Relational Multiplicity**: `Order.items must have >= 1 LineItem`
   * **Cross-Attribute Constraints**: `Order.delivered_at >= Order.shipped_at >= Order.placed_at`
   * **State Transition Matrices**: `PENDING -> PAID -> SHIPPED` (Disallowing `CANCELLED -> PAID`).
2. These constraints are exposed so CodeMesh and Northstar can run them as **executable validation gates**.

### FR-6: Ingestion & Federation Adapters
GroundTruth ingests and bi-directionally syncs with standard enterprise schema sources:
* **Relational / Analytical DDL**: PostgreSQL, MySQL, Snowflake, BigQuery.
* **API & Wire Protocols**: OpenAPI 3.x specifications, Protobuf definitions, Apache Avro schemas.
* **Modern Code Models**: Pydantic models, SQLAlchemy declarative tables, dataclasses.
* **Enterprise Catalogs**: Alation, Collibra, Google Cloud Dataplex, Apache Atlas.

---

## 4. Query & Resolution API Specification

GroundTruth provides low-latency ($< 50\text{ms}$) APIs:

### A. `resolve_entity(uri: str) -> LogicalEntitySpec`
Returns full structured schema, types, descriptions, relationships, and invariants for a `data://logical/...` URI.

### B. `get_physical_realizations(logical_uri: str) -> List[PhysicalObjectSpec]`
Finds all physical database tables, indexes, Kafka topics, or parquet files realizing a given logical entity.

### C. `find_readers_and_writers(data_uri: str) -> CrossModelAccessReport`
Returns all CodeMesh symbols (`csi://...`) that have `READS`, `WRITES`, or `CREATES` relationships to this data entity.

### D. `validate_compatibility(proposed_schema: EntitySpec) -> CompatibilityReport`
Evaluates whether a proposed entity modification introduces breaking changes to existing computational readers or physical stores.
