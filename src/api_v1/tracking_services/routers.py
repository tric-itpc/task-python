from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from src.api_v1.models import db_helper
from src.api_v1.service_statistic_manager.schemas import CreateService


router = APIRouter(tags=["state_manager"])


@router.post(path="/create_service")
async def create_service(
        service: CreateService,
        session: AsyncSession = Depends(db_helper.get_scoped_session_dependency)
):
    pass




@router.get(path="/all_services_state")
async def get_all_services_state():
    pass


