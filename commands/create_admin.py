import asyncclick as click

from db import database
from managers.user import UserManager
from models.enums import RoleType


@click.command()
@click.option("-e", "--email", type=str, required=True)
@click.option("-p", "--password", type=str, required=True)
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
async def create_admin(email, password, first_name, last_name):
    user_data = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "role": RoleType.admin,
    }
    await database.connect()
    await UserManager.register(user_data)
    await database.disconnect()
    print(f"Administrator {user_data['first_name']} registered successfully.")


if __name__ == "__main__":
    create_admin(_anyio_backend="asyncio")
