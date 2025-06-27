from pydantic import BaseModel, Field


class TaskLanguage(BaseModel):
    """Language object within task schema."""

    language_iso: str = Field(..., description="Language ISO code")
    # Note: The specification mentions "language ISO codes as well as included key IDs,
    # assigned users and groups, translation memory leverage and progress information"
    # but doesn't provide the exact field structure. This would need to be expanded
    # based on actual API responses.


class Task(BaseModel):
    """Task object schema for Lokalise API."""

    task_id: int = Field(..., description="A unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Short description of the task")
    status: str = Field(
        ...,
        description="Status of the task. Allowed values are completed, in_progress, created, queued",
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
    task_type: str = Field(..., description="translation or review")
    parent_task_id: int | None = Field(None, description="ID of the parent task")
    closing_tags: list[str] = Field(
        ..., description="Tags that will be added to affected keys when task is closed"
    )
    do_lock_translations: bool = Field(
        ...,
        description="If set to true, will lock translations for non-assigned project members",
    )
    languages: list[TaskLanguage] = Field(
        ...,
        description="List of languages in the task containing language ISO codes as well as included key IDs, assigned users and groups, translation memory leverage and progress information",
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
