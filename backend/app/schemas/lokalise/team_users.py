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


class TeamUsersResponse(BaseModel):
    """Response schema for listing team users."""

    team_id: int = Field(..., description="A unique team identifier")
    team_users: list[TeamUser] = Field(..., description="List of team users")


class TeamUserResponse(BaseModel):
    """Response schema for retrieving a single team user."""

    team_id: int = Field(..., description="A unique team identifier")
    team_user: TeamUser = Field(..., description="The team user object")


class TeamUserUpdateRequest(BaseModel):
    """Request schema for updating a team user."""

    role: str = Field(
        ...,
        description="Role of the user. Available roles are owner, admin, member, biller",
    )


class TeamUserDeleteResponse(BaseModel):
    """Response schema for team user deletion."""

    team_id: int = Field(..., description="A unique team identifier")
    team_user_deleted: bool = Field(
        ..., description="Whether the team user was successfully deleted"
    )
