# Domain Catalog

This project is the first test case for the flat product-refinement layout proposed in [ADR 0001](../../adr/0001-organize-product-refinement-as-flat-layer-graph.md).

## Current Product Layer

The current source layer is `product-conception`.

Its product artifact is [product-investigation.md](layers/product-conception/artifacts/product-investigation.md).

The artifact remains a draft. No outbound refinement transform or child product layer has been accepted yet.

## Layout

```text
layers/
└── product-conception/
    ├── artifacts/
    │   └── product-investigation.md
    └── transforms/
```

- `artifacts/` contains the product as expressed at this refinement level.
- `transforms/` will contain specifications for producing more concrete sibling layers under `layers/`.
- Alternative implementations will be separate sibling layers rather than nested descendants or version directories.

The next step is to agree on the first target layer and its transform before creating either one.

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

This project is currently **not buildable**: `product-conception` is its only layer and it has no accepted outbound transform.

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
