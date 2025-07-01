import random
from locust import HttpUser, task, between


class EventUser(HttpUser):
    wait_time = between(1, 2)

    # EVENT_IDS = ["9cfac9c3-2568-4593-8bd1-c8d6daa09ad7"]
    EVENT_IDS = ["9cfac9c3-2568-4593-8bd1-c8d6daa09ad7"]

    # def on_start(self) -> None:
    # response = self.client.post(
    #     "/api/v1/auth/login/", json={"email": "admin@gmail.com", "password": 1234}
    # )

    # token = response.json().get("access")
    # if token:
    #     # self.client.headers.update({"Authorization": f"Bearer {token}"})
    #     self.token = f"Bearer {token}"

    # response = self.client.get("/api/v1/event/events/")
    # data = response.json()

    # events = data.get("results", [])
    # self.event_ids = [event["id"] for event in events]

    @task(3)
    def browse_events(self):
        self.client.get("/api/v1/event/events/", name="/events")

    @task(1)
    def browse_event_detail(self):
        id = random.choice(self.EVENT_IDS)

        self.client.get(f"/api/v1/event/events/{id}", name="/event_detail")

    @task
    def browse_ticket_types(self):
        event_id = random.choice(self.EVENT_IDS)
        self.client.get(
            f"/api/v1/event/events/{event_id}/ticket_types/", name="/ticket_type"
        )

    @task
    def browse_reservations(self):
        event_id = random.choice(self.EVENT_IDS)
        self.client.get(
            f"/api/v1/event/events/{event_id}/reservations/", name="/reservations"
        )
