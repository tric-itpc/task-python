import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from src.models import db_helper
from src.api_v1.tracking_services.schemas import CreateServiceSchema, ServiceStateSchema
from src.api_v1.tracking_services.crud import (
    add_service_in_db,
    add_service_state_in_db,
    get_service_by_name,
    get_last_service_state,
    get_state_history_from_db
)
from src.api_v1.tracking_services.service import states_manager


router = APIRouter(tags=["state_manager"])


@router.post(path="/create_service")
async def create_service(
        service_schema: CreateServiceSchema,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    service_model = await add_service_in_db(
        session=session,
        service_schema=service_schema
    )

    await add_service_state_in_db(
        session=session,
        service_id=service_model.id,
        service_state=service_schema.state
    )
    await session.close()

    return service_model


@router.get(path="/all_services_state")
async def get_all_services_state(
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    services_states = await get_last_service_state(session=session)

    return services_states


@router.get(path="/state_history/{service_name}")
async def get_state_history(
        service_name: str,
        limit: int = 10,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    return await get_state_history_from_db(
        session=session,
        service_name=service_name,
        limit=limit
    )


@router.post(path="/add_service_to_track")
async def add_service_to_track(
        service_name: str,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    service_model = await get_service_by_name(session=session, service_name=service_name)
    current_state = await get_last_service_state(session=session, service_model=service_model)

    states_manager.add_service(service=service_model, state=current_state[service_name])

    print(states_manager.services_states)


@router.post(path="/start_tracking")
async def start_tracking_services(
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    asyncio.create_task(states_manager.start_tracking_services_states(session=session))
    return "ok"
