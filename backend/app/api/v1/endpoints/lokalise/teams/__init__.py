from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.teams import TeamResponse, TeamsResponse

from .billing_details import router as billing_details_router
from .groups import router as groups_router
from .orders import router as orders_router
from .roles import router as roles_router
from .users import router as users_router

router = APIRouter(prefix="/teams")

router.include_router(groups_router, prefix="/{team_id}")
router.include_router(orders_router, prefix="/{team_id}")
router.include_router(roles_router, prefix="/{team_id}")
router.include_router(billing_details_router, prefix="/{team_id}")
router.include_router(users_router, prefix="/{team_id}")


@router.get("", response_model=TeamsResponse)
async def list_teams(
    response: Response,
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """Lists all teams available to the user.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams

    Requires read_team_users OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int = Path(..., description="A unique team identifier"),
):
    """Get details of a specific team.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}

    Requires read_team_users OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
