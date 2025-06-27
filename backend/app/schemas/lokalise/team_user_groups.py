from pydantic import BaseModel, Field


class TeamUserGroupPermissions(BaseModel):
    """Permissions object within team user group schema."""

    is_admin: bool = Field(
        ...,
        description="Whether the user has Admin access to the project. From the new permission release onwards is deprecated",
    )
    is_reviewer: bool = Field(
        ...,
        description="Whether the user has Reviewer access to the project. From the new permission release onwards is deprecated",
    )
    admin_rights: list[str] = Field(
        ..., description="List of group administrative permissions"
    )
    languages: list[str] = Field(
        ..., description="List of languages, accessible to the user"
    )
    # Note: The languages array structure is not fully specified.
    # This might need to be expanded based on actual API responses.


class TeamUserGroup(BaseModel):
    """Team user group object schema for Lokalise API."""

    group_id: int = Field(..., description="A unique identifier of the group")
    name: str = Field(..., description="Name of the group")
    permissions: TeamUserGroupPermissions = Field(
        ..., description="List of group permissions"
    )
    created_at: str = Field(..., description="Date/time at which the group was created")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the group was created"
    )
    team_id: int = Field(..., description="Team identifier")
    projects: list[str] = Field(..., description="List of projects, group is added to")
    # Note: The projects array structure is not fully specified.
    # This might contain project IDs or project objects.
    members: list[int] = Field(..., description="List of group members (user IDs)")
    role_id: int = Field(
        ...,
        description="Permission template id to take permissions from, if this parameter is provided, admin_rights is ignored",
    )


class TeamUserGroupResponse(BaseModel):
    """Response schema for team user group operations."""

    group: TeamUserGroup


class TeamUserGroupsResponse(BaseModel):
    """Response schema for multiple team user groups."""

    groups: list[TeamUserGroup]
