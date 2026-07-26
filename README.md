# Domain Catalog

This project is the first test case for the flat product-refinement layout proposed in [ADR 0001](../../adr/0001-organize-product-refinement-as-flat-layer-graph.md).

## Current Product Layer

The current source layer is `product-conception`.

Its product artifact is [product-investigation.md](layers/product-conception/artifacts/product-investigation.md).

No outbound refinement transform or child product layer has been accepted yet.

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
