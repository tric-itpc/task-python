import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models import Service, ServiceState
from .schemas import (
    CreateServiceSchema,
    ResponseHistory,
    ServiceFullInformation,
    ServiceStateHistory,
    AllServiceStates,
    CurrentServiceState
)


async def get_state_history_from_db(
        session: AsyncSession,
        service_name: str,
        limit: int = 999
) -> ResponseHistory | None:
    """
        Функция, которая по имени сервиса получает
        всю историю его изменений. Если сервис не
        найден, то возвращает None object.
        :param session: Объект ассинхронной сессии
        :param service_name: Имя существующего сервиса
        :param limit: Количество записей(по убыванию даты)
        :return: ResponseHistory
        :exception None: если сервис не найден, возвращается None
    """
    stmt = select(Service).options(
           selectinload(Service.all_states)
    ).where(
        Service.service_name == service_name
    )

    service_history = await session.scalar(stmt)
    await session.close()

    if not service_history:
        return None

    service_data = ServiceFullInformation.model_validate(
        service_history, from_attributes=True
    )

    result = ResponseHistory(
        service_info=service_data
    )

    counter = 0
    for state in service_history.all_states:
        if counter > limit:
            break
        counter += 1
        print(state)
        result.service_state_history.append(
            ServiceStateHistory.model_validate(state, from_attributes=True)   # Sqlalchemy.model>>Pydantic.schema
        )

    return result


async def add_service_in_db(
        session: AsyncSession,
        service_schema: CreateServiceSchema
) -> Service:
    """
    Функция, добавляет сервис в базу данных.
    :param session: Объект ассинхронной сессии.
    :param service_schema: Pydantic схема.
    :return: Service(sqlalchemy model obj)
    """
    service_model = Service(
        service_name=service_schema.service_name,
        service_description=service_schema.service_description
    )
    session.add(service_model)
    await session.commit()

    return service_model


async def add_service_state_in_db(
        session: AsyncSession,
        service_id: uuid.UUID,
        service_state: str
) -> ServiceState:
    """
    Функция добавляет запись в таблицу историй
    состояний сервисов.
    :param session:  Объект ассинхронной сессии
    :param service_id: uuid сервиса.
    :param service_state: Состояние сервиса(stable, unstable, disable)
    :return: ServiceState sqlalchemy model
    """
    service_state_model = ServiceState(
        service_id=service_id,
        service_state=service_state)

    session.add(service_state_model)
    await session.commit()

    return service_state_model


async def get_service_by_name(
        session: AsyncSession,
        service_name: str,
) -> Service | None:
    """
    Функция получает имя объекта и возвращает
    sqlalchemy Service.
    :param session: Объект ассинхронной сессии
    :param service_name: Имя сервиса
    :return: Service sqlalchemy model или None, если сервис не найден.
    """
    stmt = select(Service).where(Service.service_name == service_name)
    result = await session.execute(stmt)
    service: Service | None = result.one_or_none()

    return service


async def get_last_service_state(
        session: AsyncSession,
        service_model: Service | None = None
) -> AllServiceStates:
    """
    Функция получает Service sqlalchemy model, и возвращает
    последнее состояние(ПОСЛЕДНЯЯ ЗАПИСЬ В БД И ЯВЛЯЕТСЯ АКТУАЛЬНЫМ СОСТОЯНИЕМ)
    если service_model = None, то возвращается актуальное состоянеи ВСЕХ сервисов.
    :param session: Объект ассинхронной сессии
    :param service_model: Service sqlalchemy model OR None obj.
    :return: AllServiceStates pydantic obj.
    """
    stmt = select(Service).options(
        selectinload(Service.state)
    ).order_by()

    if service_model:
        stmt = stmt.where(Service.service_name == service_model.service_name)

    services = await session.scalars(stmt)

    await session.close()

    result = AllServiceStates()
    for service in services:
        state = service.state
        if not state:
            state = "disable"
        else:
            state = service.state.service_state
        result.current_state.append(
            CurrentServiceState(
                service_name=service.service_name,
                service_state=state
            )
        )

    return result
