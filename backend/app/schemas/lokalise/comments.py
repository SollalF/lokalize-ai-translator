from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Complete Comment object from Lokalise API.

    Represents a comment attached to a key in a Lokalise project.
    """

    comment_id: int = Field(..., description="A unique identifier of the comment")
    key_id: int = Field(
        ..., description="Identifier of a key, the comment is attached to"
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


class CommentCreate(BaseModel):
    """Schema for creating a single comment."""

    comment: str = Field(..., description="The comment to add")


class CommentsCreate(BaseModel):
    """Schema for creating multiple comments."""

    comments: list[CommentCreate] = Field(..., description="A set of comments to add")


class CommentCreateResponse(BaseModel):
    """Response structure for create comments API call."""

    project_id: str = Field(..., description="A unique project identifier")
    comment: Comment = Field(..., description="The created comment object")


class CommentFilters(BaseModel):
    """Query parameters for filtering key comments."""

    limit: int | None = Field(
        None, description="Number of items to include (max 5000)", le=5000
    )
    page: int | None = Field(
        None, description="Return results starting from this page", ge=1
    )


class KeyCommentsResponse(BaseModel):
    """Response structure for list key comments API call."""

    project_id: str = Field(..., description="A unique project identifier")
    comments: list[Comment] = Field(..., description="Array of comment objects")
    total_count: int | None = Field(
        None, description="Total count of comments (from X-Total-Count header)"
    )
