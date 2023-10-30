from fastapi import HTTPException, status

import asyncio
from random import randint, choice
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.tracking_services.schemas import ServiceStateSchema
from src.models import Service
from src.api_v1.tracking_services.crud import add_service_state_in_db, get_service_by_name

class ServicesInWork:
    def __init__(self):
        self.services_states: dict[str:Literal["stable", "unstable", "disable"]] = dict()

    def add_service(self, service: Service, state: str):
        self.services_states[service.service_name] = state

    async def start_tracking_services_states(self, session: AsyncSession):
        while True:
            interval = randint(1, 2)
            current_state = counting_probability_of_status_change()
            service_name = choice(list(self.services_states.keys()))

            if self.services_states[service_name] != current_state:
                self.services_states[service_name] = current_state
                service = await get_service_by_name(session=session, service_name=service_name)
                await add_service_state_in_db(
                    session=session,
                    service_state=current_state,
                    service_id=service.id
                    )

            await asyncio.sleep(interval)


def counting_probability_of_status_change() -> str:
    number = randint(0, 100)

    if number > 90:
        return "disable"
    if number > 60:
        return "unstable"

    return "stable"


states_manager = ServicesInWork()

