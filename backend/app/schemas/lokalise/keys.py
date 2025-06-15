from typing import Any

from pydantic import BaseModel


class PlatformKeyNames(BaseModel):
    """Platform-specific key names."""

    ios: str | None = None
    android: str | None = None
    web: str | None = None
    other: str | None = None


class TranslationMetadata(BaseModel):
    """Translation metadata from Lokalise."""

    translation_id: int | None = None
    modified_by: int | None = None
    modified_by_email: str | None = None
    modified_at: str | None = None
    modified_at_timestamp: int | None = None
    is_reviewed: bool = False
    is_unverified: bool = False
    reviewed_by: int | None = None
    words: int | None = None


class TranslationKey(BaseModel):
    """Enhanced model for translation key data from Lokalise."""

    # Basic identification
    key_id: int
    key_name: str | PlatformKeyNames

    # Content
    source_text: str
    translated_text: str | None = None

    # Translation status
    is_translated: bool
    language_code: str

    # Key metadata
    created_at: str | None = None
    created_at_timestamp: int | None = None
    description: str | None = None
    platforms: list[str] = []
    tags: list[str] = []

    # Key properties
    is_plural: bool = False
    plural_name: str | None = None
    is_hidden: bool = False
    is_archived: bool = False
    context: str | None = None
    base_words: int | None = None
    char_limit: int | None = None

    # Translation metadata
    translation_metadata: TranslationMetadata | None = None

    # Timestamps
    modified_at: str | None = None
    modified_at_timestamp: int | None = None
    translations_modified_at: str | None = None
    translations_modified_at_timestamp: int | None = None


class LokaliseKeyFilters(BaseModel):
    """Query parameters for filtering Lokalise keys."""

    untranslated_only: bool = False
    include_archived: bool = False
    include_hidden: bool = False
    platforms: list[str] | None = None
    tags: list[str] | None = None
    reviewed_only: bool = False


# New schemas for creating keys


class KeyFilenames(BaseModel):
    """Platform-specific filenames for a key."""

    ios: str | None = None
    android: str | None = None
    web: str | None = None
    other: str | None = None


class KeyComment(BaseModel):
    """Comment for a key."""

    comment: str


class KeyScreenshot(BaseModel):
    """Screenshot attached to a key."""

    title: str | None = None
    description: str | None = None
    screenshot_tags: list[str] = []
    data: str  # Base64 encoded screenshot with leading image type


class KeyTranslation(BaseModel):
    """Translation for a key during creation."""

    language_iso: str
    translation: str | dict[str, Any]  # Can be string or object for plurals
    is_reviewed: bool = False
    is_unverified: bool = False
    custom_translation_status_ids: list[str] = []


class KeyCreate(BaseModel):
    """Schema for creating a single key."""

    # Required fields
    key_name: str  # For per-platform names, pass JSON encoded string
    platforms: list[str]  # ios, android, web, other

    # Optional fields
    description: str | None = None
    filenames: KeyFilenames | None = None
    tags: list[str] = []
    comments: list[KeyComment] = []
    screenshots: list[KeyScreenshot] = []
    translations: list[KeyTranslation] = []
    is_plural: bool = False
    plural_name: str | None = None
    is_hidden: bool = False
    is_archived: bool = False
    context: str | None = None
    char_limit: int | None = None
    custom_attributes: str | None = None  # JSON encoded string


class KeysCreate(BaseModel):
    """Schema for creating multiple keys."""

    keys: list[KeyCreate]
    use_automations: bool = False  # Whether to run automations on new key translations


class KeyCreateMeta(BaseModel):
    """Meta information from key creation response."""

    count: int
    created: int
    limit: int | None = None
    errors: dict[str, Any] = {}


class KeysCreateResponse(BaseModel):
    """Response structure for create keys API call."""

    data: list[TranslationKey]
    meta: KeyCreateMeta
