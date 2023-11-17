import motor.motor_asyncio
from config import DB_URL
from fastapi import FastAPI

app = FastAPI()
db = motor.motor_asyncio.AsyncIOMotorClient(DB_URL).service

