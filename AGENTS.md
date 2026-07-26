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

Non-effectiveness does not block exploratory refinement. A draft layer may be used to create further draft descendants when the applicable transform exists, the exact source revision is recorded, and unresolved assumptions or upstream gaps remain explicit. Continuing downstream is a way to expose weaknesses in earlier layers, not a claim that those layers are accepted.

When an upstream correction is later made, follow the transform graph, treat affected descendants as stale, and regenerate them in order before accepting or relying on the corrected branch as effective.

Critique, review, and test evidence belong with the relevant transform or change record. They are not product layers.
