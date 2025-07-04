from pydantic import BaseModel, Field


class Order(BaseModel):
    """Order object schema for Lokalise API."""

    order_id: str = Field(..., description="A unique order identifier")
    project_id: str = Field(..., description="Project identifier")
    branch: str = Field(..., description="Branch name")
    payment_method: str = Field(
        ...,
        description="Payment method. Possible values are credit_card, team_credit, none. null will be returned for orders made before the attribute was introduced",
    )
    card_id: int | None = Field(
        None, description="Identifier of the card used for payment"
    )
    status: str = Field(
        ...,
        description="Status of the order. Possible values are in progress, completed. processing, draft in case if dry_run equals to true",
    )
    created_at: str = Field(..., description="Date and time of the order creation")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the order was created"
    )
    created_by: int = Field(
        ..., description="Identifier of a user, who has created the order"
    )
    created_by_email: str = Field(
        ..., description="E-mail of a user, who has created the order"
    )
    source_language_iso: str = Field(
        ..., description="Source language code of the order"
    )
    target_language_isos: list[str] = Field(..., description="List of target languages")
    keys: list[str] = Field(
        ..., description="List of keys identifiers, included in the order"
    )
    source_words: dict[str, int] = Field(
        ...,
        description="Object, where object key is target language iso code and value is the translatable word count",
    )
    provider_slug: str = Field(..., description="Translation provider slug")
    translation_style: str = Field(
        ..., description="Style of the translation, applies to gengo provider only"
    )
    translation_tier: int = Field(
        ..., description="Tier of the translation. Tiers depend on provider"
    )
    translation_tier_name: str = Field(..., description="Tier name")
    briefing: str = Field(..., description="Order briefing")
    is_saved_to_translation_memory: bool = Field(
        ..., description="Default true, can be set only with google and deepl providers"
    )
    total: float = Field(
        ..., description="Total cost of the order in major currency units (USD)"
    )


class OrderResponse(BaseModel):
    """Response schema for order operations."""

    order: Order


class OrdersResponse(BaseModel):
    """Response schema for multiple orders."""

    orders: list[Order]


class OrderCreateRequest(BaseModel):
    """Request schema for creating a translation order."""

    project_id: str = Field(..., description="Project identifier")
    branch: str | None = Field(None, description="Branch name")
    payment_method: str = Field(
        "credit_card",
        description="Payment method. Possible values are credit_card (default) or team_credit",
    )
    card_id: int | None = Field(
        None,
        description="Identifier of the card used for payment. Required if payment_method = credit_card",
    )
    briefing: str = Field(..., description="Order briefing")
    source_language_iso: str = Field(
        ..., description="Source language code of the order"
    )
    target_language_isos: list[str] = Field(..., description="List of target languages")
    keys: list[str] = Field(
        ..., description="List of keys identifiers, included in the order"
    )
    provider_slug: str = Field(..., description="Translation provider slug")
    translation_tier: int = Field(
        ..., description="Tier of the translation. Tiers depend on provider"
    )
    is_saved_to_translation_memory: bool = Field(
        True,
        description="Default true, can be set only with google and deepl providers",
    )
    dry_run: bool = Field(
        False,
        description="Return the response without actually placing an order. Useful for price estimation",
    )
    translation_style: str | None = Field(
        None,
        description="Only for gengo provider. Available values are formal, informal, business, friendly. Defaults to friendly",
    )
