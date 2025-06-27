from pydantic import BaseModel, Field


class TeamQuota(BaseModel):
    """Quota object for both usage and allocation within team schema."""

    users: int = Field(..., description="Number of users")
    keys: int = Field(..., description="Number of keys")
    projects: int = Field(..., description="Number of projects")
    mau: int = Field(
        ..., description="Number of monthly active users (for Lokalise SDK)"
    )
    ai_words: int = Field(..., description="Number of Lokalise AI words")


class Team(BaseModel):
    """Team object schema for Lokalise API."""

    team_id: int = Field(..., description="A unique team identifier")
    name: str = Field(..., description="Team name")
    created_at: str = Field(..., description="Date and time when team was created")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the team was created"
    )
    plan: str = Field(..., description="Current subscription plan of the team")
    quota_usage: TeamQuota = Field(
        ...,
        description="Current quota usage. Contains users (number of users in the team), keys (number of keys used across all team projects), projects (number of projects in the team), mau (number of monthly active users for Lokalise SDK), ai_words (number of Lokalise AI words consumed by the team in the subscription period)",
    )
    quota_allowed: TeamQuota = Field(
        ...,
        description="Quotas allocated to the team. Contains users (total number of users allocated to the team), keys (total number of keys allocated across all team projects), projects (total number of projects allocated to the team), mau (total number of monthly active users allocated to the team for Lokalise SDK), ai_words (total number of Lokalise AI words allocated to the team in the subscription period)",
    )


class TeamResponse(BaseModel):
    """Response schema for team operations."""

    team: Team


class TeamsResponse(BaseModel):
    """Response schema for multiple teams."""

    teams: list[Team]
