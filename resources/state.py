from typing import List

from fastapi import APIRouter, Depends

from managers.auth import is_admin, is_admin_or_staff, oauth2_scheme
from managers.state import StateManager
from schemas.request.state import StateIn
from schemas.response.state import StateOut

router = APIRouter(tags=["States"])


@router.get(
    "/states",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=List[StateOut],
)
async def get_states(limit: int = 10, offset: int = 0):
    """
    Outputs a list of all states in the database,
    pagination is available by the query parameters
    "limit" and "offset".
    For usage your role should be "staff" or "admin".
    """
    return await StateManager.get_states(limit, offset)


@router.post(
    "/states",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=StateOut,
)
async def create_state(state: StateIn):
    """
    Adds the state of service to the database,
    the time stamp is added automatically.
    For usage your role should be "admin".
    """
    return await StateManager.create_state(state.dict())


@router.put(
    "/states/{state_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def update_state(state_id: int, state_data: StateIn):
    """
    Changes the state of service data,
    the time stamp can't be changed.
    For usage your role should be "admin".
    """
    await StateManager.update_state(state_id, state_data.dict())


@router.delete(
    "/states/{state_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def delete_state(state_id: int):
    """
    Removes the state of service from the database.
    For usage your role should be "admin".
    """
    await StateManager.delete_state(state_id)
