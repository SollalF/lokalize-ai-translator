from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import Response

from app.schemas.lokalise.projects import (
    ProjectCreateRequest,
    ProjectDeleteResponse,
    ProjectEmptyResponse,
    ProjectResponse,
    ProjectsResponse,
    ProjectUpdateRequest,
)
from app.services.lokalise.projects import lokalise_projects_service

from .comments import router as comments_router
from .contributors import router as contributors_router
from .files import router as files_router
from .glossary import router as glossary_router
from .keys import router as keys_router
from .languages import router as languages_router
from .processes import router as processes_router
from .screenshots import router as screenshots_router
from .segments import router as segments_router
from .snapshots import router as snapshots_router
from .tasks import router as tasks_router
from .tokens import router as tokens_router
from .translations import router as translations_router
from .webhooks import router as webhooks_router

router = APIRouter(prefix="/projects", tags=["lokalise-projects"])

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
router.include_router(tasks_router, prefix="/{project_id}")
router.include_router(tokens_router, prefix="/{project_id}")
router.include_router(translations_router, prefix="/{project_id}")
router.include_router(webhooks_router, prefix="/{project_id}")


@router.get("/", response_model=ProjectsResponse)
async def list_projects(
    filter_team_id: Annotated[
        int | None, Query(description="Limit results to team ID")
    ] = None,
    filter_names: Annotated[
        str | None,
        Query(description="One or more project names to filter by (comma separated)"),
    ] = None,
    include_statistics: Annotated[
        int | None,
        Query(
            description="Whether to include project statistics. Possible values are 1 and 0",
            ge=0,
            le=1,
        ),
    ] = 1,
    include_settings: Annotated[
        int | None,
        Query(
            description="Whether to include project settings. Possible values are 1 and 0",
            ge=0,
            le=1,
        ),
    ] = 1,
    limit: Annotated[
        int | None,
        Query(description="Number of items to include (max 5000)", ge=1, le=5000),
    ] = None,
    page: Annotated[
        int | None, Query(description="Return results starting from this page", ge=1)
    ] = None,
):
    """
    Retrieves a list of projects available to the user, authorized with a token.

    This endpoint mirrors the Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects

    Requires read_projects OAuth access scope.
    """

    return await lokalise_projects_service.list_projects(
        filter_team_id=filter_team_id,
        filter_names=filter_names,
        include_statistics=include_statistics,
        include_settings=include_settings,
        limit=limit,
        page=page,
    )


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(request: ProjectCreateRequest):
    """
    Creates a new project in the specified team. Requires Admin role in the team.

    This endpoint mirrors the Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects

    Requires write_projects OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Retrieve a Project object.

    Retrieves a Project object.

    Requires read_projects OAuth access scope.

    Args:
        project_id: A unique project identifier

    Returns:
        ProjectResponse: Complete project object with settings, statistics, and languages
    """

    return await lokalise_projects_service.get_project(project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    request: ProjectUpdateRequest,
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Update the details of a project.

    Updates the details of a project. Requires Manage settings admin right.

    Requires write_projects OAuth access scope.

    Args:
        request: Project update data (name required, description optional)
        project_id: A unique project identifier

    Returns:
        ProjectResponse: Updated project object with settings, statistics, and languages
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{project_id}", response_model=ProjectDeleteResponse)
async def delete_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Delete a project.

    Deletes a project.

    Requires write_projects OAuth access scope.

    Args:
        project_id: A unique project identifier

    Returns:
        ProjectDeleteResponse: Deletion status with project_id and project_deleted boolean
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{project_id}/empty", response_model=ProjectEmptyResponse)
async def empty_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Delete all keys and translations from the project.

    Deletes all keys and translations from the project. Requires Manage settings admin right.

    Requires write_projects OAuth access scope.

    Args:
        project_id: A unique project identifier

    Returns:
        ProjectEmptyResponse: Deletion status with project_id and keys_deleted boolean
    """
    raise HTTPException(status_code=501, detail="Not implemented")
