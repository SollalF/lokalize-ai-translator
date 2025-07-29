"""
Pytest tests for Lokalise Translations API endpoints.
Run with: pytest tests/api/test_lokalise/test_translations.py -v
"""

import pytest


class TestTranslationsAPI:
    """Test suite for Lokalise translations API endpoints."""

    @pytest.mark.asyncio
    @pytest.mark.lokalise
    async def test_project_translations_list(self):
        """Test project translations list endpoint."""
        # TODO: Implement when translations endpoint is ready
        pytest.skip("Translations list endpoint not yet implemented")

    @pytest.mark.asyncio
    @pytest.mark.lokalise
    async def test_project_translations_update(self):
        """Test project translations update endpoint."""
        # TODO: Implement when translations endpoint is ready
        pytest.skip("Translations update endpoint not yet implemented")
