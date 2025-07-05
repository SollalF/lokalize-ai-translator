from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.translations import (
    TranslationResponse,
    TranslationsResponse,
    TranslationUpdateRequest,
)

router = APIRouter(tags=["lokalise-project-translations"])


@router.get("/translations", response_model=TranslationsResponse)
async def list_project_translations(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    disable_references: int | None = Query(
        None,
        ge=0,
        le=1,
        description="Whether to disable key references. Possible values are 1 and 0.",
    ),
    filter_lang_id: int | None = Query(
        None, description="Return translations only for presented language ID."
    ),
    filter_is_reviewed: int | None = Query(
        None,
        ge=0,
        le=1,
        description="Filter translations which are reviewed. Possible values are 1 and 0.",
    ),
    filter_unverified: int | None = Query(
        None,
        ge=0,
        le=1,
        description="Filter translations which are unverified. Possible values are 1 and 0.",
    ),
    filter_untranslated: int | None = Query(
        None,
        ge=0,
        le=1,
        description="Filter by untranslated keys. Possible values are 1 and 0.",
    ),
    filter_qa_issues: str | None = Query(
        None,
        description="One or more QA issues to filter by (comma separated). Possible values are spelling_and_grammar, placeholders, html, url_count, url, email_count, email, brackets, numbers, leading_whitespace, trailing_whitespace, double_space, special_placeholder and unbalanced_brackets.",
    ),
    filter_active_task_id: int | None = Query(
        None, description="Filter translations which are part of given task ID."
    ),
    pagination: str | None = Query(
        "offset",
        description="Type of pagination. Possible values are offset and cursor. The default value is offset.",
    ),
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        None, ge=1, description="Return results starting from this page"
    ),
    cursor: str | None = Query(
        None, description="Return results starting from this cursor"
    ),
):
    """Retrieves a list of project translation items, ungrouped.

    You may want to request Keys resource in order to get the structured key/translation pairs for all languages.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/translations

    Requires read_translations OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/translations/{translation_id}", response_model=TranslationResponse)
async def get_project_translation(
    project_id: str = Path(..., description="A unique project identifier"),
    translation_id: int = Path(..., description="Unique translation identifier"),
    disable_references: int | None = Query(
        None,
        ge=0,
        le=1,
        description="Whether to disable key references. Possible values are 1 and 0.",
    ),
):
    """Retrieves a Translation object.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/translations/{translation_id}

    Requires read_translations OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/translations/{translation_id}", response_model=TranslationResponse)
async def update_project_translation(
    project_id: str = Path(..., description="A unique project identifier"),
    translation_id: int = Path(..., description="Unique translation identifier"),
    request: TranslationUpdateRequest = ...,
):
    """Updates a translation. Alternatively, use the Multi-key update endpoint to update translations.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/translations/{translation_id}

    Requires write_translations OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
