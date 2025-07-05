from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.translation_providers import (
    TranslationProviderResponse,
    TranslationProvidersResponse,
)

router = APIRouter(tags=["lokalise-translation-providers"])


@router.get("/translation_providers", response_model=TranslationProvidersResponse)
async def list_translation_providers(
    response: Response,
    team_id: int = Path(..., description="A unique team identifier"),
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """Lists all translation providers.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/translation_providers

    Requires read_team_orders OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get(
    "/translation_providers/{provider_id}", response_model=TranslationProviderResponse
)
async def get_translation_provider(
    team_id: int = Path(..., description="A unique team identifier"),
    provider_id: int = Path(..., description="A unique identifier of the provider"),
):
    """Retrieves a Translation provider object with tiers and available language pairs.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/translation_providers/{provider_id}

    Requires read_team_orders OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
