from pydantic import BaseModel, Field

from app.schemas.lokalise.queued_processes import QueuedProcess


class File(BaseModel):
    """File object schema for Lokalise API."""

    file_id: int = Field(..., description="A unique identifier of the file")
    filename: str = Field(..., description="File name")
    key_count: int = Field(
        ..., description="Total number of keys, associated with this file"
    )


class FileResponse(BaseModel):
    """Response schema for file operations."""

    file: File


class FilesResponse(BaseModel):
    """Response schema for multiple files."""

    files: list[File]


# Response including project_id
class ProjectFilesResponse(BaseModel):
    """Response schema for listing project files."""

    project_id: str = Field(..., description="A unique project identifier")
    files: list[File] = Field(..., description="Project files with key counts")


class FileUploadRequest(BaseModel):
    """Request schema for uploading a file."""

    data: str = Field(..., description="Base64 encoded file")
    filename: str = Field(..., description="Set the filename")
    lang_iso: str = Field(
        ..., description="Language code of the translations in the file"
    )
    convert_placeholders: bool | None = Field(
        None, description="Enable to automatically convert placeholders"
    )
    detect_icu_plurals: bool | None = Field(
        None,
        description="Enable to automatically detect and parse ICU formatted plurals",
    )
    tags: list[str] | None = Field(None, description="Tag keys with the specified tags")
    tag_inserted_keys: bool | None = Field(
        None, description="Add specified tags to inserted keys"
    )
    tag_updated_keys: bool | None = Field(
        None, description="Add specified tags to updated keys"
    )
    tag_skipped_keys: bool | None = Field(
        None, description="Add specified tags to skipped keys"
    )
    replace_modified: bool | None = Field(
        None, description="Enable to replace translations that have been modified"
    )
    slashn_to_linebreak: bool | None = Field(
        None, description="Enable to replace \\n with a line break"
    )
    keys_to_values: bool | None = Field(
        None, description="Enable to automatically replace values with key names"
    )
    distinguish_by_file: bool | None = Field(
        None, description="Enable to allow keys with similar names to coexist"
    )
    apply_tm: bool | None = Field(
        None,
        description="Enable to automatically apply 100% translation memory matches",
    )
    use_automations: bool | None = Field(
        None, description="Whether to run automations for this upload"
    )
    hidden_from_contributors: bool | None = Field(
        None, description="Enable to automatically set newly created keys as hidden"
    )
    cleanup_mode: bool | None = Field(
        None, description="Enable to delete all keys not present in the uploaded file"
    )
    custom_translation_status_ids: list[str] | None = Field(
        None, description="Custom translation status IDs to be added to translations"
    )
    custom_translation_status_inserted_keys: bool | None = Field(
        None, description="Add custom translation statuses to inserted keys"
    )
    custom_translation_status_updated_keys: bool | None = Field(
        None, description="Add custom translation statuses to updated keys"
    )
    custom_translation_status_skipped_keys: bool | None = Field(
        None, description="Add custom translation statuses to skipped keys"
    )
    skip_detect_lang_iso: bool | None = Field(
        None, description="Skip automatic language detection by filename"
    )
    format: str | None = Field(
        None, description="File format (e.g. json, strings, xml)"
    )
    filter_task_id: int | None = Field(
        None, description="Apply import results as a part of a task"
    )


class FileUploadResponse(BaseModel):
    """Response schema for file upload."""

    project_id: str = Field(..., description="A unique project identifier")
    process: QueuedProcess = Field(..., description="Queued process object")


# ----- File Download Schemas -----


class LanguageMapping(BaseModel):
    """Language mapping object for download request."""

    original_language_iso: str = Field(
        ..., description="Original language code as defined in language settings"
    )
    custom_language_iso: str = Field(
        ..., description="Language code to replace the original one with"
    )


