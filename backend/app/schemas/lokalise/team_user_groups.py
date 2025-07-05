from pydantic import BaseModel, Field


class TeamUserGroupLanguage(BaseModel):
    """Language object within team user group permissions."""

    lang_id: int = Field(..., description="Language ID")
    lang_iso: str = Field(..., description="Language code")
    lang_name: str = Field(..., description="Language name")
    is_writable: bool = Field(
        ..., description="Whether the user has write access to the language"
    )


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
    languages: list[TeamUserGroupLanguage] = Field(
        ..., description="List of languages, accessible to the user"
    )


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
    members: list[int] = Field(..., description="List of group members (user IDs)")
    role_id: int = Field(
        ...,
        description="Permission template id attached to the group",
    )


class TeamUserGroupResponse(BaseModel):
    """Response schema for team user group operations."""

    group: TeamUserGroup


class TeamUserGroupsResponse(BaseModel):
    """Response schema for multiple team user groups."""

    groups: list[TeamUserGroup]


class GroupCreateLanguages(BaseModel):
    """Languages object for group creation."""

    reference: list[str] = Field(
        ..., description="List of reference language IDs for the group"
    )
    contributable: list[str] = Field(
        ..., description="List of contributable language IDs for the group"
    )


class GroupCreateRequest(BaseModel):
    """Request schema for creating a group."""

    name: str = Field(..., description="Name of the group")
    is_reviewer: bool = Field(
        ...,
        description="Whether the group has reviewer access to the project. From the new permission release onwards is deprecated",
    )
    is_admin: bool = Field(
        ...,
        description="Whether the group has Admin access to the project. From the new permission release onwards is deprecated",
    )
    role_id: int | None = Field(
        None,
        description="Permission template id to grab permissions from, if provided admin_rights is ignored",
    )
    admin_rights: list[str] | None = Field(
        None,
        description="List of group permissions. Possible values are activity,contributors,branches_create,branches_main_modify,branches_merge,custom_status_modify,download,glossary,glossary_edit,glossary_delete,keys,manage_languages,review,screenshots,settings,statistics,tasks,upload",
    )
    languages: GroupCreateLanguages | None = Field(
        None, description="Required if group doesn't have admin rights"
    )


class GroupUpdateRequest(BaseModel):
    """Request schema for updating a group."""

    name: str = Field(..., description="Name of the group")
    is_reviewer: bool = Field(
        ...,
        description="Whether the group has Reviewer access to the project. From the new permission release onwards is deprecated",
    )
    is_admin: bool = Field(
        ...,
        description="Whether the group has Admin access to the project. From the new permission release onwards is deprecated",
    )
    role_id: int | None = Field(
        None,
        description="Permission template id to grab permissions from, if provided admin_rights is ignored",
    )
    admin_rights: list[str] | None = Field(
        None,
        description="List of group permissions. Possible values are activity,contributors,branches_create,branches_main_modify,branches_merge,custom_status_modify,download,glossary,glossary_edit,glossary_delete,keys,manage_languages,review,screenshots,settings,statistics,tasks,upload",
    )
    languages: GroupCreateLanguages | None = Field(
        None, description="Required if group doesn't have admin rights"
    )


class GroupAddProjectsRequest(BaseModel):
    """Request schema for adding projects to a group."""

    projects: list[str] = Field(..., description="List of project IDs to add to group")


class GroupAddMembersRequest(BaseModel):
    """Request schema for adding members to a group."""

    users: list[str] = Field(..., description="List of user IDs to add to group")


class GroupRemoveMembersRequest(BaseModel):
    """Request schema for removing members from a group."""

    users: list[str] = Field(..., description="List of user IDs to remove from group")


class GroupDeleteResponse(BaseModel):
    """Response schema for group deletion."""

    team_id: int = Field(..., description="A unique team identifier")
    group_deleted: bool = Field(
        ..., description="Whether the group was successfully deleted"
    )


class TeamGroupResponse(BaseModel):
    """Response schema for single team group."""

    team_id: int = Field(..., description="A unique team identifier")
    group: TeamUserGroup = Field(..., description="The group object")


class TeamGroupsResponse(BaseModel):
    """Response schema for listing team groups."""

    team_id: int = Field(..., description="A unique team identifier")
    user_groups: list[TeamUserGroup] = Field(
        ..., description="List of user groups in the team"
    )
