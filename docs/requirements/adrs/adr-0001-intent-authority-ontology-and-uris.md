# ADR 0001: Intent Authority Entity Hierarchy & Canonical URI Addressing 🏛️

- **URI**: `decision://arch/adr-0001-intent-authority-ontology-and-uris`
- **Status**: `ACTIVE`

## 1. Context and Problem Statement
In autonomous AI software engineering, reasoning about code in isolation leads to architectural drift, fragile patches, and violation of business rules. To form a complete semantic federation, we need an authoritative domain responsible for capturing human purpose, architectural choices, and compliance boundaries without conflating them with code syntax or data storage.

## 2. Decision Outcome
Drivers

* Clear separation of concerns between Computation (`codemesh`), Information (`groundtruth`), and Intent (`northstar`).
* Deterministic, machine-queryable URI addressing across all requirements and governance artifacts.
* Support for multi-tiered provenance (`DECLARED`, `DERIVED`, `INFERRED`).

## 3. Consequences

### Positive Consequences
- *(None recorded)*

### Negative Consequences / Trade-offs
- *(None recorded)*
