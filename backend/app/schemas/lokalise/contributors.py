from pydantic import BaseModel, Field

from .languages import BaseLanguage


class ContributorLanguage(BaseLanguage):
    """Language object within contributor schema."""

    is_writable: bool = Field(
        ..., description="Whether the user has write access to the language"
    )


class Contributor(BaseModel):
    """Contributor object schema for Lokalise API."""

    user_id: int = Field(..., description="A unique identifier of the user")
    email: str = Field(..., description="E-mail associated with this user")
    fullname: str = Field(..., description="Full name as set by the user")
    created_at: str = Field(..., description="Date/time at which the user was created")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the user was created"
    )
    is_admin: bool = Field(
        ...,
        description="Whether the user has Admin access to the project. From the new permission release onwards is deprecated",
    )
    is_reviewer: bool = Field(
        ...,
        description="Whether the user has Reviewer access to the project. From the new permission release onwards is deprecated",
    )
    languages: list[ContributorLanguage] = Field(
        ..., description="List of languages, accessible to the user"
    )
    admin_rights: list[str] = Field(..., description="List of user permissions")
    role_id: int = Field(
        ..., description="Permission template id attached to the contributor"
    )


class ContributorResponse(BaseModel):
    """Response schema for contributor operations."""

    contributor: Contributor


class ContributorsResponse(BaseModel):
    """Response schema for multiple contributors."""

    contributors: list[Contributor]
