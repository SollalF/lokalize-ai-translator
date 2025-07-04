from fastapi import APIRouter, HTTPException, Path

from app.schemas.lokalise.tokens import (
    ServiceTokenCreateRequest,
    ServiceTokenResponse,
)

router = APIRouter(tags=["lokalise-tokens"])


@router.post("/tokens", response_model=ServiceTokenResponse, status_code=200)
async def create_service_token(
    project_id: str = Path(..., description="A unique project identifier"),
    request: ServiceTokenCreateRequest = ...,
):
    """Create a JWT token for working with other services.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/tokens

    Creates a JWT token for the specified service to enable integration with
    other Lokalise services.

    Requires appropriate OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
