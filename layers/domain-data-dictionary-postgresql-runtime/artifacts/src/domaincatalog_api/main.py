"""FastAPI application construction and operational health endpoints."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Protocol

from fastapi import FastAPI, Response, status
from psycopg import Error as PsycopgError
from psycopg_pool import PoolTimeout

from domaincatalog_api.database import Database
from domaincatalog_api.settings import Settings

LOGGER = logging.getLogger(__name__)


class DatabaseLifecycle(Protocol):
    """Minimal database behavior used by the operational API."""

    async def open(self) -> None: ...

    async def close(self) -> None: ...

    async def is_ready(self) -> bool: ...


def create_app(database: DatabaseLifecycle | None = None) -> FastAPI:
    """Construct the operational API without defining product capabilities."""

    runtime_database = database or Database(Settings.from_environment())

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await runtime_database.open()
        try:
            yield
        finally:
            await runtime_database.close()

    app = FastAPI(
        title="Domain Catalog API",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health/live", include_in_schema=False)
    async def live() -> dict[str, str]:
        return {"status": "live"}

    @app.get("/health/ready", include_in_schema=False)
    async def ready(response: Response) -> dict[str, str]:
        try:
            is_ready = await runtime_database.is_ready()
        except (PsycopgError, PoolTimeout, RuntimeError):
            LOGGER.warning("Database readiness check failed", exc_info=True)
            is_ready = False

        if not is_ready:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"status": "not_ready"}
        return {"status": "ready"}

    return app
