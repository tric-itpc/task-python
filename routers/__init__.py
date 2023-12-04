from fastapi import APIRouter

from routers import log_router

router = APIRouter()

router.include_router(log_router.router)
