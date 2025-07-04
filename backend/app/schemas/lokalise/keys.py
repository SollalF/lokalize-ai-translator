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
    description: str = Field(..., description="Description of the key")
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


class ProjectKeysResponse(BaseModel):
    """Response schema for listing project keys."""

    project_id: str = Field(..., description="A unique project identifier")
    keys: list[Key] = Field(..., description="List of keys in the project")


class ProjectKeyResponse(BaseModel):
    """Response schema for retrieving a single project key."""

    project_id: str = Field(..., description="A unique project identifier")
    key: Key = Field(..., description="The key object")


# ----- Key Creation Schemas -----


class KeyCommentCreate(BaseModel):
    """Comment object for key creation."""

    comment: str = Field(..., description="The comment message")


class KeyScreenshotCreate(BaseModel):
    """Screenshot object for key creation."""

    title: str | None = Field(None, description="Title of the screenshot")
    description: str | None = Field(None, description="Description of the screenshot")
    screenshot_tags: list[str] | None = Field(
        None, description="List of screenshot tags"
    )
    data: str = Field(
        ...,
        description="Base64 encoded screenshot (with leading image type 'data:image/jpeg;base64,')",
    )


class KeyTranslationCreate(BaseModel):
    """Translation object for key creation."""

    language_iso: str = Field(
        ..., description="Unique code of the language of the translation"
    )
    translation: str = Field(..., description="The actual translation")
    is_reviewed: bool | None = Field(
        None, description="Whether the translation is marked as Reviewed"
    )
    is_unverified: bool | None = Field(
        None, description="Whether the translation is marked as Unverified"
    )
    custom_translation_status_ids: list[str] | None = Field(
        None, description="Custom translation status IDs to assign to translation"
    )


class KeyCreate(BaseModel):
    """Key object for creation request."""

    key_name: str = Field(
        ...,
        description="Key identifier. For Per-platform key names, pass JSON encoded string with platform attributes",
    )
    description: str | None = Field(None, description="Description of the key")
    platforms: list[str] = Field(
        ..., description="List of platforms enabled for this key"
    )
    filenames: KeyFilename | None = Field(
        None, description="Key filename attribute for each platform"
    )
    tags: list[str] | None = Field(None, description="List of tags for this key")
    comments: list[KeyCommentCreate] | None = Field(
        None, description="List of comments for this key"
    )
    screenshots: list[KeyScreenshotCreate] | None = Field(
        None, description="List of screenshots attached to this key"
    )
    translations: list[KeyTranslationCreate] | None = Field(
        None, description="Translations for all languages"
    )
    is_plural: bool | None = Field(None, description="Whether this key is plural")
    plural_name: str | None = Field(
        None, description="Optional custom plural name (used in some formats)"
    )
    is_hidden: bool | None = Field(
        None, description="Whether this key is hidden from non-admins"
    )
    is_archived: bool | None = Field(None, description="Whether this key is archived")
    context: str | None = Field(
        None, description="Optional context of the key (used with some file formats)"
    )
    char_limit: int | None = Field(
        None,
        description="Maximum allowed number of characters in translations for this key",
    )
    custom_attributes: str | None = Field(
        None, description="JSON encoded string containing custom attributes"
    )


class KeysCreateRequest(BaseModel):
    """Request schema for creating keys."""

    keys: list[KeyCreate] = Field(..., description="Keys to be added to the project")
    use_automations: bool | None = Field(
        None, description="Whether to run automations on the new key translations"
    )


# ----- Key Update Schemas -----


class KeyTranslationUpdate(BaseModel):
    """Translation object for key update."""

    language_iso: str = Field(
        ..., description="Unique code of the language of the translation"
    )
    translation: str = Field(..., description="The actual translation")
    is_reviewed: bool | None = Field(
        None, description="Whether the translation is marked as Reviewed"
    )
    is_unverified: bool | None = Field(
        None, description="Whether the translation is marked as Unverified"
    )
    custom_translation_status_ids: list[str] | None = Field(
        None, description="Custom translation status IDs to assign to translation"
    )
    merge_custom_translation_statuses: bool | None = Field(
        None, description="Merge statuses instead of replacing them"
    )


