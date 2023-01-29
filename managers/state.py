from db import database
from models import state


class StateManager:
    @staticmethod
    async def get_states(limit: int, offset: int):
        query = (
            state.select()
            .order_by(state.c.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return await database.fetch_all(query)

    @staticmethod
    async def create_state(state_data):
        id_ = await database.execute(state.insert().values(state_data))
        return await database.fetch_one(state.select().where(state.c.id == id_))

    @staticmethod
    async def update_state(state_id, state_data):
        await database.execute(
            state.update().where(state.c.id == state_id).values(state_data)
        )

    @staticmethod
    async def delete_state(state_id):
        await database.execute(state.delete().where(state.c.id == state_id))
