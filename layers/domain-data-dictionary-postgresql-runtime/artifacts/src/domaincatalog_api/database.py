"""Psycopg connection-pool lifecycle and transaction boundary."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from psycopg import AsyncConnection, sql
from psycopg_pool import AsyncConnectionPool

from domaincatalog_api.settings import Settings


class Database:
    """Own the process connection pool and its transaction contexts."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._pool: AsyncConnectionPool[AsyncConnection[tuple[Any, ...]]] = AsyncConnectionPool(
            conninfo=settings.database_conninfo,
            min_size=settings.pool_min_size,
            max_size=settings.pool_max_size,
            timeout=settings.pool_timeout_seconds,
            max_lifetime=settings.pool_max_lifetime_seconds,
            open=False,
        )

    async def open(self) -> None:
        """Open the pool and prove that its minimum connections are available."""

        await self._pool.open(wait=True)

    async def close(self) -> None:
        """Close the pool and its connections."""

        await self._pool.close()

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[AsyncConnection[tuple[Any, ...]]]:
        """Provide one connection with commit-on-success and rollback-on-error."""

        async with self._pool.connection() as connection:
            yield connection

    async def is_ready(self) -> bool:
        """Check database reachability and the expected Flyway history relation."""

        schema_name, relation_name = self._settings.flyway_history_relation.split(".", 1)
        qualified_relation = sql.Identifier(schema_name, relation_name).as_string()
        async with self.connection() as connection:
            cursor = await connection.execute("SELECT to_regclass(%s)", (qualified_relation,))
            row = await cursor.fetchone()
        return row is not None and row[0] is not None
