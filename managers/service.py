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
