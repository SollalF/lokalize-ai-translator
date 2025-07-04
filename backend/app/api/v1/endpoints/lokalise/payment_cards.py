"""Payment Cards endpoints for Lokalise API."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.lokalise import (
    PaymentCard,
    PaymentCardCreateRequest,
    PaymentCardDeleteResponse,
    UserPaymentCardResponse,
    UserPaymentCardsResponse,
)

router = APIRouter(prefix="/payment_cards", tags=["Payment Cards"])


@router.post("", response_model=PaymentCard)
async def create_card(
    card_data: PaymentCardCreateRequest,
) -> PaymentCard:
    """
    Add new payment card to user cards.

    Adds new payment card to user cards.

    Requires write_payment_cards OAuth access scope.

    Args:
        card_data: Payment card creation data (number, cvc, exp_month, exp_year)

    Returns:
        PaymentCard: Created payment card object
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("", response_model=UserPaymentCardsResponse)
async def list_all_cards(
    limit: Annotated[
        int | None,
        Query(
            description="Number of items to include (max 5000)",
            ge=1,
            le=5000,
        ),
    ] = None,
    page: Annotated[
        int | None,
        Query(
            description="Return results starting from this page",
            ge=1,
        ),
    ] = None,
) -> UserPaymentCardsResponse:
    """
    List all user payment cards.

    Lists all user payment cards.

    Requires read_payment_cards OAuth access scope.

    Args:
        limit: Number of items to include (max 5000)
        page: Return results starting from this page

    Returns:
        UserPaymentCardsResponse: User payment cards with user_id and cards list
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{card_id}", response_model=UserPaymentCardResponse)
async def retrieve_card(
    card_id: Annotated[
        int,
        Path(
            description="A unique identifier of the card",
            ge=1,
        ),
    ],
) -> UserPaymentCardResponse:
    """
    Retrieve a Payment card object.

    Retrieves a Payment card object.

    Requires read_payment_cards OAuth access scope.

    Args:
        card_id: A unique identifier of the card

    Returns:
        UserPaymentCardResponse: User payment card with user_id and single card object
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{card_id}", response_model=PaymentCardDeleteResponse)
async def delete_card(
    card_id: Annotated[
        int,
        Path(
            description="A unique identifier of the card",
            ge=1,
        ),
    ],
) -> PaymentCardDeleteResponse:
    """
    Delete a payment card from user cards.

    Deletes a payment card from user cards.

    Requires write_payment_cards OAuth access scope.

    Args:
        card_id: A unique identifier of the card

    Returns:
        PaymentCardDeleteResponse: Deletion status with card_id and card_deleted boolean
    """
    raise HTTPException(status_code=501, detail="Not implemented")
