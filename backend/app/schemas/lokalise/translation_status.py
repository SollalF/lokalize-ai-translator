from pydantic import BaseModel, Field


class CustomTranslationStatus(BaseModel):
    """Custom translation status object schema for Lokalise API."""

    status_id: int = Field(
        ..., description="A unique custom translation status identifier"
    )
    title: str = Field(..., description="Status title")
    color: str = Field(..., description="Hex color of the status")


class CustomTranslationStatusResponse(BaseModel):
    """Response schema for custom translation status operations."""

    custom_translation_status: CustomTranslationStatus


class CustomTranslationStatusesResponse(BaseModel):
    """Response schema for multiple custom translation statuses."""

    custom_translation_statuses: list[CustomTranslationStatus]
