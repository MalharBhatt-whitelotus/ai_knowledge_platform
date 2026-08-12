import asyncio
import pytest


@pytest.mark.asyncio
async def test_file_upload_and_processing(
    http_client,
    auth_headers,
):
    files = {
        "file": (
            "integration_test.txt",
            b"This is an integration test document.",
            "text/plain",
        )
    }

    upload_response = await http_client.post(
        "http://localhost:8002/upload_file",
        files=files,
        headers=auth_headers,
    )

    assert upload_response.status_code in {200, 201}

    upload_data = upload_response.json()

    file_id = upload_data["file_id"]

    assert upload_data["status"] == "in_queue"

    # Wait for worker processing
    for _ in range(15):

        response = await http_client.get(
            f"http://localhost:8002/get_file/{file_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200

        data = response.json()

        if data["status"] == "completed":
            break

        await asyncio.sleep(2)

    else:
        pytest.fail(
            f"File {file_id} was not processed within timeout"
        )