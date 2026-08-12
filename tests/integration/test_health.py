import pytest


@pytest.mark.asyncio
async def test_all_services_are_healthy(
    http_client,
    service_urls,
):

    for service, base_url in service_urls.items():

        response = await http_client.get(
            f"{base_url}/health"
        )

        assert response.status_code == 200, (
            f"{service} healthcheck failed: "
            f"{response.text}"
        )

        data = response.json()

        assert data["status"] == "healthy"