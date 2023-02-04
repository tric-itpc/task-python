from collections import deque
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from managers.auth import is_admin, is_admin_or_staff, oauth2_scheme
from managers.service import ServiceManager
from schemas.request.service import ServiceIn
from schemas.response.service import (
    ServiceAndStateOut,
    ServiceOut,
    ServiceSlaOut,
)
from schemas.response.state import HistoryStateOut

router = APIRouter(tags=["Services"])


@router.get(
    "/services",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=List[ServiceOut],
)
async def get_services():
    """
    Outputs a list of all services in the database.
    For usage your role should be "staff" or "admin".
    """
    return await ServiceManager.get_services()


@router.post(
    "/services",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=ServiceOut,
)
async def create_service(service_data: ServiceIn):
    """
    Adds the service to the database.
    For usage your role should be "admin".
    """
    return await ServiceManager.create_service(service_data.dict())


@router.put(
    "/services/{service_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def update_service(service_id: int, service_data: ServiceIn):
    """
    Changes the service data.
    For usage your role should be "admin".
    """
    await ServiceManager.update_service(service_id, service_data.dict())


@router.delete(
    "/services/{service_id}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def delete_service(service_id: int):
    """
    Removes the service from the database.
    For usage your role should be "admin".
    """
    await ServiceManager.delete_service(service_id)


@router.get(
    "/services/states",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=List[ServiceAndStateOut],
)
async def get_services_with_states():
    """
    Outputs a list of services with actual states.
    For usage your role should be "staff" or "admin".
    """
    return await ServiceManager.get_services_with_states()


@router.get(
    "/services/states/{service_name}",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=List[HistoryStateOut],
)
async def get_service_states_history(
    service_name: str, limit: int = 15, offset: int = 0
):
    """
    Outputs the history of service states by the service name,
    pagination is available by the query parameters
    "limit" and "offset". Returns a message if service
    does not exists or contains no states.
    For usage your role should be "staff" or "admin".
    """
    history = await ServiceManager.get_service_states_history(
        service_name, limit, offset
    )
    if not history:
        return JSONResponse(
            {"message": "This service does not exist or contains no states."}
        )
    return history


@router.get(
    "/services/states/{service_name}/sla",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin_or_staff)],
    response_model=ServiceSlaOut,
)
async def get_service_sla(
    service_name: str, start_date: str = "31.01.23_00.00", end_date: str = "now"
):
    """
    Outputs service downtime and SLA (Service Level Agreement)
    by the service name and according to the specified interval
    as query parameters. Time format should be "dd.mm.yy_HH.MM"
    ("31.12.22_12.25") also you can use "now" as end date.
    Default values is "31.01.23_00.00" — "now". Returns a message
    if service does not exists or contains no states.
    For usage your role should be "staff" or "admin".
    """

    start_date_dtime = datetime.strptime(start_date, "%d.%m.%y_%H.%M")
    if end_date == "now":
        end_date_dtime = datetime.now()
    else:
        end_date_dtime = datetime.strptime(end_date, "%d.%m.%y_%H.%M")

    states = await ServiceManager.get_service_sla(
        service_name, start_date_dtime, end_date_dtime
    )

    if not states:
        return JSONResponse(
            {"message": "This service does not exist or contains no states."}
        )

    # Determine starting point for counting uptime/downtime
    if start_date_dtime >= states[0].created_at:
        counting_point = start_date_dtime
    else:
        counting_point = states[0].created_at

    # Using collections.deque instead of list due to optimized left append
    states_durations = deque()
    if len(states) == 1:
        states_durations.append(end_date_dtime - counting_point)
    else:
        # Walk through states entries except for the first and last
        # When its only two entries – this loop do nothing
        for i in range(1, len(states) - 1):
            states_durations.append(
                states[i + 1].created_at - states[i].created_at
            )

        # Append first state duration
        states_durations.appendleft(states[1].created_at - counting_point)
        # Append last state duration
        states_durations.append(end_date_dtime - states[-1].created_at)

    uptime = timedelta()
    downtime = timedelta()
    for i in range(len(states)):
        if states[i].status == "running":
            uptime += states_durations[i]
        else:
            downtime += states_durations[i]

    sla = uptime / (uptime + downtime) * 100

    return JSONResponse(
        {"downtime": str(downtime), "SLA_percentage": float(f"{sla:.3f}")}
    )
