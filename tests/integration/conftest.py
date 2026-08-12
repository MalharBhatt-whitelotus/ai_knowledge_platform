import pytest
import pytest_asyncio
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


@pytest_asyncio.fixture
async def http_client():
    async with httpx.AsyncClient(
        timeout=10.0
    ) as client:
        yield client

@pytest_asyncio.fixture
async def auth_headers(http_client):
    response = await http_client.post(
        "http://localhost:8001/login_user",
        json={
            "username": "mal1",
            "password": "Mal123!"
            },
    )

    assert response.status_code == 200
    data = response.json()
    token = data["token"]["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }