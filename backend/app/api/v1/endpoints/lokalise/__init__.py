from fastapi import APIRouter

from . import projects

router = APIRouter()

# Include project endpoints under /projects prefix
router.include_router(projects.router, prefix="/projects", tags=["lokalise-projects"])
