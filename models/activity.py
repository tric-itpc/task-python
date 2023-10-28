from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ServiceStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    UNSTABLE = 'UNSTABLE'
    STOPPED = 'STOPPED'



class CurrentActivity(BaseModel):
    service_name: str = Field(example='Service_name')
    status: ServiceStatus = Field(examle=ServiceStatus.ACTIVE)
    description: str = Field(example='stable operation of the server')


class ServicesList(CurrentActivity):
    status_map: dict


class ServicesLog(CurrentActivity):
    log_uuid: UUID = Field(default_factory=uuid4)
    created_date: datetime
