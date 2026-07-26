# Domain Catalog

This project is the first test case for the flat product-refinement layout proposed in [ADR 0001](../../adr/0001-organize-product-refinement-as-flat-layer-graph.md).

## Project Decisions

- [Domain Catalog ADR 0001](adr/0001-require-mof-conformance-for-the-governing-model-definition.md): require the governing model definition to conform to MOF. Direct CMOF use is now being tested by the first draft refinement but is not yet accepted.

## Current Product Layer

The current source layer is `product-conception`.

Its product artifact is [product-investigation.md](layers/product-conception/artifacts/product-investigation.md).

The artifact remains a draft. A draft outbound transform now produces the sibling `data-modeling-definition` layer, but neither the source nor the target has been accepted as effective.

The draft target artifact is [data-modeling-language.md](layers/data-modeling-definition/artifacts/data-modeling-language.md). It is authoritative for the language's OMG, ISO, and DAMA standards profile. Its owning [transform](layers/product-conception/transforms/data-modeling-definition/transform.md) records the supporting standards evidence, CMOF fit assessment, worked example, and remaining validation conditions.

Use the target artifact's **Canonical Model and Artifact Registry** when referring to the model stack. In particular, distinguish the MOF specification (`MOF-SPEC`) from its Complete MOF governing model (`CMOF-GOV`), the data-modeling definition (`DML-*`) from particular business models (`BDM-*`), and the catalog repository (`CAT-*`) from subject-system deployment and data.

A provisional child layer now contains the draft [Domain Data Dictionary component design](layers/domain-data-dictionary-component/artifacts/component-design.md). The product owner selected Model C, required PostgreSQL as the first physical deployment target, and directed a common capability API for machine and human-facing clients. Its source-colocated [transform](layers/data-modeling-definition/transforms/domain-data-dictionary-component/transform.md) records the design assignment, governing constraints, and incomplete validation state. The design remains non-effective because its source and upstream evidence are incomplete.

## Layout

```text
layers/
├── product-conception/
│   ├── artifacts/
│   │   └── product-investigation.md
│   └── transforms/
│       └── data-modeling-definition/
│           ├── transform.md
│           ├── standards-assessment.md
│           ├── cmof-fit-assessment.md
│           └── worked-example.md
├── data-modeling-definition/
│   ├── artifacts/
│   │   └── data-modeling-language.md
│   └── transforms/
│       └── domain-data-dictionary-component/
│           └── transform.md
├── domain-data-dictionary-component/
│   ├── README.md
│   ├── artifacts/
│   │   └── component-design.md
│   └── transforms/
│       └── domain-data-dictionary-conceptual-model/
│           └── transform.md
├── domain-data-dictionary-conceptual-model/
│   ├── README.md
│   ├── artifacts/
│   │   ├── build-design.md
│   │   └── conceptual-data-model.md
│   └── transforms/
│       └── domain-data-dictionary-logical-model/
│           └── transform.md
├── domain-data-dictionary-logical-model/
│   ├── README.md
│   ├── artifacts/
│   │   ├── logical-design.md
│   │   └── logical-data-model.md
│   └── transforms/
│       └── domain-data-dictionary-postgresql-design/
│           ├── transform.md
│           └── migration-tool-assessment.md
├── domain-data-dictionary-postgresql-design/
│   ├── README.md
│   ├── artifacts/
│   │   ├── technical-design.md
│   │   └── development-checklist.md
│   └── transforms/
│       └── domain-data-dictionary-postgresql-runtime/
│           └── transform.md
└── domain-data-dictionary-postgresql-runtime/
    ├── README.md
    ├── artifacts/
    │   ├── pyproject.toml
    │   ├── compose.yaml
    │   ├── Dockerfile
    │   ├── src/
    │   ├── tests/
    │   └── infra/
    └── evidence/
        └── scaffold-verification.md
```

- `artifacts/` contains the product as expressed at this refinement level.
- `transforms/` will contain specifications for producing more concrete sibling layers under `layers/`.
- Alternative implementations will be separate sibling layers rather than nested descendants or version directories.

The Model C design now has a conceptual refinement and a draft logical refinement in [logical-design.md](layers/domain-data-dictionary-logical-model/artifacts/logical-design.md) and [logical-data-model.md](layers/domain-data-dictionary-logical-model/artifacts/logical-data-model.md). The logical model selects a hybrid catalog kernel: typed authority for catalog-specific governance records, reflective authority for CMOF/DML model objects, and derived typed projections over those objects.

The PostgreSQL implementation branch now has an architect-approved [technical design](layers/domain-data-dictionary-postgresql-design/artifacts/technical-design.md) and an active [engineer development checklist](layers/domain-data-dictionary-postgresql-design/artifacts/development-checklist.md). They select the pinned local PostgreSQL 18.4 image, a three-service Compose topology, Flyway-managed SQL migrations, and a separately built Python 3.14/FastAPI service using uv and Psycopg 3. The architect resolved the runtime artifact boundary: the uv root is `layers/domain-data-dictionary-postgresql-runtime/artifacts/`, owned by a named runnable sibling layer and a source-colocated transform. `CAT-LOG` is the semantic source for the PostgreSQL realization; migration SQL is executable physical authority, with a derived traceability manifest and deployed inventory as evidence rather than a separately approved physical model. The operational scaffold is verified, and product migrations are the next runtime-transform work. The runtime remains an exploratory descendant because no upstream layer is effective.

