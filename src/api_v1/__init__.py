from fastapi import APIRouter

from .tracking_services.routers import router as service_statistic_router

router = APIRouter()

router.include_router(
    router=service_statistic_router,
    prefix="/tracking_service"
)

