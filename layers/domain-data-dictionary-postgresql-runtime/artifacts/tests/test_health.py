"""Operational health behavior without a live database."""

import pytest
from httpx import ASGITransport, AsyncClient

from domaincatalog_api.main import create_app


class FakeDatabase:
    def __init__(self, *, ready: bool) -> None:
        self.ready = ready
        self.opened = False
        self.closed = False

    async def open(self) -> None:
        self.opened = True

    async def close(self) -> None:
        self.closed = True

    async def is_ready(self) -> bool:
        return self.ready


async def request(database: FakeDatabase, path: str) -> tuple[int, dict[str, str]]:
    app = create_app(database)
    async with (
        app.router.lifespan_context(app),
        AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client,
    ):
        response = await client.get(path)
    return response.status_code, response.json()


@pytest.mark.asyncio
async def test_liveness_does_not_depend_on_database_readiness() -> None:
    database = FakeDatabase(ready=False)
    status_code, body = await request(database, "/health/live")

    assert status_code == 200
    assert body == {"status": "live"}
    assert database.opened
    assert database.closed


@pytest.mark.asyncio
async def test_readiness_reports_ready() -> None:
    status_code, body = await request(FakeDatabase(ready=True), "/health/ready")

    assert status_code == 200
    assert body == {"status": "ready"}


@pytest.mark.asyncio
async def test_readiness_reports_unavailable() -> None:
    status_code, body = await request(FakeDatabase(ready=False), "/health/ready")

    assert status_code == 503
    assert body == {"status": "not_ready"}
