from pydantic import BaseModel, Field


class KeyCoordinates(BaseModel):
    """Key coordinates object within screenshot schema."""

    left: int = Field(..., description="x position of the left-top corner")
    top: int = Field(..., description="y position of the left-top corner")
    width: int = Field(..., description="width of the area in pixels")
    height: int = Field(..., description="height of the area in pixels")


class ScreenshotKey(BaseModel):
    """Key object with coordinates within screenshot schema."""

    key_id: int = Field(..., description="A unique identifier of the key")
    coordinates: KeyCoordinates = Field(
        ..., description="Key coordinates of the key area"
    )


class Screenshot(BaseModel):
    """Screenshot object schema for Lokalise API."""

    screenshot_id: int = Field(..., description="A unique identifier of the screenshot")
    key_ids: list[int] = Field(
        ..., description="List of key identifiers, the screenshot is attached to"
    )
    keys: list[ScreenshotKey] = Field(
        ..., description="List of key keys with coordinates"
    )
    url: str = Field(..., description="Link to the screenshot")
    title: str = Field(..., description="Screenshot title")
    description: str = Field(..., description="Description of the screenshot")
    screenshot_tags: list[str] = Field(..., description="List of screenshot tags")
    width: int = Field(..., description="Width of the screenshot, in pixels")
    height: int = Field(..., description="Height of the screenshot, in pixels")
    created_at: str = Field(..., description="Creation date of the screenshot")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the screenshot was created"
    )


class ScreenshotResponse(BaseModel):
    """Response schema for screenshot operations."""

    screenshot: Screenshot


class ScreenshotsResponse(BaseModel):
    """Response schema for multiple screenshots."""

    screenshots: list[Screenshot]


class ProjectScreenshotsResponse(BaseModel):
    """Response schema for project screenshots."""

    project_id: str = Field(..., description="A unique project identifier")
    screenshots: list[Screenshot] = Field(..., description="List of screenshots")


class ProjectScreenshotResponse(BaseModel):
    """Response schema for single project screenshot."""

    project_id: str = Field(..., description="A unique project identifier")
    screenshot: Screenshot = Field(..., description="Single screenshot")


class ScreenshotCreate(BaseModel):
    """Screenshot creation object schema for Lokalise API."""

    data: str = Field(
        ...,
        description="The screenshot, base64 encoded (with leading image type data:image/jpeg;base64,). Supported file formats are JPG and PNG",
    )
    title: str | None = Field(None, description="Set screenshot title (optional)")
    description: str | None = Field(None, description="Set screenshot description")
    ocr: bool | None = Field(
        None,
        description="Try to recognize translations on the image and attach screenshot to all possible keys",
    )
    key_ids: list[str] | None = Field(
        None, description="Attach the screenshot to key IDs specified"
    )
    tags: list[str] | None = Field(
        None, description="List of tags to add to the uploaded screenshot"
    )


class ScreenshotsCreateRequest(BaseModel):
    """Request schema for creating screenshots."""

    screenshots: list[ScreenshotCreate] = Field(
        ..., description="List of the screenshot objects"
    )


class ScreenshotUpdateRequest(BaseModel):
    """Request schema for updating a screenshot."""

    title: str | None = Field(None, description="Set screenshot title (optional)")
    description: str | None = Field(None, description="Set screenshot description")
    key_ids: list[str] | None = Field(
        None, description="Attach the screenshot to key IDs specified"
    )
    tags: list[str] | None = Field(
        None, description="List of tags to add to the uploaded screenshot"
    )


class ScreenshotDeleteResponse(BaseModel):
    """Response schema for screenshot deletion."""

    project_id: str = Field(..., description="A unique project identifier")
    screenshot_deleted: bool = Field(
        ..., description="Whether the screenshot was successfully deleted"
    )
