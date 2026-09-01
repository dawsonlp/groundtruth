# Domain Data Dictionary Capability API Architecture

## Status

- Status: first draft produced for review
- Effective: no
- Primary source layer: `domain-data-dictionary-logical-model`
- Semantic source revision: `5728636`
- Product-owner decision supplement: 2026-07-28
- Owning transform: [domain-data-dictionary-capability-api-architecture](../domain-data-dictionary-logical-model/transforms/domain-data-dictionary-capability-api-architecture/transform.md)
- Product artifact: [architecture.md](artifacts/architecture.md)

## Purpose

Define the client-independent capability boundary over the hybrid catalog kernel. The architecture makes typed semantic behavior available to machine and human-facing clients, keeps user interfaces thin, and uses self-modeling plus observation of the local PostgreSQL runtime as the first end-to-end test.

## Boundary

This layer defines architecture, not endpoint paths, wire schemas, UI technology, technical design, or implementation code. It remains exploratory because its source layers are not effective and its review conditions are incomplete.
