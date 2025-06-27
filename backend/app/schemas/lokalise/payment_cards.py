from pydantic import BaseModel, Field


class PaymentCard(BaseModel):
    """Payment card object schema for Lokalise API."""

    card_id: int = Field(..., description="A unique identifier of the card")
    last4: str = Field(..., description="Last 4 digits of the card")
    brand: str = Field(..., description="Card brand")
    created_at: str = Field(..., description="Date/time at which the card was created")
    created_at_timestamp: int = Field(
        ..., description="Unix timestamp when the card was created"
    )


class PaymentCardResponse(BaseModel):
    """Response schema for payment card operations."""

    payment_card: PaymentCard


class PaymentCardsResponse(BaseModel):
    """Response schema for multiple payment cards."""

    payment_cards: list[PaymentCard]
