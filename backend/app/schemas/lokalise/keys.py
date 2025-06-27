from pydantic import BaseModel, Field

from .comments import Comment
from .translation_status import CustomTranslationStatus


class KeyName(BaseModel):
    """Platform-specific key names object."""

    ios: str = Field(..., description="iOS platform key name")
    android: str = Field(..., description="Android platform key name")
    web: str = Field(..., description="Web platform key name")
    other: str = Field(..., description="Other platform key name")


class KeyFilename(BaseModel):
    """Platform-specific filename object."""

    ios: str = Field(..., description="iOS platform filename")
    android: str = Field(..., description="Android platform filename")
    web: str = Field(..., description="Web platform filename")
    other: str = Field(..., description="Other platform filename")


class Screenshot(BaseModel):
    """Screenshot object within key schema."""

    screenshot_id: int = Field(..., description="A unique identifier of the screenshot")
    key_ids: list[int] = Field(
        ..., description="List of key identifiers, the screenshot is attached to"
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


class KeyTranslation(BaseModel):
    """Translation object within key schema."""

    translation_id: int = Field(
        ..., description="Unique identifier of translation entry"
    )
    key_id: int = Field(..., description="A unique identifier of the key")
    language_iso: str = Field(
        ..., description="Unique code of the language of the translation"
    )
    translation: str | dict = Field(
        ...,
        description="The actual translation. Contains an object, in case it includes plural forms and is_plural is true",
    )
    modified_by: int = Field(
        ..., description="Identifier of a user, who has updated the translation"
    )
    modified_by_email: str = Field(
        ..., description="E-mail of a user, who has updated the translation"
    )
    modified_at: str = Field(
        ..., description="Date of last modification of the translation"
    )
    modified_at_timestamp: int = Field(
        ..., description="Unix timestamp of last modification of the translation"
    )
    is_reviewed: bool = Field(
        ..., description="Whether the translation is marked as Reviewed"
    )
    is_unverified: bool = Field(
        ..., description="Whether the translation is marked as Unverified"
    )
    reviewed_by: int | None = Field(
        ...,
        description="Identifier of the user, who has reviewed the translation (if reviewed)",
    )
    words: int = Field(..., description="Number of words in the translation")
    custom_translation_statuses: list[CustomTranslationStatus] = Field(
        ..., description="Array consisting of Custom Translation Status objects"
    )
    task_id: int | None = Field(
        ...,
        description="Identifier of the task, if the key is a part of one, or null if it's not",
    )


class Key(BaseModel):
    """Key object schema for Lokalise API."""

    key_id: int = Field(..., description="A unique identifier of the key")
    created_at: str = Field(..., description="Creation date of the key")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the key was created"
    )
    key_name: str | KeyName = Field(
        ...,
        description="An object containing key names for all platforms or a string. You may need to enable 'Per-platform key names' in project settings",
    )
    filenames: list[KeyFilename] = Field(
        ..., description="An object containing key filename attribute for each platform"
    )
    descripton: str = Field(..., description="Description of the key")
    platforms: list[str] = Field(
        ..., description="List of platforms enabled for this key"
    )
    tags: list[str] = Field(..., description="List of tags for this key")
    comments: list[Comment] = Field(..., description="Comments for this key")
    screenshots: list[Screenshot] = Field(
        ..., description="Screenshots, attached to this key"
    )
    translations: list[KeyTranslation] = Field(
        ..., description="Translations for all languages"
    )
    is_plural: bool = Field(..., description="Whether this key is plural")
    plural_name: str = Field(
        ..., description="Optional custom plural name (used in some formats)"
    )
    is_hidden: bool = Field(
        ..., description="Whether this key is hidden from non-admins (translators)"
    )
    is_archived: bool = Field(..., description="Whether this key is archived")
    context: str = Field(
        ..., description="Optional context of the key (used with some file formats)"
    )
    base_words: int = Field(..., description="Number of words in base language")
    char_limit: int = Field(
        ...,
        description="Maximum allowed number of characters in translations for this key",
    )
    custom_attributes: str = Field(
        ..., description="JSON containing custom attributes (if any)"
    )
    modified_at: str = Field(
        ...,
        description="Date of the latest key update (including screenshots and comments)",
    )
    modified_at_timestamp: int = Field(
        ...,
        description="Unix timestamp of the latest key update (including screenshots and comments)",
    )
    translations_modified_at: str = Field(
        ..., description="Date of the latest key translation update"
    )
    translations_modified_at_timestamp: int = Field(
        ..., description="Unix timestamp of the latest key translation update"
    )


class KeyResponse(BaseModel):
    """Response schema for key operations."""

    key: Key


class KeysResponse(BaseModel):
    """Response schema for multiple keys."""

    keys: list[Key]
