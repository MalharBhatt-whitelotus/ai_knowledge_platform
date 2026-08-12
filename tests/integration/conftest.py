import pytest
import httpx


SERVICES = {
    "gateway": "http://localhost:8000",
    "auth": "http://localhost:8001",
    "file": "http://localhost:8002",
    "embedding": "http://localhost:8003",
    "search": "http://localhost:8004",
    "ai": "http://localhost:8005",
}


@pytest.fixture
def service_urls():
    return SERVICES


@pytest.fixture
async def http_client():
    async with httpx.AsyncClient(
        timeout=10.0
    ) as client:
        yield client