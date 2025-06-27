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
