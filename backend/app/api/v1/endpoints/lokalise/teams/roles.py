from fastapi import APIRouter, HTTPException, Path, Response

from app.schemas.lokalise.permission_templates import TeamRolesResponse

router = APIRouter(tags=["lokalise-roles"])


@router.get("/roles", response_model=TeamRolesResponse)
async def list_team_roles(
    response: Response,
    team_id: int = Path(..., description="A unique team identifier"),
):
    """List all permission templates for particular team.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/roles

    List all permission templates for particular team to assign to contributor/group.
    Returns detailed information about each role including permissions, descriptions,
    and display properties.

    Requires appropriate OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    raise HTTPException(status_code=501, detail="Not implemented")
