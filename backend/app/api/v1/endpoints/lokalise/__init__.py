from fastapi import APIRouter

from .projects import router as projects_router
from .system import router as system_router
from .teams import router as teams_router

router = APIRouter()

router.include_router(projects_router)
router.include_router(system_router)
router.include_router(teams_router)