class KeyUpdate(BaseModel):
    """Key object for update request."""

    key_id: int = Field(..., description="A unique identifier of the key")
    key_name: str | None = Field(
        None,
        description="Key identifier. For Per-platform key names, pass JSON encoded string with platform attributes",
    )
    description: str | None = Field(None, description="Description of the key")
    platforms: list[str] | None = Field(
        None, description="List of platforms enabled for this key"
    )
    filenames: KeyFilename | None = Field(
        None, description="Key filename attribute for each platform"
    )
    tags: list[str] | None = Field(None, description="List of tags for this key")
    merge_tags: bool | None = Field(
        None, description="Enable to merge specified tags with current tags"
    )
    comments: list[KeyCommentCreate] | None = Field(
        None, description="List of comments for this key"
    )
    screenshots: list[KeyScreenshotCreate] | None = Field(
        None, description="List of screenshots attached to this key"
    )
    translations: list[KeyTranslationUpdate] | None = Field(
        None, description="Translations for all languages"
    )
    is_plural: bool | None = Field(None, description="Whether this key is plural")
    plural_name: str | None = Field(
        None, description="Optional custom plural name (used in some formats)"
    )
    is_hidden: bool | None = Field(
        None, description="Whether this key is hidden from non-admins"
    )
    is_archived: bool | None = Field(None, description="Whether this key is archived")
    context: str | None = Field(
        None, description="Optional context of the key (used with some file formats)"
    )
    char_limit: int | None = Field(
        None,
        description="Maximum allowed number of characters in translations for this key",
    )
    custom_attributes: str | None = Field(
        None, description="JSON encoded string containing custom attributes"
    )


class KeysUpdateRequest(BaseModel):
    """Request schema for updating keys."""

    keys: list[KeyUpdate] = Field(..., description="Keys to update")
    use_automations: bool | None = Field(
        None, description="Whether to run automations on the updated key translations"
    )


class KeySingleUpdateRequest(BaseModel):
    """Request schema for updating a single key."""

    key_name: str | None = Field(
        None,
        description="Key identifier. For Per-platform key names, pass JSON encoded string with platform attributes",
    )
    description: str | None = Field(None, description="Description of the key")
    platforms: list[str] | None = Field(
        None, description="List of platforms enabled for this key"
    )
    filenames: KeyFilename | None = Field(
        None, description="Key filename attribute for each platform"
    )
    tags: list[str] | None = Field(None, description="List of tags for this key")
    merge_tags: bool | None = Field(
        None, description="Enable to merge specified tags with current tags"
    )
    is_plural: bool | None = Field(None, description="Whether this key is plural")
    plural_name: str | None = Field(
        None, description="Optional custom plural name (used in some formats)"
    )
    is_hidden: bool | None = Field(
        None, description="Whether this key is hidden from non-admins"
    )
    is_archived: bool | None = Field(None, description="Whether this key is archived")
    context: str | None = Field(
        None, description="Optional context of the key (used with some file formats)"
    )
    char_limit: int | None = Field(
        None,
        description="Maximum allowed number of characters in translations for this key",
    )
    custom_attributes: str | None = Field(
        None, description="JSON encoded string containing custom attributes"
    )


class KeyUpdateResponse(BaseModel):
    """Response schema for updating a key."""

    project_id: str = Field(..., description="A unique project identifier")
    key: Key = Field(..., description="Updated key object")


# ----- Key Delete Schemas -----


class KeysDeleteRequest(BaseModel):
    """Request schema for deleting keys."""

    keys: list[str] = Field(..., description="List of key IDs to delete")


class KeysDeleteResponse(BaseModel):
    """Response schema for deleting keys."""

    project_id: str = Field(..., description="A unique project identifier")
    keys_removed: bool = Field(..., description="Whether keys were removed")
    keys_locked: int = Field(
        ..., description="Number of locked keys that couldn't be deleted"
    )


class KeyDeleteResponse(BaseModel):
    """Response schema for deleting a single key."""

    project_id: str = Field(..., description="A unique project identifier")
    key_removed: bool = Field(..., description="Whether the key was removed")
    keys_locked: int = Field(
        ..., description="Number of locked keys that couldn't be deleted"
    )
