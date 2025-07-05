from fastapi import APIRouter

from .comments import router as comments_router
from .contributors import router as contributors_router
from .core import router as core_router
from .files import router as files_router
from .glossary import router as glossary_router
from .keys import router as keys_router
from .languages import router as languages_router
from .processes import router as processes_router
from .screenshots import router as screenshots_router
from .segments import router as segments_router
from .snapshots import router as snapshots_router
from .tokens import router as tokens_router

router = APIRouter(prefix="/projects")

router.include_router(core_router)
router.include_router(comments_router, prefix="/{project_id}")
router.include_router(contributors_router, prefix="/{project_id}")
router.include_router(files_router, prefix="/{project_id}")
router.include_router(glossary_router, prefix="/{project_id}")
router.include_router(keys_router, prefix="/{project_id}")
router.include_router(languages_router, prefix="/{project_id}")
router.include_router(processes_router, prefix="/{project_id}")
router.include_router(screenshots_router, prefix="/{project_id}")
router.include_router(segments_router, prefix="/{project_id}")
router.include_router(snapshots_router, prefix="/{project_id}")
router.include_router(tokens_router, prefix="/{project_id}")
