from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.team_user_groups import (
    GroupAddMembersRequest,
    GroupAddProjectsRequest,
    GroupCreateRequest,
    GroupDeleteResponse,
    GroupRemoveMembersRequest,
    GroupUpdateRequest,
    TeamGroupResponse,
    TeamGroupsResponse,
)

router = APIRouter(tags=["lokalise-groups"])


@router.get("/groups", response_model=TeamGroupsResponse)
async def list_team_groups(
    response: Response,
    team_id: int = Path(..., description="A unique team identifier"),
    limit: int | None = Query(
        100, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """List all user groups in the team.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/groups

    Requires read_team_groups OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/groups/{group_id}", response_model=TeamGroupResponse)
async def get_team_group(
    team_id: int = Path(..., description="A unique team identifier"),
    group_id: int = Path(..., description="A unique identifier of the group"),
):
    """Retrieve a User group object.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/groups/{group_id}

    Requires read_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/groups/{group_id}", response_model=TeamGroupResponse)
async def update_team_group(
    team_id: int = Path(..., description="A unique team identifier"),
    group_id: int = Path(..., description="A unique identifier of the group"),
    request: GroupUpdateRequest = ...,
):
    """Update the properties of a group.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/teams/{team_id}/groups/{group_id}

    Updates the properties of a group. Requires Admin right in the team.

    Requires write_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/groups/{group_id}/projects/add", response_model=TeamGroupResponse)
async def add_projects_to_group(
    team_id: int = Path(..., description="A unique team identifier"),
    group_id: int = Path(..., description="A unique identifier of the group"),
    request: GroupAddProjectsRequest = ...,
):
    """Add projects to group.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/teams/{team_id}/groups/{group_id}/projects/add

    Requires Admin right in the team.

    Requires write_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/groups/{group_id}/members/add", response_model=TeamGroupResponse)
async def add_members_to_group(
    team_id: int = Path(..., description="A unique team identifier"),
    group_id: int = Path(..., description="A unique identifier of the group"),
    request: GroupAddMembersRequest = ...,
):
    """Add members to group.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/teams/{team_id}/groups/{group_id}/members/add

    Requires Admin right in the team.

    Requires write_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/groups/{group_id}/members/remove", response_model=TeamGroupResponse)
async def remove_members_from_group(
    team_id: int = Path(..., description="A unique team identifier"),
    group_id: int = Path(..., description="A unique identifier of the group"),
    request: GroupRemoveMembersRequest = ...,
):
    """Remove members from group.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/teams/{team_id}/groups/{group_id}/members/remove

    Requires Admin right in the team.

    Requires write_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/groups/{group_id}/projects/remove", response_model=TeamGroupResponse)
async def remove_projects_from_group(
    team_id: int = Path(..., description="A unique team identifier"),
    group_id: int = Path(..., description="A unique identifier of the group"),
    request: GroupAddProjectsRequest = ...,
):
    """Remove projects from group.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/teams/{team_id}/groups/{group_id}/projects/remove

    Requires Admin right in the team.

    Requires write_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/groups/{group_id}", response_model=GroupDeleteResponse)
async def delete_team_group(
    team_id: int = Path(..., description="A unique team identifier"),
    group_id: int = Path(..., description="A unique identifier of the group"),
):
    """Delete a group from the team.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/teams/{team_id}/groups/{group_id}

    Deletes a group from the team. Requires Admin right in the team.

    Requires write_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/groups", response_model=TeamGroupResponse, status_code=200)
async def create_team_group(
    team_id: int = Path(..., description="A unique team identifier"),
    request: GroupCreateRequest = ...,
):
    """Create a group in the team.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/teams/{team_id}/groups

    Creates a group in the team. Requires Admin right in the team.
    If is_admin flag is set to true, the group would automatically get access to all project languages, overriding supplied languages object.

    Requires write_team_groups OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
