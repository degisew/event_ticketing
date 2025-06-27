import random
from locust import HttpUser, task, between


class EventUser(HttpUser):

    wait_time = between(1, 2)

    EVENT_IDS = [
        "9cfac9c3-2568-4593-8bd1-c8d6daa09ad7"
    ]

    def on_start(self) -> None:
        response = self.client.post(
            "/api/v1/auth/login/",
            json={
                "email": "admin@gmail.com",
                "password": 1234
            }
        )

        token = response.json().get("access")
        if token:
            self.client.headers.update({
                "Authorization": f"Bearer {token}"
            })

        response = self.client.get("/api/v1/event/events/")
        data = response.json()
        events = data.get("results", [])
        self.event_ids = [event["id"] for event in events]

    @task(3)
    def browse_events(self):
        self.client.get("/api/v1/event/events/", name="/event")

    @task(1)
    def browse_event_detail(self):
        id = random.choice(self.EVENT_IDS)

        self.client.get(f"/api/v1/event/events/{id}", name="/event_detail")

    @task
    def browse_ticket_types(self):
        self.client.get("/api/v1/event/ticket_types/", name="/ticket_type")

    @task
    def browse_reservations(self):
        self.client.get("/api/v1/event/reservations/", name="reservations")
