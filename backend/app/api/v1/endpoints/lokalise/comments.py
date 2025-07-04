from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.comments import (
    CommentCreateRequest,
    CommentDeleteResponse,
    ProjectCommentResponse,
    ProjectCommentsResponse,
)

router = APIRouter()


@router.get("/projects/{project_id}/comments", response_model=ProjectCommentsResponse)
async def list_project_comments(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    limit: int | None = Query(
        100, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """Retrieve a list of all comments in a project.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/comments

    Requires read_comments OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get(
    "/projects/{project_id}/keys/{key_id}/comments",
    response_model=ProjectCommentsResponse,
)
async def list_key_comments(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    limit: int | None = Query(
        100, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """Retrieve a list of all comments for a key.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/keys/{key_id}/comments

    Requires read_comments OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(
    "/projects/{project_id}/keys/{key_id}/comments",
    response_model=ProjectCommentResponse,
    status_code=201,
)
async def create_key_comments(
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    request: CommentCreateRequest = ...,
):
    """Add a set of comments to the key.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/keys/{key_id}/comments

    Requires write_comments OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete(
    "/projects/{project_id}/keys/{key_id}/comments/{comment_id}",
    response_model=CommentDeleteResponse,
)
async def delete_comment(
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    comment_id: int = Path(..., description="A unique identifier of the comment"),
):
    """Delete a comment from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/keys/{key_id}/comments/{comment_id}

    Requires write_comments OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
