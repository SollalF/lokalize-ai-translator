from pydantic import BaseModel, Field

from .translation_status import CustomTranslationStatus


class Segment(BaseModel):
    """Segment object schema for Lokalise API."""

    segment_number: int = Field(..., description="Segment number")
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
    value: str | dict = Field(
        ...,
        description="The actual segment content. Pass as an object, in case it includes plural forms and is_plural is true",
    )
    is_fuzzy: bool = Field(
        ...,
        description="Whether the Fuzzy flag is enabled. (Note: Fuzzy is called Unverified in the editor now)",
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


class SegmentResponse(BaseModel):
    """Response schema for segment operations."""

    segment: Segment


class SegmentsResponse(BaseModel):
    """Response schema for multiple segments."""

    segments: list[Segment]
