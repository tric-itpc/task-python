from sqlalchemy import and_, func, select

from db import database
from models import service, state


class ServiceManager:
    @staticmethod
    async def get_services():
        query = service.select()
        return await database.fetch_all(query)

    @staticmethod
    async def create_service(service_data):
        id_ = await database.execute(service.insert().values(service_data))
        return await database.fetch_one(
            service.select().where(service.c.id == id_)
        )

    @staticmethod
    async def update_service(service_id, service_data):
        await database.execute(
            service.update()
            .where(service.c.id == service_id)
            .values(service_data)
        )

    @staticmethod
    async def delete_service(service_id):
        await database.execute(
            service.delete().where(service.c.id == service_id)
        )

    @staticmethod
    async def get_services_with_states():
        # Subquery retrieving last state of every service
        subq = (
            select(
                [
                    state.c.service_id,
                    func.max(state.c.created_at).label("created_at"),
                ]
            )
            .group_by(state.c.service_id)
            .alias("last_state")
        )
        q = (
            select([service, state])
            .select_from(
                service.join(state, service.c.id == state.c.service_id).join(
                    subq,
                    and_(
                        subq.c.service_id == state.c.service_id,
                        subq.c.created_at == state.c.created_at,
                    ),
                )
            )
            .distinct(state.c.service_id)
        )
        return await database.fetch_all(q)

    @staticmethod
    async def get_service_states_history(service_name, limit: int, offset: int):
        # Subquery that finds service by its name
        wanted_service_subq = service.select().where(
            service.c.name == service_name
        )

        query = (
            state.select()
            .where(state.c.service_id == wanted_service_subq.c.id)
            .order_by(state.c.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return await database.fetch_all(query)

    @staticmethod
    async def get_service_sla(service_name, start_date, end_date):
        # Subquery that finds service by its name
        wanted_service_subq = service.select().where(
            service.c.name == service_name
        )

        # Query for the states between two dates
        between_dates_q = (
            state.select()
            .where(state.c.service_id == wanted_service_subq.c.id)
            .where(state.c.created_at >= start_date)
            .where(state.c.created_at <= end_date)
            .order_by(state.c.created_at.desc())
        )

        # Query for the state actual for the start date
        before_start_date_q = (
            state.select()
            .where(state.c.service_id == wanted_service_subq.c.id)
            .where(state.c.created_at < start_date)
            .order_by(state.c.created_at.desc())
            .limit(1)
        )

        union_query = between_dates_q.union(before_start_date_q)
        return await database.fetch_all(union_query)
