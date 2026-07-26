# PostgreSQL Initialization Shadow

This documentation-only directory is mounted over `/docker-entrypoint-initdb.d`.

It deliberately suppresses the batteries-included image's automatic extension activation and demonstration objects. Do not add executable `.sql` or `.sh` files here. All accepted database changes belong in Flyway migrations derived from `CAT-LOG` through the owning runtime transform.
