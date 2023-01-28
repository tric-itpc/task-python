from pydantic import BaseModel

from models.enums import Status


class UserBase(BaseModel):
    email: str


class BaseService(BaseModel):
    name: str
    description: str


class BaseState(BaseModel):
    service_id: int
    status: Status
    state_description: str
