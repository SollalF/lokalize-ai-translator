from pydantic import BaseModel, Field


class QueuedProcess(BaseModel):
    """Queued process object schema for Lokalise API."""

    process_id: str = Field(..., description="A unique process identifier")
    type: str = Field(
        ...,
        description="The type of the process. Can be file-import, sketch-import, bulk-apply-tm, or create-branch-reindex. The latter process type is fired when a branch is created via the Create a branch endpoint, and it is advised to wait until the process finishes before working with the new branch",
    )
    status: str = Field(
        ...,
        description="Current status of the process. Can be queued, pre_processing, running, post_processing, cancelled, finished or failed",
    )
    message: str = Field(
        ...,
        description="Can contain a message related to the current process status (such as an error message)",
    )
    created_by: int = Field(..., description="ID of a user who initiated the process")
    created_by_email: str = Field(
        ..., description="email of a user who initiated the process"
    )
    created_at: str = Field(
        ..., description="Date of when the process was created in the queue"
    )
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp of when the process was created in the queue"
    )


class QueuedProcessResponse(BaseModel):
    """Response schema for queued process operations."""

    process: QueuedProcess


class QueuedProcessesResponse(BaseModel):
    """Response schema for multiple queued processes."""

    processes: list[QueuedProcess]


class ProjectProcessesResponse(BaseModel):
    """Response schema for project queued processes."""

    project_id: str = Field(..., description="A unique project identifier")
    processes: list[QueuedProcess] = Field(..., description="List of queued processes")


class ProjectProcessResponse(BaseModel):
    """Response schema for single project queued process."""

    project_id: str = Field(..., description="A unique project identifier")
    process: QueuedProcess = Field(..., description="Single queued process")
