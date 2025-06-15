from .base import LokaliseBaseService


class LokaliseSystemService(LokaliseBaseService):
    """Service for Lokalise system-level operations (non-language specific)."""

    pass


# Create singleton instance
lokalise_system_service = LokaliseSystemService()
