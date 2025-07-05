from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.webhooks import (
    WebhookCreateRequest,
    WebhookDeleteResponse,
    WebhookResponse,
    WebhookSecretRegenerateResponse,
    WebhooksResponse,
    WebhookUpdateRequest,
)

router = APIRouter(tags=["lokalise-project-webhooks"])


@router.get("/webhooks", response_model=WebhooksResponse)
async def list_project_webhooks(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    limit: int | None = Query(
        None, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """Retrieves a list of configured webhooks. Requires Manage settings admin right.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/webhooks

    Requires read_webhooks OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/webhooks", response_model=WebhookResponse, status_code=200)
async def create_project_webhook(
    project_id: str = Path(..., description="A unique project identifier"),
    request: WebhookCreateRequest = ...,
):
    """Creates a webhook in the project. Requires Manage settings admin right. See our documentation for available events and payload examples.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/webhooks

    Requires write_webhooks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/webhooks/{webhook_id}", response_model=WebhookResponse)
async def get_project_webhook(
    project_id: str = Path(..., description="A unique project identifier"),
    webhook_id: str = Path(..., description="A unique identifier of the webhook"),
):
    """Retrieves a Webhook object. Requires Manage settings admin right.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/webhooks/{webhook_id}

    Requires read_webhooks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/webhooks/{webhook_id}", response_model=WebhookResponse)
async def update_project_webhook(
    project_id: str = Path(..., description="A unique project identifier"),
    webhook_id: str = Path(..., description="A unique identifier of the webhook"),
    request: WebhookUpdateRequest = ...,
):
    """Updates a configured webhook in the project. Requires Manage settings admin right.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/webhooks/{webhook_id}

    Requires write_webhooks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/webhooks/{webhook_id}", response_model=WebhookDeleteResponse)
async def delete_project_webhook(
    project_id: str = Path(..., description="A unique project identifier"),
    webhook_id: str = Path(..., description="A unique identifier of the webhook"),
):
    """Deletes a configured webhook in the project. Requires Manage settings admin right.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/webhooks/{webhook_id}

    Requires write_webhooks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.patch(
    "/webhooks/{webhook_id}/secret/regenerate",
    response_model=WebhookSecretRegenerateResponse,
)
async def regenerate_webhook_secret(
    project_id: str = Path(..., description="A unique project identifier"),
    webhook_id: str = Path(..., description="A unique identifier of the webhook"),
):
    """Regenerate a webhook secret. Requires Manage settings admin right.

    Mirrors Lokalise API endpoint:
    PATCH https://api.lokalise.com/api2/projects/{project_id}/webhooks/{webhook_id}/secret/regenerate

    Requires write_webhooks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
