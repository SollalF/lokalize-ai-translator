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


# Response including project_id
class ProjectContributorsResponse(BaseModel):
    """Response schema for listing project contributors."""

    project_id: str = Field(..., description="A unique project identifier")
    contributors: list[Contributor] = Field(
        ..., description="Contributors of the project with access details"
    )


# ----- Schemas for creating contributors -----


class ContributorCreateLanguage(BaseModel):
    """Language access object for contributor creation."""

    lang_iso: str = Field(..., description="Language code")
    is_writable: bool = Field(
        False, description="Whether the user has write access to the language"
    )


class ContributorCreateItem(BaseModel):
    """Single contributor object for create request."""

    email: str = Field(..., description="E-mail of the contributor")
    fullname: str | None = Field(None, description="Full name of the contributor")
    is_admin: bool | None = Field(
        None,
        description="Whether the user has Admin access (deprecated, overrides languages)",
    )
    is_reviewer: bool | None = Field(
        None,
        description="Whether the user has Reviewer access (deprecated)",
    )
    role_id: int | None = Field(
        None, description="Permission template id to take permissions from"
    )
    languages: list[ContributorCreateLanguage] | None = Field(
        None,
        description="List of languages accessible to the user (required if not admin)",
    )
    admin_rights: list[str] | None = Field(
        None,
        description="Custom list of user permissions (ignored if role_id provided)",
    )


class ContributorsCreateRequest(BaseModel):
    """Request schema for creating contributors."""

    contributors: list[ContributorCreateItem] = Field(
        ..., description="A set of contributors to add"
    )


# Request schema for updating a contributor
class ContributorUpdateRequest(BaseModel):
    """Request schema for updating contributor properties."""

    is_admin: bool | None = Field(
        None,
        description="Whether the user has Admin access to the project (deprecated)",
    )
    is_reviewer: bool | None = Field(
        None,
        description="Whether the user has Reviewer access to the project (deprecated)",
    )
    role_id: int | None = Field(
        None,
        description="Permission template id to take permissions from (admin_rights ignored if provided)",
    )
    languages: list[ContributorCreateLanguage] | None = Field(
        None,
        description="Full list of languages accessible to the contributor",
    )
    admin_rights: list[str] | None = Field(
        None,
        description="Custom list of user permissions (ignored if role_id provided)",
    )


class ProjectContributorResponse(BaseModel):
    """Response schema for single created contributor."""

    project_id: str = Field(..., description="A unique project identifier")
    contributor: Contributor = Field(..., description="Created contributor object")


# Response schema for deleting contributor
class ContributorDeleteResponse(BaseModel):
    """Response schema for contributor deletion."""

    project_id: str = Field(..., description="A unique project identifier")
    contributor_deleted: bool = Field(
        ..., description="Whether the contributor was deleted"
    )
