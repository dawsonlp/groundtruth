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

A provisional child layer has been scaffolded for the first deployable component. Its [layer README](layers/domain-data-dictionary-component/README.md) reserves the target structure, while its source-colocated [transform](layers/data-modeling-definition/transforms/domain-data-dictionary-component/transform.md) records the design assignment and governing constraints. The transform has not been executed and no component design exists yet.

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
└── domain-data-dictionary-component/
    ├── README.md
    └── artifacts/                     # component-design.md is the next output
```

- `artifacts/` contains the product as expressed at this refinement level.
- `transforms/` will contain specifications for producing more concrete sibling layers under `layers/`.
- Alternative implementations will be separate sibling layers rather than nested descendants or version directories.

The next component step is to execute the new transform by writing `layers/domain-data-dictionary-component/artifacts/component-design.md`. That design must remain provisional while its source is draft. In parallel, the source definition still requires DAMA and normative-standard verification, OCL encoding and evaluation boundaries, representative physical-model tests, a complete RDBMS metadata inventory, a lossless repository round-trip prototype, machine-readable CMOF/XMI validation, and the follow-up decision on direct CMOF use.

## Working With This Project

### Effective layers

The source layer is effective when its artifact has been accepted. A derived layer is effective when it:

- was produced from the current accepted revisions of its source artifacts;
- was produced by the current accepted transform specification;
- passed that transform's validation conditions; and
- has not been invalidated by a change to an upstream layer or transform.

The **latest effective layer** is the most concrete effective layer on a selected refinement branch. Different implementation branches may therefore have different latest effective layers.

Directory depth, modification time, and Git commit order do not determine which layer is effective.

### Building the product

To build or run the product:

1. Select the intended implementation branch. If several alternatives exist and none was requested, do not choose one implicitly.
2. Follow the branch's transform references to find its latest effective layer.
3. Check whether that layer is runnable.
4. If it is not runnable, execute its accepted outbound transform to produce the next layer. The transform specification must provide its required inputs, procedure or command, expected artifacts, and validation conditions.
5. Validate the generated layer before treating it as effective.
6. Repeat the transform-and-validate process until reaching a runnable layer.
7. Follow the runnable layer's own build and execution instructions.

Do not invent a missing transform, silently select an implementation branch, or treat an unvalidated generated layer as effective. If no accepted path reaches a runnable layer, report that the product is not yet buildable and identify the missing transform or decision.

This project is currently **not buildable**: no layer is effective, both draft transforms have unmet validation conditions, and no accepted path reaches a runnable layer.

### Updating the product

To make a product change:

1. Describe the semantic change before selecting files to edit.
2. Find the least concrete layer that owns the decision being changed. A visible defect in a downstream layer may originate in an upstream artifact, the transform, a human input to the transform, or generation that failed to follow valid inputs.
3. Create a Git branch or worktree from the last accepted state.
4. Change the owning layer artifact, transform specification, or recorded human input. Do not repair only a downstream symptom while leaving its source contradictory.
5. Identify affected descendants by following outbound transform references. Unrelated sibling implementations remain unchanged unless they consume the changed source.
6. Treat each affected descendant as stale until it has been regenerated from the new source revision and validated.
7. Apply each succeeding transform in order along every affected branch, validating each output before using it as the source for the next transform.
8. Build and test the resulting runnable layer.
9. Review the complete change and merge it only after product intent, transformation fidelity, and runnable behavior agree.

If a change applies only to an implementation and does not alter an upstream contract, it belongs in that implementation layer. If implementation work exposes a faulty upstream assumption, restart from the layer that owns that assumption and propagate the correction downward.
