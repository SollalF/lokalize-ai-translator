from fastapi import APIRouter

from . import comments, contributors, projects

router = APIRouter()

router.include_router(projects.router, prefix="/projects", tags=["lokalise-projects"])
router.include_router(comments.router, tags=["lokalise-comments"])
router.include_router(contributors.router, tags=["lokalise-contributors"])
