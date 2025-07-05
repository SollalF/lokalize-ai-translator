from typing import Any

from pydantic import BaseModel, Field


class CustomTranslationStatus(BaseModel):
    """Custom translation status object within translation schema."""

    status_id: int = Field(..., description="Custom translation status ID")
    title: str = Field(..., description="Custom translation status title")


class Translation(BaseModel):
    """Translation object schema for Lokalise API."""

    translation_id: int = Field(..., description="Unique translation identifier")
    key_id: int = Field(..., description="Identifier of the key of the translation")
    language_iso: str = Field(..., description="Language code")
    modified_at: str = Field(
        ..., description="Date and time of last translation modification"
    )
    modified_at_timestamp: int = Field(
        ..., description="Unix timestamp of last translation modification"
    )
    modified_by: int = Field(
        ..., description="Identifier of the user, who made last modification"
    )
    modified_by_email: str = Field(
        ..., description="E-mail of the user, who made last modification"
    )
    translation: str | dict[str, Any] = Field(
        ...,
        description="The actual translation content. Pass as an object, in case it includes plural forms and is_plural is true",
    )
    is_unverified: bool = Field(
        ..., description="Whether the Unverified flag is enabled"
    )
    is_reviewed: bool = Field(..., description="Whether the Reviewed flag is enabled")
    reviewed_by: int | None = Field(
        None,
        description="Identifier of the user, who has reviewed the translation (if reviewed)",
    )
    words: int = Field(..., description="Number of words in the translation")
    custom_translation_statuses: list[CustomTranslationStatus] = Field(
        ..., description="Array consisting of Custom Translation Status objects"
    )
    task_id: int | None = Field(
        None,
        description="Identifier of the task, if the key is a part of one, or null if it's not",
    )
    segment_number: int = Field(
        ...,
        description="If segmentation is used then this is a segment number. If not then it defaults to 1",
    )


class TranslationsResponse(BaseModel):
    """Response schema for listing translations."""

    project_id: str = Field(..., description="A unique project identifier")
    translations: list[Translation] = Field(
        ..., description="List of project translation items"
    )


class TranslationResponse(BaseModel):
    """Response schema for retrieving a single translation."""

    project_id: str = Field(..., description="A unique project identifier")
    translation: Translation = Field(..., description="The translation object")


class TranslationUpdateRequest(BaseModel):
    """Request schema for updating a translation."""

    translation: str | dict[str, Any] = Field(
        ...,
        description="The actual translation content. Use an JSON object for plural keys.",
    )
    is_unverified: bool | None = Field(
        None, description="Whether the Unverified flag is enabled."
    )
    is_reviewed: bool | None = Field(
        True, description="Whether the Reviewed flag is enabled."
    )
    custom_translation_status_ids: list[str] | None = Field(
        None,
        description="Custom translation status IDs to assign to translation (existing statuses will be replaced).",
    )
