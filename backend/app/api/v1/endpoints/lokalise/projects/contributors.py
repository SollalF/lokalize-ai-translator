from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.contributors import (
    ContributorDeleteResponse,
    ContributorsCreateRequest,
    ContributorUpdateRequest,
    ProjectContributorResponse,
    ProjectContributorsResponse,
)

router = APIRouter(tags=["lokalise-contributors"])


@router.get(
    "/contributors",
    response_model=ProjectContributorsResponse,
)
async def list_project_contributors(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    limit: int | None = Query(
        100, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """List contributors of a project including their language access levels.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/contributors

    Requires read_contributors OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(
    "/contributors",
    response_model=ProjectContributorResponse,
    status_code=201,
)
async def create_contributors(
    project_id: str = Path(..., description="A unique project identifier"),
    request: ContributorsCreateRequest = ...,
):
    """Create one or more contributors in the project.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/contributors

    Requires write_contributors OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get(
    "/contributors/{contributor_id}",
    response_model=ProjectContributorResponse,
)
async def get_contributor(
    project_id: str = Path(..., description="A unique project identifier"),
    contributor_id: int = Path(
        ..., description="A unique identifier of the contributor"
    ),
):
    """Retrieve a single contributor object.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/contributors/{contributor_id}

    Requires read_contributors OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put(
    "/contributors/{contributor_id}",
    response_model=ProjectContributorResponse,
)
async def update_contributor(
    project_id: str = Path(..., description="A unique project identifier"),
    contributor_id: int = Path(
        ..., description="A unique identifier of the contributor"
    ),
    request: ContributorUpdateRequest = ...,
):
    """Update properties of a contributor.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/contributors/{contributor_id}

    Requires write_contributors OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete(
    "/contributors/{contributor_id}",
    response_model=ContributorDeleteResponse,
)
async def delete_contributor(
    project_id: str = Path(..., description="A unique project identifier"),
    contributor_id: int = Path(
        ..., description="A unique identifier of the contributor"
    ),
):
    """Delete a contributor from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/contributors/{contributor_id}

    Requires write_contributors OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get(
    "/contributors/me",
    response_model=ProjectContributorResponse,
)
async def get_my_contributor(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """Retrieve contributor object for the requesting user.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/contributors/me

    Requires read_contributors OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