class FileDownloadRequest(BaseModel):
    """Request schema for async file download."""

    format: str = Field(
        ..., description="File format (e.g. json, strings, xml) or SDK bundle type"
    )
    original_filenames: bool | None = Field(
        None, description="Enable to use original filenames/formats"
    )
    bundle_structure: str | None = Field(
        None, description="Bundle structure when original_filenames is false"
    )
    directory_prefix: str | None = Field(
        None, description="Directory prefix when original_filenames is true"
    )
    all_platforms: bool | None = Field(
        None, description="Enable to include all platform keys"
    )
    filter_langs: list[str] | None = Field(
        None, description="List of languages to export"
    )
    filter_data: list[str] | None = Field(None, description="Narrow export data range")
    filter_filenames: list[str] | None = Field(
        None, description="Only keys attributed to selected files"
    )
    add_newline_eof: bool | None = Field(
        None, description="Add new line at end of file"
    )
    custom_translation_status_ids: list[str] | None = Field(
        None, description="Only translations with selected custom statuses"
    )
    include_tags: list[str] | None = Field(
        None, description="Narrow export range to specified tags"
    )
    exclude_tags: list[str] | None = Field(
        None, description="Exclude keys with these tags"
    )
    export_sort: str | None = Field(None, description="Export key sort mode")
    export_empty_as: str | None = Field(
        None, description="How to export empty translations"
    )
    export_null_as: str | None = Field(
        None, description="How to export null translations (Ruby on Rails YAML only)"
    )
    include_comments: bool | None = Field(
        None, description="Include key comments and description"
    )
    include_description: bool | None = Field(
        None, description="Include key description"
    )
    include_pids: list[str] | None = Field(
        None, description="Other project IDs to include"
    )
    triggers: list[str] | None = Field(None, description="Trigger integration exports")
    filter_repositories: list[str] | None = Field(
        None, description="Repositories for pull requests"
    )
    replace_breaks: bool | None = Field(
        None, description="Replace line breaks with \\n"
    )
    disable_references: bool | None = Field(
        None, description="Skip automatic replace of key reference placeholders"
    )
    plural_format: str | None = Field(
        None, description="Override default plural format"
    )
    placeholder_format: str | None = Field(
        None, description="Override default placeholder format"
    )
    webhook_url: str | None = Field(
        None, description="URL to receive POST with bundle URL when complete"
    )
    language_mapping: list[LanguageMapping] | None = Field(
        None, description="Override default ISO codes for export"
    )
    icu_numeric: bool | None = Field(
        None, description="Replace plural forms with numeric equivalents"
    )
    escape_percent: bool | None = Field(
        None, description="Export percent placeholders as double percent"
    )
    indentation: str | None = Field(None, description="Override default indentation")
    yaml_include_root: bool | None = Field(
        None, description="Include language ISO code as root key (YAML only)"
    )
    json_unescaped_slashes: bool | None = Field(
        None, description="Leave forward slashes unescaped (JSON only)"
    )
    java_properties_encoding: str | None = Field(
        None, description="Encoding for .properties files (Java Properties only)"
    )
    java_properties_separator: str | None = Field(
        None, description="Separator for keys/values (Java Properties only)"
    )
    bundle_description: str | None = Field(
        None, description="Description of the created bundle (SDK bundles only)"
    )
    filter_task_id: int | None = Field(
        None, description="Only keys attributed to the task (offline_xliff only)"
    )
    compact: bool | None = Field(
        None, description="Export minimum required structure (ARB only)"
    )


class FileDownloadResponse(BaseModel):
    """Response schema for async file download."""

    process_id: str = Field(..., description="Process ID to track download progress")


class FileSyncDownloadResponse(BaseModel):
    """Response schema for synchronous file download."""

    project_id: str = Field(..., description="A unique project identifier")
    bundle_url: str = Field(..., description="URL to download the generated bundle")


class FileDeleteResponse(BaseModel):
    """Response schema for file deletion."""

    project_id: str = Field(..., description="A unique project identifier")
    file_deleted: bool = Field(
        ..., description="Whether the file was successfully deleted"
    )
