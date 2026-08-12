from locust import HttpUser, task, between


class RagUser(HttpUser):
    host = "http://localhost:8005"
    wait_time = between(2, 5)

    @task
    def ask_rag(self):
        with self.client.post(
            "/ask",
            json={
                "question": "What is FastAPI?",
                "top_k": 5,
            },
            name="/ask",
            catch_response=True,
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"RAG failed: {response.status_code} "
                    f"{response.text}"
                )
                return

            data = response.json()

            if not data.get("answer"):
                response.failure("RAG returned an empty answer")