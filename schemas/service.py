from datetime import datetime

from pydantic import BaseModel

class Service(BaseModel):
    name: str
    state: str
    description: str

class ServiceHistory(BaseModel):
    service_name: str
    from_state: str
    to_state: str
    change_time: datetime
    time_not_working: str


class SLA_output(BaseModel):
    service_name: str
    from_date: datetime
    to_date: datetime
    SLA: float
    all_downtimes: int
    downtimes_by_period: int
