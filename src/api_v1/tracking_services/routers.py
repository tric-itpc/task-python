import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status, HTTPException


from src.api_v1.tracking_services.update_service_module import states_manager
from src.api_v1.tracking_services.schemas import *
from src.models import db_helper
from src.api_v1.tracking_services.crud import (
    add_service_in_db,
    add_service_state_in_db,
    get_service_by_name,
    get_last_service_state,
    get_state_history_from_db
)


router = APIRouter(tags=["State manager API"])


@router.post(
    path="/create_service",
    response_model=ResponseService,
    description="If creation is successful, the service ID is returned",
    status_code=status.HTTP_201_CREATED
)
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
        service_state=service_schema.service_state
    )
    await session.close()

    return service_model


@router.get(
    path="/all_services_state",
    response_model=AllServiceStates,
    description="""
    Get the current state of services 
    (assume that the last record is the current state)
    """
)
async def get_all_services_state(
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    services_states = await get_last_service_state(session=session)

    if not services_states:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no server with that name"
        )

    return services_states


@router.get(
    path="/state_history/{service_name}",
    status_code=status.HTTP_200_OK,
    description="To get states history service",
    response_model=ResponseHistory
)
async def get_state_history(
        service_name: str,
        limit: int = 10,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    state_history = await get_state_history_from_db(
        session=session,
        service_name=service_name,
        limit=limit
    )

    if not state_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no server with that name"
        )

    return state_history


@router.post(
    path="/add_service_to_track",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessAddServiceToTrack,
    description="Adds a service to the state update buffer"
)
async def add_service_to_track(
        service_name: str,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    """
    Добавление сервиса (СУЩЕСТВУЮЩЕГО!) в буфер сервиса для обновления состояний.
    """
    service_model = await get_service_by_name(session=session, service_name=service_name)
    if not service_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found, try again!"
        )

    current_state = await get_last_service_state(session=session, service_model=service_model)
    states_manager.add_service(service=service_model, state=current_state.current_state)

    return SuccessAddServiceToTrack()


@router.post(
    path="/start_tracking",
    response_model=SuccessStartUpdateSchema,
    status_code=status.HTTP_202_ACCEPTED,
    description="Endpoint for starting update services conditions"
)
async def start_tracking_services(
        session: AsyncSession = Depends(db_helper.get_scoped_session)
) -> SuccessStartUpdateSchema:
    """
    Энвпоинт для запуска обновлений состояний сервисов(которые добавлены для
    отслеживания)
    """
    if not states_manager.services_states:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tracking list is empty"
        )
    asyncio.create_task(
        states_manager.start_tracking_services_states(session=session)
    )

    return SuccessStartUpdateSchema()
