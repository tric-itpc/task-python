import asyncio
from random import randint, choice
from typing import Literal
from requests import Session

from src.api_v1.models import db_helper, Service

session = Session()


class ServicesInWork:
    def __init__(self):
        self.services_states: dict[str:Literal["stable", "unstable", "disable"]] = dict()

    def add_service(self, service: Service, state: str):
        self.services_states[service.service_name] = state

    async def start_tracking_services_states(self):
        while True:
            interval = randint(1, 2)
            status = counting_probability_of_status_change()
            service_name = choice(list(self.services_states.keys()))

            if self.services_states[service_name] != status:
                self.services_states[service_name] = status
            await asyncio.sleep(interval)
            print(self.services_states)


def counting_probability_of_status_change() -> str:
    number = randint(0, 100)

    if number > 90:
        return "disable"
    if number > 60:
        return "unstable"

    return "stable"




