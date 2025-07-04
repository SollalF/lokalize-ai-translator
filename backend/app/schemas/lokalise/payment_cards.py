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


class UserPaymentCardsResponse(BaseModel):
    """Response schema for user payment cards."""

    user_id: int = Field(..., description="The user identifier")
    payment_cards: list[PaymentCard] = Field(
        ..., description="List of user payment cards"
    )


class UserPaymentCardResponse(BaseModel):
    """Response schema for single user payment card."""

    user_id: int = Field(..., description="The user identifier")
    payment_cards: PaymentCard = Field(..., description="Single user payment card")


class PaymentCardDeleteResponse(BaseModel):
    """Response schema for payment card deletion."""

    card_id: int = Field(..., description="A unique identifier of the card")
    card_deleted: bool = Field(
        ..., description="Whether the card was successfully deleted"
    )


class PaymentCardCreateRequest(BaseModel):
    """Request schema for creating a payment card."""

    number: str = Field(..., description="Card number")
    cvc: str = Field(..., description="3-digit card CVC code")
    exp_month: int = Field(..., description="Card expiration month (1-12)", ge=1, le=12)
    exp_year: int = Field(..., description="Card expiration year")
