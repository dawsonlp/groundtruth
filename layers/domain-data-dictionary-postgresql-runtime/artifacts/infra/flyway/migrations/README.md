# Product Migrations

This directory intentionally contains no SQL migrations. Do not add a `V*.sql` file until an accepted PostgreSQL `CAT-PHY` artifact traces every product object to the logical model.

When that gate is satisfied, versioned SQL uses:

```text
V<UTC timestamp>__<description>.sql
```

Applied migrations are immutable. Corrections roll forward through another versioned migration.
