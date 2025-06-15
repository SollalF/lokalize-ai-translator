from pydantic import BaseModel, Field

# Placeholder for future project-related schemas
# Example schemas to add:
# - Project
# - ProjectSettings
# - Language
# - Contributor
# - ProjectStats


class QAIssues(BaseModel):
    """QA issues breakdown object."""

    not_reviewed: int = Field(0, description="Count of not reviewed translations")
    unverified: int = Field(0, description="Count of unverified translations")
    spelling_grammar: int = Field(
        0, description="Count of translations with spelling and/or grammar errors"
    )
    inconsistent_placeholders: int = Field(
        0,
        description="Count of translations with inconsistent placeholders (source vs target)",
    )
    inconsistent_html: int = Field(
        0,
        description="Count of translations with inconsistent HTML tags (source vs target)",
    )
    different_number_of_urls: int = Field(
        0,
        description="Count of translations with different number of URLs (source vs target)",
    )
    different_urls: int = Field(
        0, description="Count of translations with different URLs (source vs target)"
    )
    leading_whitespace: int = Field(
        0, description="Count of translations with leading whitespace"
    )
    trailing_whitespace: int = Field(
        0, description="Count of translations with trailing whitespace"
    )
    different_number_of_email_address: int = Field(
        0,
        description="Count of translations with different number of email address (source vs target)",
    )
    different_email_address: int = Field(
        0,
        description="Count of translations with different email address (source vs target)",
    )
    different_brackets: int = Field(
        0,
        description="Count of translations with different brackets (source vs target)",
    )
    different_numbers: int = Field(
        0, description="Count of translations with different numbers (source vs target)"
    )
    double_space: int = Field(
        0, description="Count of translations with double spaces (target)"
    )
    special_placeholder: int = Field(
        0,
        description="Count of invalid use of [VOID], [TRUE], [FALSE] placeholders (target)",
    )
    unbalanced_brackets: int = Field(
        0, description="Count of unbalanced brackets (target)"
    )


class ProjectLanguage(BaseModel):
    """Project language with progress information."""

    language_id: int = Field(
        ..., description="A unique language identifier in the system"
    )
    language_iso: str = Field(..., description="Language/locale code")
    progress: float = Field(..., description="Translated keys percent")
    words_to_do: int = Field(
        ...,
        description="Count of words remaining to translate from projects base language",
    )


class ProjectStatistics(BaseModel):
    """Project statistics object containing progress and QA information."""

    progress_total: float = Field(
        ..., description="Overall percent of project progress"
    )
    keys_total: int = Field(..., description="Count of keys in the project")
    team: int = Field(..., description="Team members count in the project")
    base_words: int = Field(
        ..., description="Count of words in a base language of the project"
    )
    qa_issues_total: int = Field(
        ..., description="Overall count of QA issues in the project"
    )
    qa_issues: QAIssues = Field(
        ..., description="An object containing count for each QA issue type"
    )


class ProjectSettings(BaseModel):
    """Project settings object containing various configuration options."""

    per_platform_key_names: bool = Field(
        False,
        description="If enabled project has different key names for different platforms",
    )
    reviewing: bool = Field(
        False, description="If enabled contributors has reviewer access for project"
    )
    auto_toggle_unverified: bool = Field(
        False,
        description="If enabled Lokalise will automatically mark translations Unverified in case translation of base language was changed",
    )
    offline_translation: bool = Field(
        False,
        description="If enabled translators are able to download and upload translations as XLIFF files from the Editor",
    )
    key_editing: bool = Field(
        False, description="If enabled keys are allowed to be modified"
    )
    inline_machine_translations: bool = Field(
        False,
        description="If enabled inline machine translations are enabled to all project users",
    )
    branching: bool = Field(
        False, description="If enabled then branching will be available"
    )
    segmentation: bool = Field(
        False, description="If enabled then segmentation will be available"
    )
    custom_translation_statuses: bool = Field(
        False,
        description="If enabled then custom translation statuses will be available",
    )
    custom_translation_statuses_allow_multiple: bool = Field(
        False,
        description="If enabled then multiple custom translation statuses will be allowed",
    )
    contributor_preview_download_enabled: bool = Field(
        False,
        description="If enabled then translators will be allowed to preview content by downloading target files from the Editor",
    )


class Project(BaseModel):
    """Complete Project object from Lokalise API."""

    project_id: str = Field(..., description="A unique project identifier")
    project_type: str = Field(
        ...,
        description="Project type descriptor. Allowed values are localization_files or paged_documents",
    )
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Description of the project")
    created_at: str = Field(..., description="Date of project creation")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when project was created"
    )
    created_by: int = Field(
        ..., description="An identifier of a user who has created the project"
    )
    created_by_email: str = Field(
        ..., description="An e-mail of a user who has created the project"
    )
    team_id: int = Field(
        ..., description="A unique identifier of the team, the project belongs to"
    )
    base_language_id: int = Field(
        ..., description="A unique identifier of the project default language"
    )
    base_language_iso: str = Field(
        ..., description="A language/locale code of the project default language"
    )
    settings: ProjectSettings = Field(
        ..., description="An object containing project settings"
    )
    statistics: ProjectStatistics = Field(
        ...,
        description="An object containing project statistics, QA issues and project languages progress",
    )
    languages: list[ProjectLanguage] = Field(
        ..., description="An array of project languages with progress percent"
    )


class ProjectResponse(BaseModel):
    """Response structure for single project API call."""

    data: Project


class ProjectsResponse(BaseModel):
    """Response structure for multiple projects API call."""

    data: list[Project]


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(..., description="Project name", min_length=1)
    description: str = Field("", description="Description of the project")
    project_type: str = Field(
        "localization_files", description="Project type descriptor"
    )
    base_language_iso: str = Field(
        "en", description="A language/locale code of the project default language"
    )
    settings: ProjectSettings | None = Field(None, description="Project settings")


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: str | None = Field(None, description="Project name")
    description: str | None = Field(None, description="Description of the project")
    settings: ProjectSettings | None = Field(None, description="Project settings")


class ProjectFilters(BaseModel):
    """Query parameters for filtering projects."""

    filter_team_id: int | None = Field(None, description="Limit results to team ID")
    filter_names: str | None = Field(
        None, description="One or more project names to filter by (comma separated)"
    )
    include_statistics: int | None = Field(
        1,
        description="Whether to include project statistics. Possible values are 1 and 0",
    )
    include_settings: int | None = Field(
        1,
        description="Whether to include project settings. Possible values are 1 and 0",
    )
    limit: int | None = Field(
        None, description="Number of items to include (max 5000)", le=5000
    )
    page: int | None = Field(
        None, description="Return results starting from this page", ge=1
    )


class ProjectsListResponse(BaseModel):
    """Response structure for list projects API call with metadata."""

    projects: list[Project] = Field(..., description="Array of project objects")
    total_count: int | None = Field(
        None, description="Total count of projects (from X-Total-Count header)"
    )
