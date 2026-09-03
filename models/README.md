# ⚠️ GroundTruth Data Model Snapshots

> **DO NOT EDIT FILES IN THIS DIRECTORY DIRECTLY**
> 
> Per **ADR 0006 (API-First Authority Access and Automated Snapshot Exports)**, the running **GroundTruth Service (`http://localhost:9481`)** backed by PostgreSQL (`groundtruth_catalog`) is the **authoritative System of Record** for all conceptual terms, logical entities, state machines, and DDL schemas.
>
> All files in this directory are deterministic **export snapshots**.

---

## How to Query and Mutate Data Models

- **CLI**: `./bin/tripartite data solutions --tenant tripartite`
- **Terms**: `./bin/tripartite data terms`
- **Entities**: `./bin/tripartite data entities`
- **DDL Projection**: `./bin/tripartite data ddl ecommerce`
- **API**: `http://localhost:9481/api/v1/...`
- **Web UI**: `http://localhost:9400`
