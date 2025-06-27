from pydantic import BaseModel, Field

from .languages import BaseLanguage


class ProjectSettings(BaseModel):
    """Project settings object within project schema."""

    per_platform_key_names: bool = Field(
        ...,
        description="If enabled project has different key names for different platforms",
    )
    reviewing: bool = Field(
        ..., description="If enabled contributors has reviewer access for project"
    )
    auto_toggle_unverified: bool = Field(
        ...,
        description="If enabled Lokalise will automatically mark translations Unverified in case translation of base language was changed",
    )
    offline_translation: bool = Field(
        ...,
        description="If enabled translators are able to download and upload translations as XLIFF files from the Editor",
    )
    key_editing: bool = Field(
        ..., description="If enabled keys are allowed to be modified"
    )
    inline_machine_translations: bool = Field(
        ...,
        description="If enabled inline machine translations are enabled to all project users",
    )
    branching: bool = Field(
        ..., description="If enabled then branching will be available"
    )
    segmentation: bool = Field(
        ..., description="If enabled then segmentation will be available"
    )
    custom_translation_statuses: bool = Field(
        ..., description="If enabled then custom translation statuses will be available"
    )
    custom_translation_statuses_allow_multiple: bool = Field(
        ...,
        description="If enabled then multiple custom translation statuses will be allowed",
    )
    contributor_preview_download_enabled: bool = Field(
        ...,
        description="If enabled then translators will be allowed to preview content by downloading target files from the Editor",
    )


class QAIssues(BaseModel):
    """QA issues object within project statistics."""

    not_reviewed: int = Field(..., description="Count of not reviewed translations")
    unverified: int = Field(..., description="Count of unverified translations")
    spelling_grammar: int = Field(
        ..., description="Count of translations with spelling and/or grammar errors"
    )
    inconsistent_placeholders: int = Field(
        ...,
        description="Count of translations with inconsistent placeholders (source vs target)",
    )
    inconsistent_html: int = Field(
        ...,
        description="Count of translations with inconsistent HTML tags (source vs target)",
    )
    different_number_of_urls: int = Field(
        ...,
        description="Count of translations with different number of URLs (source vs target)",
    )
    different_urls: int = Field(
        ..., description="Count of translations with different URLs (source vs target)"
    )
    leading_whitespace: int = Field(
        ..., description="Count of translations with leading whitespace"
    )
    trailing_whitespace: int = Field(
        ..., description="Count of translations with trailing whitespace"
    )
    different_number_of_email_address: int = Field(
        ...,
        description="Count of translations with different number of email address (source vs target)",
    )
    different_email_address: int = Field(
        ...,
        description="Count of translations with different email address (source vs target)",
    )
    different_brackets: int = Field(
        ...,
        description="Count of translations with different brackets (source vs target)",
    )
    different_numbers: int = Field(
        ...,
        description="Count of translations with different numbers (source vs target)",
    )
    double_space: int = Field(
        ..., description="Count of translations with double spaces (target)"
    )
    special_placeholder: int = Field(
        ...,
        description="Count of invalid use of [VOID], [TRUE], [FALSE] placeholders (target)",
    )
    unbalanced_brackets: int = Field(
        ..., description="Count of unbalanced brackets (target)"
    )


class ProjectStatistics(BaseModel):
    """Project statistics object within project schema."""

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


class ProjectLanguage(BaseLanguage):
    """Project language object with progress information."""

    language_id: int = Field(
        ..., alias="lang_id", description="A unique language identifier in the system"
    )
    language_iso: str = Field(..., alias="lang_iso", description="Language/locale code")

    progress: float = Field(..., description="Translated keys percent")
    words_to_do: int = Field(
        ...,
        description="Count of words remaining to translate from projects base language",
    )

    class Config:
        populate_by_name = True


class Project(BaseModel):
    """Project object schema for Lokalise API."""

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
    """Response schema for project operations."""

    project: Project


class ProjectsResponse(BaseModel):
    """Response schema for multiple projects."""

    projects: list[Project]
