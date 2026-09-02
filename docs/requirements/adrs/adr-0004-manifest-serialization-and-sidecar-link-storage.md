# ADR 0004: Intent Manifest File Layout and Sidecar Link Storage 🏛️

- **URI**: `decision://arch/adr-0004-manifest-serialization-and-sidecar-link-storage`
- **Status**: `ACTIVE`

## 1. Context and Problem Statement
For Northstar to function in local developer environments, CI/CD pipelines, and git-managed codebases without requiring a dedicated external database server, we must define:
1. How intent nodes (`component://`, `req://`, `decision://`, `constraint://`, `policy://`) serialize to files on disk.
2. How cross-ontology relational links connecting CodeMesh symbols (`csi://...`), GroundTruth entities (`data://...`), and Northstar intent nodes (`req://...`) are stored and versioned.

Embedding relational links directly inside application source code docstrings (e.g. `# @satisfies(req://payments/charge-card)`) creates invasive code churn and requires parsing thousands of source files to discover intent links. Conversely, storing links in an external remote database disconnects intent from Git branch history.

---

## 2. Decision Outcome
We establish the standard file layout and sidecar link storage model for Northstar:

### 2.1 File-System Manifest Layout

Repository root directories store intent artifacts under a structured `intent/` directory and standard `adrs/` directory:

```text
repository-root/
├── adrs/                                      # Architectural Decision Records (MADR Markdown)
│   ├── 0001-intent-authority-ontology.md
│   └── 0004-redis-idempotency.md
│
├── intent/                                    # Machine-Authorable Intent Manifests (YAML)
│   ├── components/
│   │   ├── payments.yaml                      # ComponentSpec (Exported/Required interfaces)
│   │   └── inventory.yaml
│   ├── capabilities/
│   │   ├── payments/
│   │   │   ├── charge_card.yaml               # CapabilitySpec (OperationalContract, Errors)
│   │   │   └── refund_charge.yaml
│   │   └── inventory/
│   │       └── reserve_stock.yaml
│   ├── workflows/
│   │   └── order_checkout_saga.yaml           # WorkflowSpec (Multi-step saga choreography)
│   ├── constraints/
│   │   ├── architectural_boundaries.yaml      # InvariantSpec (Boundary rules & AST patterns)
│   │   └── mandatory_decorators.yaml
│   └── policies/
│       └── pci_dss_cardholder_data.yaml       # PolicySpec (Compliance mandates)
│
└── .northstar/                                # Sidecar Metadata & Link Cache
    └── links.yaml                             # Cross-Ontology Relational Graph Edges
```

---

### 2.2 Sidecar Link Manifest (`.northstar/links.yaml`)

Cross-ontology relationships are stored in a centralized, Git-versioned **Sidecar Link Manifest** at `.northstar/links.yaml` (or `.codemesh/links.yaml`):

```yaml
version: "1.0"
updated_at: "2026-09-02T09:15:00Z"
edges:
  - source: "csi://payments/services/PaymentService.charge"
    verb: "SATISFIES"
    target: "req://payments/charge-card"
    provenance:
      tier: "DECLARED"
      author: "Larry Dawson"
      confidence: 1.0

  - source: "req://payments/charge-card"
    verb: "OPERATES_ON"
    target: "data://logical/payments/PaymentTransaction"
    provenance:
      tier: "DECLARED"

  - source: "constraint://payments/require-idempotent-decorator"
    verb: "CONSTRAINS"
    target: "csi://payments/services/PaymentService.charge"
    provenance:
      tier: "DERIVED"
```

---

## 3. Consequences

### Positive Consequences
- *(None recorded)*

### Negative Consequences / Trade-offs
- *(None recorded)*
