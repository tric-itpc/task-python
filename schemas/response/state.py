from datetime import datetime

from pydantic import BaseModel

from models.enums import Status
from schemas.base import BaseState


class StateOut(BaseState):
    id: int
    created_at: datetime


class HistoryStateOut(BaseModel):
    status: Status
    state_description: str
    created_at: datetime
    id: int
