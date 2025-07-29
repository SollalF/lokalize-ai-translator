from fastapi import APIRouter, Path, Query

from app.schemas.lokalise.glossary import (
    GlossaryTermResponse,
    GlossaryTermsCreate,
    GlossaryTermsCreateResponse,
    GlossaryTermsDelete,
    GlossaryTermsDeleteResponse,
    GlossaryTermsResponse,
    GlossaryTermsUpdate,
    GlossaryTermsUpdateResponse,
)
from app.services.lokalise.glossary import lokalise_glossary_service

router = APIRouter(tags=["lokalise-glossary"])


@router.get("/glossary-terms", response_model=GlossaryTermsResponse)
async def list_glossary_terms(
    project_id: str = Path(..., description="A unique project identifier"),
    limit: int | None = Query(
        None, ge=1, le=500, description="Number of items to include (max 500)"
    ),
    cursor: int | None = Query(
        None, description="Return results starting from this cursor"
    ),
):
    """Retrieve a list of glossary terms.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/glossary-terms

    Retrieves a list of glossary terms with their translations, tags, and metadata.
    Supports cursor-based pagination for efficient traversal of large glossaries.

    Requires read_glossary OAuth access scope.
    """
    return await lokalise_glossary_service.get_glossary_terms(
        project_id=project_id, limit=limit, cursor=cursor
    )


@router.get("/glossary-terms/{term_id}", response_model=GlossaryTermResponse)
async def get_glossary_term(
    project_id: str = Path(..., description="A unique project identifier"),
    term_id: int = Path(..., description="A unique glossary term identifier"),
):
    """Retrieve a specific glossary term.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/glossary-terms/{term_id}

    Retrieves a Glossary Term object with all its associated data including
    translations, tags, and metadata.

    Requires read_glossary OAuth access scope.
    """
    term = await lokalise_glossary_service.get_glossary_term(
        project_id=project_id, term_id=term_id
    )
    return GlossaryTermResponse(data=term)


@router.post(
    "/glossary-terms", response_model=GlossaryTermsCreateResponse, status_code=200
)
async def create_glossary_terms(
    project_id: str = Path(..., description="A unique project identifier"),
    request: GlossaryTermsCreate = ...,
):
    """Create one or more glossary terms in the project.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/glossary-terms

    Creates one or more glossary terms in the project. Requires
    Manage glossary admin right. Returns the created terms and
    metadata about the operation including any errors.

    Requires write_glossary OAuth access scope.
    """
    return await lokalise_glossary_service.create_glossary_terms(
        project_id=project_id, request=request
    )


@router.put(
    "/glossary-terms", response_model=GlossaryTermsUpdateResponse, status_code=200
)
async def update_glossary_terms(
    project_id: str = Path(..., description="A unique project identifier"),
    request: GlossaryTermsUpdate = ...,
):
    """Update one or more glossary terms in the project.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/glossary-terms

    Updates one or more glossary terms in the project. Requires
    Manage glossary admin right. Returns the updated terms and
    metadata about the operation including any errors.

    Requires write_glossary OAuth access scope.
    """
    return await lokalise_glossary_service.update_glossary_terms(
        project_id=project_id, request=request
    )


@router.delete(
    "/glossary-terms", response_model=GlossaryTermsDeleteResponse, status_code=200
)
async def delete_glossary_terms(
    project_id: str = Path(..., description="A unique project identifier"),
    request: GlossaryTermsDelete = ...,
):
    """Delete multiple glossary terms from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/glossary-terms

    Deletes all specified glossary terms from the project. Requires
    Manage glossary admin right. Returns information about successfully
    deleted terms and any that failed to delete.

    Requires write_glossary OAuth access scope.
    """
    return await lokalise_glossary_service.delete_glossary_terms(
        project_id=project_id, request=request
    )
