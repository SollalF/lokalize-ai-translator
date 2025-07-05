from fastapi import APIRouter

from .groups import router as groups_router
from .orders import router as orders_router
from .roles import router as roles_router

router = APIRouter(prefix="/teams")

router.include_router(groups_router, prefix="/{team_id}")
router.include_router(orders_router, prefix="/{team_id}")
router.include_router(roles_router, prefix="/{team_id}")
