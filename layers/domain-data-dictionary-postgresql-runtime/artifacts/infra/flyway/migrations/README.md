# Product Migrations

This directory currently contains no SQL migrations and records the verified scaffold baseline. The owning runtime transform may now add `V*.sql` files derived from the selected `CAT-LOG` revision; no separately approved PostgreSQL physical-model artifact is required.

Versioned SQL uses:

```text
V<UTC timestamp>__<description>.sql
```

Applied migrations are immutable. Corrections roll forward through another versioned migration.

Every migration-created object and enforcement mechanism must appear in the derived realization manifest. Ordinary PostgreSQL choices belong to the transform; escalate only semantic weakening, competing authority, material external dependencies, major operational commitments, or upstream deficiencies.
