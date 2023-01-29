from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import is_admin, is_admin_or_staff, oauth2_scheme
from managers.service import ServiceManager
from schemas.request.service import ServiceIn
from schemas.response.service import ServiceAndStateOut, ServiceOut

router = APIRouter(tags=["Services"])


@router.get(
    "/services/",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=List[ServiceOut],
)
async def get_services(request: Request):
    return await ServiceManager.get_services()


@router.post(
    "/services/",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=ServiceOut,
)
async def create_service(request: Request, service_data: ServiceIn):
    return await ServiceManager.create_service(service_data.dict())


@router.put(
    "/services/{service_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def update_service(service_id: int, service_data: ServiceIn):
    await ServiceManager.update_service(service_id, service_data.dict())


@router.delete(
    "/services/{service_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def delete_service(service_id: int):
    await ServiceManager.delete_service(service_id)


@router.get(
    "/services/states",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=List[ServiceAndStateOut],
)
async def get_services_with_states(request: Request):
    return await ServiceManager.get_services_with_states()
