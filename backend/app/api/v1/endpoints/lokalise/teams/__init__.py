from fastapi import APIRouter

from .orders import router as orders_router

router = APIRouter(prefix="/teams")

router.include_router(orders_router, prefix="/{team_id}")
