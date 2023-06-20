from fastapi import APIRouter

from app.routes import log_router

router = APIRouter()

router.include_router(log_router.router)
