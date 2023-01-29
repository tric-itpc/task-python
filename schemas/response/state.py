from datetime import datetime

from schemas.base import BaseState


class StateOut(BaseState):
    id: int
    created_at: datetime
