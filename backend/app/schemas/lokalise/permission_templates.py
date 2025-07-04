from pydantic import BaseModel, Field


class PermissionTemplate(BaseModel):
    """Permission template object schema for Lokalise API."""

    id: int = Field(..., description="Id of permission template")
    role: str = Field(..., description="Name of a permission template holder")
    permissions: list[str] = Field(
        ..., description="List of permissions in simple list format"
    )
    description: str = Field(..., description="Description of a permission template")
    tag: str = Field(
        ...,
        description="Tag type attached to the role, needed only for display purposes",
    )
    tagColor: str = Field(  # noqa: N815
        ..., description="Attached tag colour for displaying in interface"
    )
    tagInfo: str = Field(  # noqa: N815
        ..., description="Helper for a tag for displaying in interface"
    )
    doesEnableAllReadOnlyLanguages: bool = Field(  # noqa: N815
        ...,
        description="Shows if permission template enables all read only languages (calculated based on permissions attached)",
    )


class PermissionTemplateResponse(BaseModel):
    """Response schema for permission template operations."""

    permission_template: PermissionTemplate


class PermissionTemplatesResponse(BaseModel):
    """Response schema for multiple permission templates."""

    permission_templates: list[PermissionTemplate]


class TeamRolesResponse(BaseModel):
    """Response schema for team roles (permission templates)."""

    roles: list[PermissionTemplate] = Field(
        ..., description="List of permission templates for the team"
    )
