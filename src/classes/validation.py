from datetime import datetime, timedelta
from typing import Tuple

from pydantic import BaseModel

from settings import env


class service_model(BaseModel):
    id: str = None
    service: str
    status: str
    description: str = ""
    date_time: datetime

    @staticmethod
    def create_as_dict(service: str, status: str, description: str = "") -> dict:
        representation = service_model(
            service=service,
            status=status,
            description=description,
            date_time=datetime.now(),
        ).model_dump()
        representation.pop(env.PARAM_ID)
        return representation


class sla_object(BaseModel):
    uptime: float
    availability: float


class difference_model(BaseModel):
    service: str
    status: str
    date_time: datetime = datetime.now()
    difference: timedelta = None


class service_statistic(BaseModel):
    enable_time: float
    disabled_time: float
    unstable_time: float
    SLA: sla_object


class service_status(BaseModel):
    service: str
    interval: Tuple[datetime, datetime]
    statistic: service_statistic


class service_create(BaseModel):
    service: str
    status: str
    description: str = ""