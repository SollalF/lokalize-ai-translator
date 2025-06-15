from fastapi import HTTPException

from app.core.config import get_settings
from app.core.logging import logger
from lokalise import Client  # pyright: ignore[reportMissingTypeStubs]


class LokaliseBaseService:
    """Base service for interacting with Lokalise API."""

    client: Client

    def __init__(self):
        settings = get_settings()
        if not settings.LOKALISE_API_TOKEN:
            raise ValueError("Lokalise API token is not configured")
        self.client = Client(settings.LOKALISE_API_TOKEN)

    def _safe_get_attr(self, obj, attr_name, default=None):
        """Safely get attribute from object or dictionary."""
        if isinstance(obj, dict):
            return obj.get(attr_name, default)
        else:
            return getattr(obj, attr_name, default)

    def _handle_api_error(
        self, error: Exception, operation: str, resource_id: str = ""
    ) -> None:
        """Handle common Lokalise API errors and convert to appropriate HTTP exceptions."""
        error_message = str(error)
        resource_info = f" {resource_id}" if resource_id else ""

        logger.error(
            f"Lokalise API error during {operation}{resource_info}: {error_message}"
        )

        if "Invalid API token" in error_message:
            raise HTTPException(
                status_code=401, detail="Invalid Lokalise API token"
            ) from error
        elif "Rate limit exceeded" in error_message:
            raise HTTPException(
                status_code=429, detail="Lokalise API rate limit exceeded"
            ) from error
        elif "Project not found" in error_message:
            raise HTTPException(
                status_code=404, detail="Lokalise project not found"
            ) from error
        elif "Translation not found" in error_message or "404" in error_message:
            raise HTTPException(
                status_code=404, detail=f"Resource not found{resource_info}"
            ) from error
        elif "Custom translation statuses not enabled" in error_message:
            raise HTTPException(
                status_code=409,
                detail="Custom translation statuses are not enabled for this project. Remove custom_translation_statuses from your request or enable this feature in your Lokalise project settings.",
            ) from error
        elif "Validation failed" in error_message or "400" in error_message:
            raise HTTPException(
                status_code=400, detail=f"Invalid data: {error_message}"
            ) from error
        else:
            raise HTTPException(
                status_code=500, detail=f"Lokalise API error: {error_message}"
            ) from error

    def _ensure_int(self, value, default: int = 0) -> int:
        """Safely convert value to integer with fallback."""
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default
