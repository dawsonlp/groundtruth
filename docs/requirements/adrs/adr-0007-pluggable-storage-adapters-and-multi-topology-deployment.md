# ADR 0007: Pluggable Storage Adapters and Multi-Topology Deployment Architecture 🏛️

- **URI**: `decision://arch/adr-0007-pluggable-storage-adapters-and-multi-topology-deployment`
- **Status**: `ACTIVE`

## 1. Context and Problem Statement
Northstar serves diverse user personas across multiple operational contexts:
1. **Local AI Coding Agents & Developers**: Require zero-network, sub-millisecond in-process graph queries during active code mutation and CI pre-commit checks.
2. **Human Stakeholders & Product Owners**: Require interactive web portals to inspect requirements, participate in elicitation interviews, verify intent completeness, and track solution development stages.
3. **Enterprise Teams & Compliance Auditors**: Require centralized, multi-user intent repositories with real-time synchronization, access control, and audit logs.

If Northstar couples its domain model (`CapabilitySpec`, `IntentGraph`, `OperationalContract`) to a single storage mechanism (e.g. only Git YAML files or only a remote database), it either creates heavy database setup friction for local developers or denies rich collaborative web tooling to business stakeholders.

---

## 2. Decision Outcome
: Hexagonal Ports-and-Adapters Architecture

We establish that the **Northstar Core Domain Model is strictly storage- and deployment-agnostic**, using a **Ports-and-Adapters (Hexagonal)** architecture:

```
                                  ┌─────────────────────────────────────────────────────────┐
                                  │                PURE CORE DOMAIN MODEL                   │
                                  │                  (src/northstar/core)                   │
                                  │                                                         │
                                  │   • IntentGraph (Entities, Nodes, Relational Edges)     │
                                  │   • CapabilitySpec, ComponentSpec, DecisionSpec         │
                                  │   • InvariantEngine & Closure Resolution                │
                                  └────────────────────────────┬────────────────────────────┘
                                                               │
                                       ┌───────────────────────┴───────────────────────┐
                                       │        STORAGE & DEPLOYMENT PORTS             │
                                       │         (IntentRepository Interface)          │
                                       └───────────────────────┬───────────────────────┘
                                                               │
                    ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
                    ▼                                          ▼                                          ▼
┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐
│       ADAPTER 1: LOCAL GIT/YAML      │    │      ADAPTER 2: EMBEDDED SQLITE      │    │    ADAPTER 3: HOSTED SERVICE + DB    │
│            (File-Backed)             │    │            (Single-File)             │    │     (PostgreSQL / Graph DB + API)    │
├──────────────────────────────────────┤    ├──────────────────────────────────────┤    ├──────────────────────────────────────┤
│ • intent/**/*.yaml manifests         │    │ • .northstar/catalog.sqlite3         │    │ • Centralized Enterprise Catalog     │
│ • adrs/*.md files                    │    │ • Zero-config local querying         │    │ • Multi-user real-time sync          │
│ • .northstar/links.yaml sidecar      │    │ • Lightning-fast local cache         │    │ • REST / GraphQL / WebSockets API    │
│ • Optimal for offline Git & CI       │    │ • Optimal for IDE extensions         │    │ • Powers Solution Control Plane Web  │
└──────────────────────────────────────┘    └──────────────────────────────────────┘    └──────────────────────────────────────┘
```

---

## 3. Consequences

### Positive Consequences
- *(None recorded)*

### Negative Consequences / Trade-offs
- *(None recorded)*
