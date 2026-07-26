# Agent Instructions

Before working in this repository, read [README.md](README.md), especially **Working With This Project**, and the governing [ADR 0001](../../adr/0001-organize-product-refinement-as-flat-layer-graph.md).

Before changing files, state:

- the selected refinement branch;
- the latest effective layer on that branch;
- the layer or transform that owns the requested change; and
- the downstream layers expected to become stale.

For build requests, follow the README's build procedure. For update requests, follow its update procedure.

Do not:

- invent a missing transform or required human decision;
- choose among alternative implementations without direction;
- create a child layer without a source-colocated transform specification;
- edit a downstream layer so it contradicts its source; or
- treat generated output as effective before its validation conditions pass.

Critique, review, and test evidence belong with the relevant transform or change record. They are not product layers.
