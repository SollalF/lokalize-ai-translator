"""
Snapshots endpoints for Lokalise API.
"""

from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise import (
    Project,
    ProjectSnapshotResponse,
    ProjectSnapshotsResponse,
    SnapshotCreateRequest,
    SnapshotDeleteResponse,
)

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


@router.get("", response_model=ProjectSnapshotsResponse)
async def list_project_snapshots(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    limit: int | None = Query(
        500, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
) -> ProjectSnapshotsResponse:
    """
    List all snapshots.

    Retrieves a list of project snapshots. Requires Manage settings admin right.

    Requires read_snapshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        limit: Number of items to include (max 5000)
        page: Return results starting from this page

    Returns:
        ProjectSnapshotsResponse: Project snapshots with project_id and snapshots array
    """
    # Set total count header (placeholder)
    response.headers["X-Total-Count"] = "0"

    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("", response_model=ProjectSnapshotResponse)
async def create_project_snapshot(
    request: SnapshotCreateRequest,
    project_id: str = Path(..., description="A unique project identifier"),
) -> ProjectSnapshotResponse:
    """
    Create a snapshot.

    Creates snapshot of the project. Requires Manage settings admin right.

    Requires write_snapshots OAuth access scope.

    Args:
        request: Snapshot creation data with title
        project_id: A unique project identifier

    Returns:
        ProjectSnapshotResponse: Created snapshot with project_id and snapshot object
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{snapshot_id}", response_model=Project)
async def restore_project_snapshot(
    project_id: str = Path(..., description="A unique project identifier"),
    snapshot_id: int = Path(..., description="A unique identifier of the snapshot"),
) -> Project:
    """
    Restore a snapshot.

    Restores project snapshot to a project copy. Requires Manage settings admin right and Admin role in the team.

    Requires write_snapshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        snapshot_id: A unique identifier of the snapshot

    Returns:
        Project: Complete project object with all settings, statistics, and languages
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{snapshot_id}", response_model=SnapshotDeleteResponse)
async def delete_project_snapshot(
    project_id: str = Path(..., description="A unique project identifier"),
    snapshot_id: int = Path(..., description="A unique identifier of the snapshot"),
) -> SnapshotDeleteResponse:
    """
    Delete a snapshot.

    Deletes project snapshot. Requires Manage settings admin right.

    Requires write_snapshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        snapshot_id: A unique identifier of the snapshot

    Returns:
        SnapshotDeleteResponse: Deletion status with project_id and snapshot_deleted boolean
    """
    raise HTTPException(status_code=501, detail="Not implemented")
