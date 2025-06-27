import random
from locust import HttpUser, task, between


class EventUser(HttpUser):
    wait_time = between(1, 2)
    # url_prefix = "/api/v1/"

    @task(3)
    def browse_events(self):
        self.client.get("/api/v1/event/events/", name="/event")

    @task(1)
    def browse_event_detail(self):
        id = random.choice(self.event_ids)

        self.client.get(f"/api/v1/event/events/{id}", name="/event_detail")

    def on_start(self) -> None:
        response = self.client.get("/api/v1/event/events/")
        data = response.json()
        events = data.get("results", [])
        self.event_ids = [event["id"] for event in events]
