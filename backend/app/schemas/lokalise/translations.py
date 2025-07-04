from pydantic import BaseModel, Field

from .translation_status import CustomTranslationStatus


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
    translation: str | dict = Field(
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


class TranslationResponse(BaseModel):
    """Response schema for translation operations."""

    translation: Translation


class TranslationsResponse(BaseModel):
    """Response schema for multiple translations."""

    translations: list[Translation]
