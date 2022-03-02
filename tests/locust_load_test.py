from locust import HttpUser, TaskSet, task


class BookstoreLocustTasks(TaskSet):
    @task
    def token_test(self):
        self.client.post("/token", dict(username="test", password="test"))

    @task
    def test_post_user(self):
        user_dict = {
            "name": "personel1",
            "password": "pass1",
            "role": "admin",
            "mail": "a@b.com"
        }
        auth_header = {"Authorization": "Bearer token"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)

class BookstoreLoadTest(HttpUser):
    tasks = [BookstoreLocustTasks]
    host = "http://localhost:8000"

