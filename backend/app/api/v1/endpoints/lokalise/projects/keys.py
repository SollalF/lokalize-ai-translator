from typing import Literal

from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.keys import (
    KeyDeleteResponse,
    KeysCreateRequest,
    KeysDeleteRequest,
    KeysDeleteResponse,
    KeySingleUpdateRequest,
    KeysUpdateRequest,
    KeyUpdateResponse,
    ProjectKeyResponse,
    ProjectKeysResponse,
)

router = APIRouter(tags=["lokalise-keys"])


@router.get("/keys", response_model=ProjectKeysResponse)
async def list_project_keys(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    disable_references: int | None = Query(
        0, ge=0, le=1, description="Whether to disable key references"
    ),
    include_comments: int | None = Query(
        0, ge=0, le=1, description="Whether to include comments"
    ),
    include_screenshots: int | None = Query(
        0, ge=0, le=1, description="Whether to include URL to screenshots"
    ),
    include_translations: int | None = Query(
        0, ge=0, le=1, description="Whether to include translations"
    ),
    filter_translation_lang_ids: str | None = Query(
        None, description="One or more language ID to filter by (comma separated)"
    ),
    filter_tags: str | None = Query(
        None, description="One or more tags to filter by (comma separated)"
    ),
    filter_filenames: str | None = Query(
        None, description="One or more filenames to filter by (comma separated)"
    ),
    filter_keys: str | None = Query(
        None, description="One or more key name to filter by (comma separated)"
    ),
    filter_key_ids: str | None = Query(
        None, description="One or more key identifiers to filter by (comma separated)"
    ),
    filter_platforms: str | None = Query(
        None, description="One or more platforms to filter by (comma separated)"
    ),
    filter_untranslated: int | None = Query(
        0, ge=0, le=1, description="Filter by untranslated keys"
    ),
    filter_qa_issues: str | None = Query(
        None, description="One or more QA issues to filter by (comma separated)"
    ),
    filter_archived: Literal["include", "exclude", "only"] | None = Query(
        "include", description="Archived filter"
    ),
    pagination: Literal["offset", "cursor"] | None = Query(
        "offset", description="Type of pagination"
    ),
    limit: int | None = Query(
        100, ge=1, le=500, description="Number of items to include (max 500)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
    cursor: str | None = Query(
        None, description="Return results starting from this cursor"
    ),
):
    """List all keys in the project.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/keys

    IMPORTANT: This endpoint should not be called on every user visit. Instead,
    fetch results periodically, store them locally, and serve static content.
    Consider using the File Download endpoint with cloud storage integration.

    Requires read_keys OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/keys/{key_id}", response_model=ProjectKeyResponse)
async def get_key(
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    disable_references: int | None = Query(
        0, ge=0, le=1, description="Whether to disable key references"
    ),
):
    """Retrieve a specific key from the project.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/keys/{key_id}

    Retrieves a Key object with all its associated data including translations,
    comments, and screenshots.

    Requires read_keys OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/keys/{key_id}", response_model=ProjectKeyResponse, status_code=200)
async def update_key(
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    request: KeySingleUpdateRequest = ...,
):
    """Update the properties of a key and its associated objects.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/keys/{key_id}

    Updates the properties of a key and its associated objects. Requires
    Manage keys admin right.

    Requires write_keys OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/keys/{key_id}", response_model=KeyDeleteResponse, status_code=200)
async def delete_key(
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
):
    """Delete a key from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/keys/{key_id}

    Deletes a key from the project. Requires Manage keys admin right.

    Requires write_keys OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/keys", response_model=ProjectKeysResponse, status_code=200)
async def create_keys(
    project_id: str = Path(..., description="A unique project identifier"),
    request: KeysCreateRequest = ...,
):
    """Create one or more keys in the project.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/keys

    Creates one or more keys in the project. Requires Manage keys admin right.
    We recommend sending payload in chunks of up to 500 keys per request.

    Requires write_keys OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/keys", response_model=KeyUpdateResponse, status_code=200)
async def update_keys(
    project_id: str = Path(..., description="A unique project identifier"),
    request: KeysUpdateRequest = ...,
):
    """Update one or more keys in the project (multi-update).

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/keys

    Updates one or more keys in the project. Requires Manage keys admin right.
    Supports merge options for tags and custom translation statuses.

    Requires write_keys OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/keys", response_model=KeysDeleteResponse, status_code=200)
async def delete_keys(
    project_id: str = Path(..., description="A unique project identifier"),
    request: KeysDeleteRequest = ...,
):
    """Delete multiple keys from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/keys

    Deletes multiple keys from the project. Requires Manage keys admin right.
    Returns information about successfully removed keys and any locked keys.

    Requires write_keys OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
