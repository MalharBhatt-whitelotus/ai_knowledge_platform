from locust import HttpUser, task, between


class ApiUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3)

    @task
    def health_check(self):
        self.client.get("/health")