"""Database lifecycle and transaction tests against the Compose PostgreSQL service."""

import os

import pytest

from domaincatalog_api.database import Database
from domaincatalog_api.settings import Settings

pytestmark = pytest.mark.skipif(
    os.getenv("DOMAINCATALOG_INTEGRATION") != "1",
    reason="set DOMAINCATALOG_INTEGRATION=1 to run database integration tests",
)


@pytest.fixture
def settings() -> Settings:
    return Settings.from_environment().model_copy(
        update={"pool_min_size": 1, "pool_max_size": 1}
    )


@pytest.mark.asyncio
async def test_pool_lifecycle_and_flyway_readiness(settings: Settings) -> None:
    database = Database(settings)
    await database.open()
    try:
        assert await database.is_ready()
    finally:
        await database.close()


@pytest.mark.asyncio
async def test_connection_commits_and_rolls_back(settings: Settings) -> None:
    database = Database(settings)
    await database.open()
    try:
        async with database.connection() as connection:
            await connection.execute("CREATE TEMP TABLE transaction_probe (value integer NOT NULL)")
            await connection.execute("INSERT INTO transaction_probe (value) VALUES (1)")

        with pytest.raises(RuntimeError, match="force rollback"):
            async with database.connection() as connection:
                await connection.execute("INSERT INTO transaction_probe (value) VALUES (2)")
                raise RuntimeError("force rollback")

        async with database.connection() as connection:
            cursor = await connection.execute("SELECT value FROM transaction_probe ORDER BY value")
            values = [row[0] async for row in cursor]

        assert values == [1]
    finally:
        await database.close()
