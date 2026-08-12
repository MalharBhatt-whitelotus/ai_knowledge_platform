from locust import HttpUser, task, between


class FileUploadUser(HttpUser):
    host = "http://localhost:8002"
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "http://localhost:8001/login_user",
            json={
                "username": "mal1",
                "password": "Mal123!",
            },
            name="/login_user",
        )

        response.raise_for_status()

        token = response.json()["token"]["access_token"]

        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    @task
    def upload_file(self):
        files = {
            "file": (
                "load_test.txt",
                b"FastAPI is a modern Python web framework for building APIs.",
                "text/plain",
            )
        }

        with self.client.post(
            "/upload_file",
            files=files,
            headers=self.headers,
            name="/upload_file",
            catch_response=True,
        ) as response:

            if response.status_code not in (200, 201):
                response.failure(
                    f"Upload failed: {response.status_code} {response.text}"
                )