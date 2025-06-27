from pydantic import BaseModel, Field


class TeamUser(BaseModel):
    """Team user object schema for Lokalise API."""

    user_id: int = Field(..., description="A unique identifier of the user")
    email: str = Field(..., description="E-mail of the user")
    fullname: str = Field(..., description="User name and last name")
    created_at: str = Field(..., description="Date/time at which the user was created")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the user was created"
    )
    role: str = Field(
        ...,
        description="Role of the user. Available roles are owner, admin, member, biller",
    )


class TeamUserResponse(BaseModel):
    """Response schema for team user operations."""

    team_user: TeamUser


class TeamUsersResponse(BaseModel):
    """Response schema for multiple team users."""

    team_users: list[TeamUser]
