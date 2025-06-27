from pydantic import BaseModel, Field


class Snapshot(BaseModel):
    """Snapshot object schema for Lokalise API."""

    snapshot_id: int = Field(..., description="A unique identifier of the snapshot")
    title: str = Field(..., description="Snapshot title")
    created_at: str = Field(..., description="Date and time of the snapshot creation")
    created_at_timestamp: str = Field(
        ..., description="Unix timestamp when the snapshot was created"
    )
    created_by: int = Field(
        ..., description="Identifier of a user, who has created the snapshot"
    )
    created_by_email: str = Field(
        ..., description="E-mail of a user, who has created the snapshot"
    )


class SnapshotResponse(BaseModel):
    """Response schema for snapshot operations."""

    snapshot: Snapshot


class SnapshotsResponse(BaseModel):
    """Response schema for multiple snapshots."""

    snapshots: list[Snapshot]
