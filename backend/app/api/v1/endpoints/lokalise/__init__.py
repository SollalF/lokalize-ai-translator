from fastapi import APIRouter

from . import comments, projects

router = APIRouter()

# Include sub-routers
router.include_router(projects.router, prefix="/projects", tags=["lokalise-projects"])
router.include_router(comments.router, tags=["lokalise-comments"])