Conceptual refinement places explicit model-family membership, responsible agents, and provenance records in `CAT-CON` as catalog business concepts governed by `DML-CON`; it does not promote them into the general language without evidence that they are general concerns. The canonical registry still requires provisional `CAT-FAMILY`, `CAT-CON`, and `CAT-LOG` role names to be accepted or replaced. Draft refinement may continue, but affected descendants require regeneration after an upstream naming or semantic correction. The source definition also still requires DAMA and normative-standard verification, OCL encoding and evaluation boundaries, representative physical-model tests, a complete RDBMS metadata inventory, a lossless repository round-trip prototype, machine-readable CMOF/XMI validation, and the follow-up decision on direct CMOF use.

## Working With This Project

### Effective layers

The source layer is effective when its artifact has been accepted. A derived layer is effective when it:

- was produced from the current accepted revisions of its source artifacts;
- was produced by the current accepted transform specification;
- passed that transform's validation conditions; and
- has not been invalidated by a change to an upstream layer or transform.

The **latest effective layer** is the most concrete effective layer on a selected refinement branch. Different implementation branches may therefore have different latest effective layers.

Directory depth, modification time, and Git commit order do not determine which layer is effective.

### Exploratory refinement from draft layers

Effectiveness controls whether a layer is accepted as a reliable source for a build or further accepted refinement. It does not control whether exploratory downstream work may be created.

A draft layer may be used as the source of another draft layer in order to test the model against more concrete design and implementation. The descendant must:

- identify the exact source revision and transform used;
- remain explicitly draft and non-effective;
- record unresolved upstream gaps and any provisional assumptions used to continue; and
- avoid converting a provisional assumption into upstream authority merely because code or a concrete artifact now depends on it.

Discovery of an upstream shortcoming does not require all downstream exploration to stop. Work may continue to expose additional consequences and test candidate realizations. When the upstream layer is corrected, every affected descendant becomes stale and must be regenerated in transform order before the branch can become effective.

### Building the product

To build or run the product from an effective branch:

1. Select the intended implementation branch. If several alternatives exist and none was requested, do not choose one implicitly.
2. Follow the branch's transform references to find its latest effective layer.
3. Check whether that layer is runnable.
4. If it is not runnable, execute its accepted outbound transform to produce the next layer. The transform specification must provide its required inputs, procedure or command, expected artifacts, and validation conditions.
5. Validate the generated layer before treating it as effective.
6. Repeat the transform-and-validate process until reaching a runnable layer.
7. Follow the runnable layer's own build and execution instructions.

Do not invent a missing transform, silently select an implementation branch, or treat an unvalidated generated layer as effective. If no accepted path reaches a runnable layer, report that no effective build is available and identify the missing transform or decision.

An exploratory build may instead follow a deliberately selected draft branch. Execute its recorded draft transforms, identify every exact source revision, validate what can be validated, and carry unresolved gaps and provisional assumptions into the runnable descendant. The result remains a draft experiment rather than an effective product build, but creating and running it is permitted and is expected to provide evidence for upstream revision.

This project is currently **not buildable as an effective product**: no layer is effective and the draft transforms have unmet validation conditions. A recorded exploratory branch does reach a runnable PostgreSQL/API scaffold; follow the runtime-layer instructions to build it, while retaining its draft and non-effective status. PostgreSQL product migrations and logical round-trip validation remain incomplete.

### Updating the product

To make a product change:

1. Describe the semantic change before selecting files to edit.
2. Find the least concrete layer that owns the decision being changed. A visible defect in a downstream layer may originate in an upstream artifact, the transform, a human input to the transform, or generation that failed to follow valid inputs.
3. Create a Git branch or worktree from the last accepted state. If no accepted state exists, or the purpose is explicitly exploratory refinement, start from the exact recorded draft revision and keep the resulting branch non-effective.
4. Change the owning layer artifact, transform specification, or recorded human input. Do not repair only a downstream symptom while leaving its source contradictory.
5. Identify affected descendants by following outbound transform references. Unrelated sibling implementations remain unchanged unless they consume the changed source.
6. Treat each affected descendant as stale until it has been regenerated from the new source revision and validated.
7. Apply each succeeding transform in order along every affected branch, validating each output before using it as the source for the next transform.
8. Build and test the resulting runnable layer.
9. Review the complete change and merge it only after product intent, transformation fidelity, and runnable behavior agree.

If a change applies only to an implementation and does not alter an upstream contract, it belongs in that implementation layer. If implementation work exposes a faulty upstream assumption, restart from the layer that owns that assumption and propagate the correction downward.
