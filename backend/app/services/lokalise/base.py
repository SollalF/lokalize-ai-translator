from typing import Any

import httpx
from fastapi import HTTPException

from app.core.config import get_settings
from app.core.logging import logger


class LokaliseBaseService:
    """Base service for interacting with Lokalise API via direct HTTP calls."""

    def __init__(self):
        settings = get_settings()
        if not settings.LOKALISE_API_TOKEN:
            raise ValueError("Lokalise API token is not configured")

        self.api_token = settings.LOKALISE_API_TOKEN
        self.base_url = "https://api.lokalise.com/api2"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Api-Token": self.api_token,
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to Lokalise API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=30.0,
            )

            await self._handle_http_error(response, endpoint)
            return response.json()

    async def _handle_http_error(self, response: httpx.Response, endpoint: str) -> None:
        """Handle HTTP errors and convert to appropriate FastAPI exceptions."""
        if response.is_success:
            return

        try:
            error_data = response.json()
            error_message = error_data.get("error", {}).get(
                "message", str(response.text)
            )
        except Exception:
            error_message = f"HTTP {response.status_code}: {response.text}"

        logger.error(f"Lokalise API error for {endpoint}: {error_message}")

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid Lokalise API token")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Resource not found")
        elif response.status_code == 429:
            raise HTTPException(
                status_code=429, detail="Lokalise API rate limit exceeded"
            )
        elif response.status_code == 400:
            raise HTTPException(
                status_code=400, detail=f"Invalid data: {error_message}"
            )
        elif response.status_code == 409:
            raise HTTPException(status_code=409, detail=error_message)
        else:
            raise HTTPException(
                status_code=500, detail=f"Lokalise API error: {error_message}"
            )
