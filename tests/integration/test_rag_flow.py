import asyncio
from io import BytesIO

import pytest


@pytest.mark.asyncio
async def test_rag_pipeline(
    http_client,
    auth_headers,
):
    # --------------------------------------------------
    # 1. Upload a document
    # --------------------------------------------------

    content = b"""
    FastAPI is a modern Python web framework for building APIs.
    It is based on Starlette for web functionality and Pydantic
    for data validation. FastAPI supports asynchronous programming
    and automatically generates OpenAPI documentation.
    """

    files = {
        "file": (
            "rag_test.txt",
            BytesIO(content),
            "text/plain",
        )
    }

    upload_response = await http_client.post(
        "http://localhost:8002/upload_file",
        files=files,
        headers=auth_headers,
    )

    assert upload_response.status_code == 201, (
        f"Upload failed: {upload_response.text}"
    )

    upload_data = upload_response.json()

    file_id = upload_data["file_id"]

    assert upload_data["status"] == "in_queue"

    # --------------------------------------------------
    # 2. Wait for worker processing
    # --------------------------------------------------

    for _ in range(15):
        response = await http_client.get(
            f"http://localhost:8002/get_file/{file_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200, (
            f"Failed to get file: {response.text}"
        )

        file_data = response.json()

        status = file_data["status"]

        if status == "completed":
            break

        if status == "rejected":
            pytest.fail(
                f"File processing was rejected: {file_data}"
            )

        await asyncio.sleep(2)

    else:
        pytest.fail(
            f"File {file_id} did not complete processing"
        )

    # --------------------------------------------------
    # 3. Ask question through RAG
    # --------------------------------------------------

    ai_response = await http_client.post(
        "http://localhost:8005/ask",
        json={
            "question": "What is FastAPI?",
            "top_k": 5,
        },
    )

    assert ai_response.status_code == 200, (
        f"AI request failed: {ai_response.text}"
    )

    data = ai_response.json()

    # --------------------------------------------------
    # 4. Validate AI response
    # --------------------------------------------------

    assert data["question"] == "What is FastAPI?"

    assert isinstance(data["answer"], str)

    assert "FastAPI" in data["answer"]
    assert "Starlette" in data["answer"]
    assert "Pydantic" in data["answer"]