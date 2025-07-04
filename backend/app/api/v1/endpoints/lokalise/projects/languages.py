from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.languages import (
    LanguageDeleteResponse,
    LanguageUpdateRequest,
    ProjectLanguageResponse,
    ProjectLanguagesResponse,
)

router = APIRouter(tags=["lokalise-languages"])


@router.get("/languages", response_model=ProjectLanguagesResponse)
async def list_project_languages(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """Retrieve a list of project languages.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/languages

    Retrieves a list of languages configured for the project with their
    properties including language codes, names, RTL status, plural forms, and
    country codes.

    Requires read_languages OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/languages/{lang_id}", response_model=ProjectLanguageResponse)
async def get_project_language(
    project_id: str = Path(..., description="A unique project identifier"),
    lang_id: int = Path(..., description="A unique language identifier in the system"),
):
    """Retrieve a specific language from the project.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/languages/{lang_id}

    Retrieves a Language object with all its properties including language codes,
    names, RTL status, plural forms, and country codes for the specified project.

    Requires read_languages OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put(
    "/languages/{lang_id}", response_model=ProjectLanguageResponse, status_code=200
)
async def update_project_language(
    project_id: str = Path(..., description="A unique project identifier"),
    lang_id: int = Path(..., description="A unique language identifier in the system"),
    request: LanguageUpdateRequest = ...,
):
    """Update the properties of a language.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/languages/{lang_id}

    Updates the properties of a language including language code, name, and
    plural forms. Requires Manage languages admin right.

    Requires write_languages OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete(
    "/languages/{lang_id}", response_model=LanguageDeleteResponse, status_code=200
)
async def delete_project_language(
    project_id: str = Path(..., description="A unique project identifier"),
    lang_id: int = Path(..., description="A unique language identifier in the system"),
):
    """Delete a language from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/languages/{lang_id}

    Deletes a language from the project. Requires Manage languages admin right.

    Requires write_languages OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
