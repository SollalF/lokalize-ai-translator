from typing import Literal

from pydantic import BaseModel, Field


class TaskLanguageUser(BaseModel):
    """User assigned to work on a language in a task."""

    user_id: int = Field(..., description="User identifier")
    email: str = Field(..., description="User email")


class TaskLanguageGroup(BaseModel):
    """Group assigned to work on a language in a task."""

    group_id: int = Field(..., description="Group identifier")
    name: str = Field(..., description="Group name")


class TaskLanguageGroups(BaseModel):
    """Groups assigned to work on a language in a task."""

    groups: list[TaskLanguageGroup] = Field(
        ..., description="List of groups assigned to work on the language"
    )


class TaskLanguageTmLeverage(BaseModel):
    """Translation Memory leverage for a task language."""

    keys_count: int = Field(..., description="Number of keys for the language")
    words_count: int = Field(..., description="Number of source words for the language")


class TaskLanguage(BaseModel):
    """Language object within task schema."""

    language_iso: str = Field(..., description="Language code")
    users: list[TaskLanguageUser] = Field(
        ..., description="List of users, assigned to work on the language"
    )
    groups: TaskLanguageGroups = Field(
        ..., description="List of groups, assigned to work on the language"
    )
    keys: list[int] = Field(
        ..., description="List of keys identifiers, included in task for this language"
    )
    status: Literal["completed", "in progress", "created"] = Field(
        ..., description="Status of the language in the task"
    )
    progress: float = Field(
        ..., description="Language progress in percents (0% - 100%)"
    )
    initial_tm_leverage: TaskLanguageTmLeverage | None = Field(
        None,
        description="Deprecated. We return data for compatibility, but please, rely on 'tm_leverage' instead",
    )
    tm_leverage: TaskLanguageTmLeverage | None = Field(
        None, description="Translation Memory leverage calculated for a task"
    )
    completed_at: str | None = Field(
        None, description="Date and time of the language completion"
    )
    completed_at_timestamp: int | None = Field(
        None, description="Unix timestamp when the language was completed"
    )
    completed_by: int | None = Field(
        None, description="Identifier of a user, who has completed the language"
    )
    completed_by_email: str | None = Field(
        None, description="E-mail of a user, who has completed the language"
    )


class Task(BaseModel):
    """Task object schema for Lokalise API."""

    task_id: int = Field(..., description="A unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Short description of the task")
    status: Literal["completed", "in_progress", "created", "queued"] = Field(
        ..., description="Status of the task"
    )
    progress: float = Field(..., description="Task progress in percents (0% - 100%)")
    due_date: str = Field(..., description="Due date")
    due_date_timestamp: int = Field(..., description="Unix timestamp of the Due date")
    keys_count: int = Field(..., description="Total number of keys in the task")
    words_count: int = Field(
        ..., description="Total number of source words in the task"
    )
    created_at: str = Field(..., description="Date and time of the task creation")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the task was created"
    )
    created_by: int = Field(
        ..., description="Identifier of a user, who has created the task"
    )
    created_by_email: str = Field(
        ..., description="E-mail of a user, who has created the task"
    )
    can_be_parent: bool = Field(
        ..., description="Can task be assigned as a parent task"
    )
    task_type: Literal[
        "translation", "automatic_translation", "lqa_by_ai", "review"
    ] = Field("translation", description="Task type")
    parent_task_id: int | None = Field(None, description="ID of the parent task")
    closing_tags: list[str] = Field(
        ..., description="Tags that will be added to affected keys when task is closed"
    )
    do_lock_translations: bool = Field(
        ...,
        description="If set to true, will lock translations for non-assigned project members",
    )
    languages: list[TaskLanguage] = Field(
        ..., description="List of languages in the task"
    )
    source_language_iso: str = Field(
        ..., description="Source language code of the task"
    )
    auto_close_languages: bool = Field(
        ...,
        description="Whether languages should be closed automatically upon completion of the last item",
    )
    auto_close_task: bool = Field(
        ...,
        description="Whether the task should be automatically closed upon all language completion",
    )
    auto_close_items: bool = Field(
        ...,
        description="Whether the translation task items should be automatically marked as completed on edit",
    )
    completed_at: str | None = Field(
        None, description="Date and time of the task completion"
    )
    completed_at_timestamp: int | None = Field(
        None, description="Unix timestamp when the task was completed"
    )
    completed_by: int | None = Field(
        None, description="Identifier of a user, who has completed the task"
    )
    completed_by_email: str | None = Field(
        None, description="E-mail of a user, who has completed the task"
    )
    custom_translation_status_ids: list[int] = Field(
        ...,
        description="IDs of custom translation statuses that will be applied to task items after item is completed",
    )


class TaskResponse(BaseModel):
    """Response schema for task operations."""

    task: Task


class TasksResponse(BaseModel):
    """Response schema for multiple tasks."""

    tasks: list[Task]


