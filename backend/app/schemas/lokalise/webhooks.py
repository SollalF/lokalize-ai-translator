from pydantic import BaseModel, Field


class WebhookEventLangMap(BaseModel):
    """Event language mapping object within webhook schema."""

    event: str = Field(..., description="Event name")
    lang_iso_codes: list[str] = Field(..., description="List of languages iso codes")


class Webhook(BaseModel):
    """Webhook object schema for Lokalise API."""

    webhook_id: str = Field(..., description="A unique identifier of the webhook")
    url: str = Field(..., description="Specified URL")
    branch: str = Field(..., description="If webhook is limited to single branch")
    secret: str = Field(..., description="X-Secret header sent with webhook requests")
    events: list[str] = Field(
        ...,
        description="List of events webhook is subscribed to. See our documentation for available events and payload examples",
    )
    event_lang_map: list[WebhookEventLangMap] = Field(
        ..., description="List of maps with languages assigned to the events"
    )


class WebhookResponse(BaseModel):
    """Response schema for webhook operations."""

    webhook: Webhook


class WebhooksResponse(BaseModel):
    """Response schema for multiple webhooks."""

    webhooks: list[Webhook]
