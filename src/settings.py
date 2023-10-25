from os import environ
from typing import Any

from dotenv import load_dotenv


class Settings:
    def __init__(self) -> None:
        load_dotenv()

    def __getattribute__(self, __name: str) -> Any:
        return environ.get(__name, None)


env = Settings()