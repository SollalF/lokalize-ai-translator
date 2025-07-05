from fastapi import APIRouter, HTTPException, Path

from app.schemas.lokalise.team_user_billing_details import (
    TeamUserBillingDetailsCreateRequest,
    TeamUserBillingDetailsResponse,
)

router = APIRouter(tags=["lokalise-billing-details"])


@router.get("/billing_details", response_model=TeamUserBillingDetailsResponse)
async def get_team_user_billing_details(
    team_id: int = Path(..., description="A unique team identifier"),
):
    """Retrieve a Team user billing details object.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/billing_details

    Requires read_team_user_billing_details OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(
    "/billing_details", response_model=TeamUserBillingDetailsResponse, status_code=200
)
async def create_team_user_billing_details(
    team_id: int = Path(..., description="A unique team identifier"),
    request: TeamUserBillingDetailsCreateRequest = ...,
):
    """Create a Team user billing details object.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/teams/{team_id}/billing_details

    Requires write_team_user_billing_details OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put(
    "/billing_details", response_model=TeamUserBillingDetailsResponse, status_code=200
)
async def update_team_user_billing_details(
    team_id: int = Path(..., description="A unique team identifier"),
    request: TeamUserBillingDetailsCreateRequest = ...,
):
    """Update a Team user billing details object.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/teams/{team_id}/billing_details

    Requires write_team_user_billing_details OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
