from pydantic import BaseModel


class CustomTranslationStatus(BaseModel):
    """Custom Translation Status object."""

    status_id: int | None = None
    title: str | None = None
    color: str | None = None


class Translation(BaseModel):
    """Complete Translation object from Lokalise API."""

    # Core identification
    translation_id: int
    key_id: int
    language_iso: str

    # Content
    translation: str | dict[str, str]  # Can be string or object for plurals

    # Modification tracking
    modified_at: str | None = None
    modified_at_timestamp: int | None = None
    modified_by: int | None = None
    modified_by_email: str | None = None

    # Status flags
    is_unverified: bool = False
    is_reviewed: bool = False
    reviewed_by: int | None = None

    # Metrics
    words: int | None = None

    # Advanced features
    custom_translation_statuses: list[CustomTranslationStatus] = []
    task_id: int | None = None
    segment_number: int = 1


class TranslationUpdate(BaseModel):
    """
    Schema for updating a translation.

    Note: custom_translation_statuses requires the Custom Translation Statuses
    feature to be enabled in your Lokalise project. If not enabled, omit this
    field or set it to None/empty list to avoid API errors.
    """

    translation: str | dict[str, str]
    is_unverified: bool | None = None
    is_reviewed: bool | None = None
    custom_translation_statuses: list[int] | None = (
        None  # List of status IDs (requires feature enabled)
    )


class TranslationCreate(BaseModel):
    """Schema for creating a new translation."""

    key_id: int
    language_iso: str
    translation: str | dict[str, str]
    is_unverified: bool = False
    is_reviewed: bool = False
    custom_translation_statuses: list[int] | None = None


class TranslationFilters(BaseModel):
    """Query parameters for filtering translations."""

    filter_langs: list[str] | None = None
    filter_keys: list[str] | None = None
    filter_key_ids: list[int] | None = None
    filter_is_reviewed: bool | None = None
    filter_unverified: bool | None = None
    filter_qa_issues: list[str] | None = None
