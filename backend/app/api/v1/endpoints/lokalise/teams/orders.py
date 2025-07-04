from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.orders import (
    OrderCreateRequest,
    OrderResponse,
    OrdersResponse,
)

router = APIRouter(tags=["lokalise-orders"])


@router.get("/orders", response_model=OrdersResponse)
async def list_team_orders(
    response: Response,
    team_id: int = Path(..., description="A unique team identifier"),
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """List all translation orders in the team.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/orders

    Lists all translation orders in the team with their complete details including
    status, payment information, source/target languages, word counts, provider
    information, and costs.

    Requires read_team_orders OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_team_order(
    team_id: int = Path(..., description="A unique team identifier"),
    order_id: str = Path(..., description="A unique order identifier"),
):
    """Retrieve a specific order from the team.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/teams/{team_id}/orders/{order_id}

    Retrieves an Order object with all its details including payment information,
    status, source/target languages, keys, word counts, provider information,
    and costs.

    Requires read_team_orders OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/orders", response_model=OrderResponse, status_code=200)
async def create_team_order(
    team_id: int = Path(..., description="A unique team identifier"),
    request: OrderCreateRequest = ...,
):
    """Create a translation order.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/teams/{team_id}/orders

    Creates a translation order for the specified team. You must have admin
    privileges in the project you are placing an order in. Supports dry run
    mode for price estimation without actually placing the order.

    Requires write_team_orders OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
