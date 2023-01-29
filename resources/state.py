from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import is_admin, oauth2_scheme
from managers.state import StateManager
from schemas.request.state import StateIn
from schemas.response.state import StateOut

router = APIRouter(tags=["States"])


@router.get(
    "/states/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[StateOut],
)
async def get_states(request: Request, limit: int = 10, offset: int = 0):
    return await StateManager.get_states(limit, offset)


@router.post(
    "/states/",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=StateOut,
)
async def create_state(request: Request, state: StateIn):
    return await StateManager.create_state(state.dict())


@router.put(
    "/states/{state_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def update_state(state_id: int, state_data: StateIn):
    await StateManager.update_state(state_id, state_data.dict())


@router.delete(
    "/states/{state_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def delete_state(state_id: int):
    await StateManager.delete_state(state_id)
