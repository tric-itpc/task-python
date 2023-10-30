import uuid
from typing import Literal
from enum import Enum

from datetime import datetime

from pydantic import BaseModel


class ServiceState(BaseModel):
    service_state: Literal["stable", "unstable", "disable"]


class CreateServiceSchema(ServiceState):
    service_name: str
    service_description: str


class ServiceStateSchema(ServiceState):
    service_id: uuid.UUID


class SuccessStartUpdateSchema(BaseModel):
    status: str = "service_update_started_success"


class SuccessAddServiceToTrack(BaseModel):
    status: str = "Service add to tracking!"


class ServiceData(BaseModel):
    service_name: str
    service_description: str


class ServiceStateHistory(ServiceState):
    created_at: datetime


class ResponseHistory(BaseModel):
    service_info: ServiceData
    service_state_history: list[ServiceStateHistory] = []