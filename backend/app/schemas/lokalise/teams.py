from pydantic import BaseModel, Field


class TeamQuotaUsage(BaseModel):
    """Current quota usage for a team."""

    users: int = Field(..., description="Number of users in the team")
    keys: int = Field(..., description="Number of keys used across all team projects")
    projects: int = Field(..., description="Number of projects in the team")
    mau: int = Field(
        ...,
        description="Number of monthly active users (for Lokalise SDK) - deprecated",
    )
    trafficBytes: int = Field(..., description="Number of bytes used in Lokalise OTA")
    ai_words: int = Field(
        ..., description="Number of Lokalise AI words consumed by the team"
    )


class TeamQuotaAllowed(BaseModel):
    """Quotas allocated to the team."""

    users: int = Field(..., description="Total number of users allocated to the team")
    keys: int = Field(
        ..., description="Total number of keys allocated across all team projects"
    )
    projects: int = Field(
        ..., description="Total number of projects allocated to the team"
    )
    mau: int = Field(
        ...,
        description="Total number of monthly active users allocated to the team (for Lokalise SDK) - deprecated",
    )
    trafficBytes: int = Field(
        ..., description="Number of bytes allowed in Lokalise OTA"
    )
    ai_words: int = Field(
        ..., description="Total number of Lokalise AI words allocated to the team"
    )


class Team(BaseModel):
    """Team object schema for Lokalise API."""

    team_id: int = Field(..., description="A unique team identifier")
    name: str = Field(..., description="Team name")
    created_at: str = Field(..., description="Date and time when team was created")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the team was created"
    )
    plan: str = Field(..., description="Current subscription plan of the team")
    logo_url: str = Field(..., description="Logo url of a team")
    role: str = Field(..., description="Role in a team for a requesting user")
    quota_usage: TeamQuotaUsage = Field(..., description="Current quota usage")
    quota_allowed: TeamQuotaAllowed = Field(
        ..., description="Quotas allocated to the team"
    )
    is_team_suspended: bool = Field(..., description="If team is suspended")
    is_end_of_trial_active: bool = Field(
        ..., description="Shows if end of trial period happened already"
    )
    trial_days_left: int = Field(..., description="Shows days of trial left")


class TeamsResponse(BaseModel):
    """Response schema for listing teams."""

    teams: list[Team] = Field(..., description="List of teams available to the user")


class TeamResponse(BaseModel):
    """Response schema for retrieving a single team."""

    team: Team = Field(..., description="The team object")
