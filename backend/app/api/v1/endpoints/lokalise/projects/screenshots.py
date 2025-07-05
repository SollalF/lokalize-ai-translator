"""Screenshots endpoints for Lokalise API."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.lokalise.screenshots import (
    ProjectScreenshotResponse,
    ProjectScreenshotsResponse,
    ScreenshotDeleteResponse,
    ScreenshotsCreateRequest,
    ScreenshotUpdateRequest,
)

router = APIRouter(tags=["lokalise-screenshots"])


@router.post("/screenshots", response_model=ProjectScreenshotsResponse)
async def create_screenshots(
    project_id: Annotated[
        str,
        Path(description="A unique project identifier"),
    ],
    request: ScreenshotsCreateRequest,
) -> ProjectScreenshotsResponse:
    """
    Create one or more screenshots in the project.

    Creates one or more screenshots in the project. Requires Manage screenshots admin right.

    Requires write_screenshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        request: Screenshots creation data with list of screenshot objects

    Returns:
        ProjectScreenshotsResponse: Created screenshots with project_id and screenshots list
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/screenshots/{screenshot_id}", response_model=ProjectScreenshotResponse)
async def retrieve_screenshot(
    project_id: Annotated[
        str,
        Path(description="A unique project identifier"),
    ],
    screenshot_id: Annotated[
        int,
        Path(description="A unique identifier of the screenshot"),
    ],
) -> ProjectScreenshotResponse:
    """
    Retrieve a Screenshot object.

    Retrieves a Screenshot object.

    Requires read_screenshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        screenshot_id: A unique identifier of the screenshot

    Returns:
        ProjectScreenshotResponse: Project screenshot with project_id and single screenshot object
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/screenshots/{screenshot_id}", response_model=ScreenshotDeleteResponse)
async def delete_screenshot(
    project_id: Annotated[
        str,
        Path(description="A unique project identifier"),
    ],
    screenshot_id: Annotated[
        int,
        Path(description="A unique identifier of the screenshot"),
    ],
) -> ScreenshotDeleteResponse:
    """
    Delete a screenshot from the project.

    Deletes a screenshot from the project. Requires Manage screenshots admin right.

    Requires write_screenshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        screenshot_id: A unique identifier of the screenshot

    Returns:
        ScreenshotDeleteResponse: Deletion status with project_id and screenshot_deleted boolean
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/screenshots/{screenshot_id}", response_model=ProjectScreenshotResponse)
async def update_screenshot(
    project_id: Annotated[
        str,
        Path(description="A unique project identifier"),
    ],
    screenshot_id: Annotated[
        int,
        Path(description="A unique identifier of the screenshot"),
    ],
    request: ScreenshotUpdateRequest,
) -> ProjectScreenshotResponse:
    """
    Update the properties of a screenshot.

    Updates the properties of a screenshot. Requires Manage screenshots admin right.

    Requires write_screenshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        screenshot_id: A unique identifier of the screenshot
        request: Screenshot update data (title, description, key_ids, tags)

    Returns:
        ProjectScreenshotResponse: Updated screenshot with project_id and single screenshot object
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/screenshots", response_model=ProjectScreenshotsResponse)
async def list_screenshots(
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
) -> ProjectScreenshotsResponse:
    """
    Retrieve a list of screenshots from the project.

    Retrieves a list of screenshots from the project.

    Requires read_screenshots OAuth access scope.

    Args:
        project_id: A unique project identifier
        limit: Number of items to include (max 5000)
        page: Return results starting from this page

    Returns:
        ProjectScreenshotsResponse: Project screenshots with project_id and screenshots list
    """
    raise HTTPException(status_code=501, detail="Not implemented")
