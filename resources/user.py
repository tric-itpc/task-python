from typing import List, Optional

from fastapi import APIRouter, Depends

from managers.auth import is_admin, is_admin_or_staff, oauth2_scheme
from managers.user import UserManager
from models.enums import RoleType
from schemas.response.user import UserOut

router = APIRouter(tags=["Users"])


@router.get(
    "/users",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=List[UserOut],
)
async def get_users(email: Optional[str] = None):
    """
    Outputs a list of all users, and when you add an email
    as a query parameter — it finds the right user.
    For usage your role should be "staff" or "admin".
    """
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.delete(
    "/users/{user_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def delete_user(user_id: int):
    """
    Removes the user from the database.
    For usage your role should be "admin".
    """
    await UserManager.delete_user(user_id)


@router.put(
    "/users/{user_id}/make-admin",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_admin(user_id: int):
    """
    Changes user's role to "admin".
    For usage your role should be "admin".
    """
    await UserManager.change_role(RoleType.admin, user_id)


@router.put(
    "/users/{user_id}/make-staff",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_staff(user_id: int):
    """
    Changes user's role to "staff".
    For usage your role should be "admin".
    """
    await UserManager.change_role(RoleType.staff, user_id)
