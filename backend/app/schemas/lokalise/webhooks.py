from pydantic import BaseModel, Field


class WebhookEventLangMap(BaseModel):
    """Event language mapping object within webhook schema."""

    event: str = Field(..., description="Event name")
    lang_iso_codes: list[str] = Field(..., description="List of languages iso codes")


class Webhook(BaseModel):
    """Webhook object schema for Lokalise API."""

    webhook_id: str = Field(..., description="A unique identifier of the webhook")
    url: str = Field(..., description="Specified URL")
    branch: str | None = Field(
        None, description="If webhook is limited to single branch"
    )
    secret: str = Field(..., description="X-Secret header sent with webhook requests")
    events: list[str] = Field(
        ...,
        description="List of events webhook is subscribed to. See our documentation for available events and payload examples",
    )
    event_lang_map: list[WebhookEventLangMap] = Field(
        ..., description="List of maps with languages assigned to the events"
    )


class WebhooksResponse(BaseModel):
    """Response schema for listing webhooks."""

    project_id: str = Field(..., description="A unique project identifier")
    webhooks: list[Webhook] = Field(..., description="List of configured webhooks")


class WebhookCreateRequest(BaseModel):
    """Request schema for creating a webhook."""

    url: str = Field(..., description="Specify the URL to your endpoint")
    branch: str | None = Field(
        None,
        description="You can limit the usage of the webhook to a specific branch by specifying the name of the branch as a string. If you pass null or skip this attribute, the webhook will be applied to all branches.",
    )
    events: list[str] = Field(
        ...,
        description="List of events to subscribe to. Possible values are project.imported, project.exported, project.deleted, project.snapshot, project.languages.added, project.language.removed , project.language.settings_changed, project.key.added, project.key.modified, project.keys.deleted, project.key.comment.added, project.translation.updated, project.translation.proofread, project.contributor.added, project.contributor.deleted, project.task.created, project.task.closed, project.task.deleted, project.task.language.closed, project.branch.added, project.branch.deleted, project.branch.merged, team.order.created, team.order.completed, team.order.deleted.",
    )
    event_lang_map: list[WebhookEventLangMap] | None = Field(
        None,
        description="Map the event with an array of languages iso codes. Omit this parameter for all languages in the project. Currently only project.translation.updated and project.translation.proofread events can be mapped with languages.",
    )


class WebhookResponse(BaseModel):
    """Response schema for single webhook operations."""

    project_id: str = Field(..., description="A unique project identifier")
    webhook: Webhook = Field(..., description="The webhook object")


class WebhookUpdateRequest(BaseModel):
    """Request schema for updating a webhook."""

    url: str | None = Field(None, description="Update the URL to your endpoint")
    branch: str | None = Field(
        None,
        description="You can limit the usage of the webhook to a specific branch by specifying the name of the branch as a string. If you pass null or skip this attribute, the webhook will be applied to all branches.",
    )
    events: list[str] | None = Field(
        None,
        description="Update the list of subscribed events. Possible values are project.imported, project.exported, project.deleted, project.snapshot, project.languages.added, project.language.removed , project.language.settings_changed, project.key.added, project.key.modified, project.keys.deleted, project.key.comment.added, project.translation.updated, project.translation.proofread, project.contributor.added, project.contributor.deleted, project.task.created, project.task.closed, project.task.deleted, project.task.language.closed, project.branch.added, project.branch.deleted, project.branch.merged, team.order.created, team.order.completed, team.order.deleted.",
    )
    event_lang_map: list[WebhookEventLangMap] | None = Field(
        None,
        description="Map the event with an array of languages iso codes. Omit this parameter for all languages in the project. Currently only project.translation.updated and project.translation.proofread events can be mapped with languages.",
    )


class WebhookDeleteResponse(BaseModel):
    """Response schema for webhook deletion."""

    project_id: str = Field(..., description="A unique project identifier")
    webhook_deleted: bool = Field(
        ..., description="Whether the webhook was successfully deleted"
    )


class WebhookSecretRegenerateResponse(BaseModel):
    """Response schema for webhook secret regeneration."""

    project_id: str = Field(..., description="A unique project identifier")
    secret: str = Field(..., description="The regenerated webhook secret")
