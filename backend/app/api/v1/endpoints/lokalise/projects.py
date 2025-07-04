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

router = APIRouter()


@router.get("", response_model=ProjectsResponse)
async def list_projects(
    response: Response,
    filter_team_id: int | None = Query(None, description="Limit results to team ID"),
    filter_names: str | None = Query(
        None, description="One or more project names to filter by (comma separated)"
    ),
    include_statistics: int | None = Query(
        1,
        description="Whether to include project statistics. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    include_settings: int | None = Query(
        1,
        description="Whether to include project settings. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    limit: int | None = Query(
        100, description="Number of items to include (max 5000)", ge=1, le=5000
    ),
    page: int | None = Query(
        1, description="Return results starting from this page", ge=1
    ),
):
    """
    Retrieves a list of projects available to the user, authorized with a token.

    This endpoint mirrors the Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects

    Requires read_projects OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("", response_model=ProjectResponse, status_code=201)
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
    Retrieves a Project object.

    This endpoint mirrors the Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}

    Requires read_projects OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    request: ProjectUpdateRequest,
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Updates the details of a project. Requires Manage settings admin right.

    This endpoint mirrors the Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}

    Requires write_projects OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{project_id}", response_model=ProjectDeleteResponse)
async def delete_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Deletes a project.

    This endpoint mirrors the Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}

    Requires write_projects OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{project_id}/empty", response_model=ProjectEmptyResponse)
async def empty_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Deletes all keys and translations from the project. Requires Manage settings admin right.

    This endpoint mirrors the Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/empty

    Requires write_projects OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
