from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Comment object schema for Lokalise API."""

    comment_id: int = Field(..., description="A unique identifier of the comment")
    key_id: int | None = Field(
        None, description="Identifier of a key, the comment is attached to"
    )
    comment: str = Field(..., description="The comment message")
    added_by: int = Field(
        ..., description="Identifier of a user, who has left the comment"
    )
    added_by_email: str = Field(
        ..., description="E-mail of a user, who has left the comment"
    )
    added_at: str = Field(..., description="Date and time the comment was added")
    added_at_timestamp: int = Field(
        ..., description="Unix timestamp the comment was added"
    )


class CommentResponse(BaseModel):
    """Response schema for comment operations."""

    comment: Comment


class CommentsResponse(BaseModel):
    """Response schema for multiple comments."""

    comments: list[Comment]


# Response schema including project_id as defined by the API docs
class ProjectCommentsResponse(BaseModel):
    """Response schema for listing project comments."""

    project_id: str = Field(..., description="A unique project identifier")
    comments: list[Comment] = Field(..., description="List of comments in the project")


# ----- Request/Response for creating comments -----


class CommentCreateItem(BaseModel):
    """Single comment item for create request."""

    comment: str = Field(..., description="The comment to add")


class CommentCreateRequest(BaseModel):
    """Request schema for adding comments to a key."""

    comments: list[CommentCreateItem] = Field(
        ..., description="A set of comments to add"
    )


class ProjectCommentResponse(BaseModel):
    """Response schema for creating a comment (single comment returned)."""

    project_id: str = Field(..., description="A unique project identifier")
    comment: Comment = Field(..., description="Created comment object")


# Response for deleting a comment
class CommentDeleteResponse(BaseModel):
    """Response schema for deleting a comment."""

    project_id: str = Field(..., description="A unique project identifier")
    comment_deleted: bool = Field(..., description="Whether the comment was deleted")