class TaskCreateLanguage(BaseModel):
    """Language object for task creation."""

    language_iso: str = Field(..., description="Language code")
    users: list[int] | None = Field(
        None, description="List of user IDs assigned to work on the language"
    )
    groups: list[int] | None = Field(
        None, description="List of group IDs assigned to work on the language"
    )
    keys: list[int] | None = Field(
        None, description="List of keys identifiers, included in task for this language"
    )


class TaskCreateRequest(BaseModel):
    """Request schema for creating a task."""

    title: str = Field(..., description="Task title")
    description: str | None = Field(
        None,
        description="Brief task description. Used as instructions for AI in automatic_translation and lqa_by_ai task types",
    )
    due_date: str | None = Field(
        None,
        description="Due date in Y-m-d H:i:s format. Example: '2024-12-24 23:59:59'",
    )
    keys: list[str] | None = Field(
        None,
        description="List of keys identifiers, included in task. Required if parent_task_id is not specified",
    )
    languages: list[TaskCreateLanguage] | None = Field(
        None, description="List of languages in the task"
    )
    source_language_iso: str | None = Field(
        None,
        description="Source language code for the task. Falls back to project base language if not provided",
    )
    auto_close_languages: bool | None = Field(
        None,
        description="Whether languages should be closed automatically upon completion of the last item. Must be true or omit the property for automatic_translation and lqa_by_ai task types",
    )
    auto_close_task: bool | None = Field(
        None,
        description="Whether the task should be automatically closed upon all language completion. Must be true or omit the property for automatic_translation and lqa_by_ai task types",
    )
    auto_close_items: bool | None = Field(
        None,
        description="Whether the translation task items should be automatically marked as completed on edit. Must be true or omit the property for automatic_translation and lqa_by_ai task types",
    )
    task_type: Literal[
        "translation", "automatic_translation", "lqa_by_ai", "review"
    ] = Field("translation", description="Task type")
    parent_task_id: int | None = Field(
        None,
        description="If task_type is review, it can have a parent task. Current task will be opened when parent task is closed",
    )
    closing_tags: list[str] | None = Field(
        None, description="Tags that will be added to affected keys when task is closed"
    )
    do_lock_translations: bool | None = Field(
        None,
        description="If set to true, will lock translations for non-assigned project members",
    )
    custom_translation_status_ids: list[str] | None = Field(
        None,
        description="IDs of custom translation statuses that will be applied to task items after item is completed",
    )
    save_ai_translation_to_tm: bool = Field(
        False,
        description="Save AI translations to Translation Memory. Only applicable for tasks with task_type set to automatic_translation",
    )
    apply_ai_tm100_matches: bool = Field(
        False,
        description="Apply 100% translation memory matches. Only applicable for tasks with task_type set to automatic_translation",
    )
    use_tm_as_context: bool = Field(
        False,
        description="Use the best 75%-100% Translation Memory match as context for AI. Only applicable for tasks with task_type set to automatic_translation",
    )


class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task."""

    title: str | None = Field(None, description="Task title")
    description: str | None = Field(
        None,
        description="Brief task description. Used as instructions for AI in automatic_translation and lqa_by_ai task types",
    )
    due_date: str | None = Field(
        None,
        description="Due date in Y-m-d H:i:s format. Example: '2024-12-24 23:59:59'",
    )
    languages: list[TaskCreateLanguage] | None = Field(
        None,
        description="List of languages in the task. This field must be omitted for automatic_translation and lqa_by_ai task types",
    )
    auto_close_languages: bool | None = Field(
        None,
        description="Whether languages should be closed automatically upon completion of the last item. Must be true or omit the property for automatic_translation and lqa_by_ai task types",
    )
    auto_close_task: bool | None = Field(
        None,
        description="Whether the task should be automatically closed upon all language completion. Must be true or omit the property for automatic_translation and lqa_by_ai task types",
    )
    auto_close_items: bool | None = Field(
        None,
        description="Whether the translation task items should be automatically marked as completed on edit. Must be true or omit the property for automatic_translation and lqa_by_ai task types",
    )
    close_task: bool | None = Field(
        None,
        description="Whether the task should be closed and notifications sent. The task cannot be reopened again",
    )
    closing_tags: list[str] | None = Field(
        None, description="Tags that will be added to affected keys when task is closed"
    )
    do_lock_translations: bool | None = Field(
        None,
        description="If set to true, will lock translations for non-assigned project members",
    )


class TaskDeleteResponse(BaseModel):
    """Response schema for task deletion."""

    project_id: str = Field(..., description="A unique project identifier")
    task_deleted: bool = Field(
        ..., description="Whether the task was successfully deleted"
    )


class ProjectTaskResponse(BaseModel):
    """Response schema for single project task."""

    project_id: str = Field(..., description="A unique project identifier")
    task: Task = Field(..., description="The task object")


class ProjectTasksResponse(BaseModel):
    """Response schema for listing project tasks."""

    project_id: str = Field(..., description="A unique project identifier")
    tasks: list[Task] = Field(..., description="List of tasks in the project")
