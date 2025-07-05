from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.team_users import (
    TeamUserDeleteResponse,
    TeamUserResponse,
    TeamUsersResponse,
    TeamUserUpdateRequest,
)

router = APIRouter(tags=["lokalise-team-users"])


@router.get("/users", response_model=TeamUsersResponse)
async def list_team_users(
    response: Response,
    team_id: int = Path(..., description="A unique team identifier"),
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """List all team users. Requires Admin role in the team.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/users

    Requires read_team_users OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/users/{user_id}", response_model=TeamUserResponse)
async def get_team_user(
    team_id: int = Path(..., description="A unique team identifier"),
    user_id: int = Path(..., description="A unique identifier of the user"),
):
    """Retrieves a Team user object. Requires Admin role in the team.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/users/{user_id}

    Requires read_team_users OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/users/{user_id}", response_model=TeamUserResponse)
async def update_team_user(
    team_id: int = Path(..., description="A unique team identifier"),
    user_id: int = Path(..., description="A unique identifier of the user"),
    request: TeamUserUpdateRequest = ...,
):
    """Updates the role of a team user. Requires Admin role in the team.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/teams/{team_id}/users/{user_id}

    Requires write_team_users OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/users/{user_id}", response_model=TeamUserDeleteResponse)
async def delete_team_user(
    team_id: int = Path(..., description="A unique team identifier"),
    user_id: int = Path(..., description="A unique identifier of the user"),
):
    """Deletes a user from the team. Requires Admin role in the team.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/teams/{team_id}/users/{user_id}

    Requires write_team_users OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
