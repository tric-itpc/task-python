import motor.motor_asyncio
from fastapi import FastAPI

from config import DB_URL


app = FastAPI()
db = motor.motor_asyncio.AsyncIOMotorClient(DB_URL).service
