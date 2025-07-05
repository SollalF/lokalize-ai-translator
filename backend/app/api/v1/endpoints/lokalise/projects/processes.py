"""Processes endpoints for Lokalise API."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.lokalise.queued_processes import (
    ProjectProcessesResponse,
    ProjectProcessResponse,
)

router = APIRouter(tags=["lokalise-processes"])


@router.get("/processes", response_model=ProjectProcessesResponse)
async def list_processes(
    project_id: Annotated[
        str,
        Path(description="A unique project identifier"),
    ],
    limit: Annotated[
        int | None,
        Query(
            description="Number of items to include (max 5000)",
            ge=1,
            le=5000,
        ),
    ] = None,
    page: Annotated[
        int | None,
        Query(
            description="Return results starting from this page",
            ge=1,
        ),
    ] = None,
) -> ProjectProcessesResponse:
    """
    Retrieve a list of Queued process objects.

    Retrieves a list of Queued process objects.

    Requires read_background_processes OAuth access scope.

    Args:
        project_id: A unique project identifier
        limit: Number of items to include (max 5000)
        page: Return results starting from this page

    Returns:
        ProjectProcessesResponse: Project processes with project_id and processes list
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/processes/{process_id}", response_model=ProjectProcessResponse)
async def retrieve_process(
    project_id: Annotated[
        str,
        Path(description="A unique project identifier"),
    ],
    process_id: Annotated[
        str,
        Path(description="A unique process identifier"),
    ],
) -> ProjectProcessResponse:
    """
    Retrieve a Queued process object.

    Retrieves a Queued process object with an additional details field containing
    information for a specific process type.

    Requires read_background_processes OAuth access scope.

    Args:
        project_id: A unique project identifier
        process_id: A unique process identifier

    Returns:
        ProjectProcessResponse: Project process with project_id and single process object
    """
    raise HTTPException(status_code=501, detail="Not implemented")
