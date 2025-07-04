from fastapi import APIRouter, HTTPException, Query, Response

from app.schemas.lokalise.languages import LanguagesResponse

router = APIRouter(prefix="/system", tags=["lokalise-system"])


@router.get("/languages", response_model=LanguagesResponse)
async def list_system_languages(
    response: Response,
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """Retrieve a list of system languages.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/system/languages

    Retrieves a list of all system languages supported by Lokalise with their
    properties including language codes, names, RTL status, plural forms, and
    country codes.

    Requires read_languages OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    raise HTTPException(status_code=501, detail="Not implemented")
