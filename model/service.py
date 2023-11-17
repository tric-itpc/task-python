import datetime
from pydantic import BaseModel, Field


class Service(BaseModel):
    id: str = ''
    name: str = Field(include=True)
    state: str = Field(include=True)
    description: str = Field(include=True)
    state_dt: datetime.datetime = Field(default=datetime.datetime.now())
