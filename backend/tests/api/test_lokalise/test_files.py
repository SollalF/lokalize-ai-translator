"""
Pytest tests for Lokalise Files API endpoints.
Run with: pytest tests/api/test_lokalise/test_files.py -v
"""

import pytest


class TestFilesAPI:
    """Test suite for Lokalise files API endpoints."""

    @pytest.mark.asyncio
    @pytest.mark.lokalise
    async def test_project_files_list(self):
        """Test project files list endpoint."""
        # TODO: Implement when files endpoint is ready
        pytest.skip("Files list endpoint not yet implemented")

    @pytest.mark.asyncio
    @pytest.mark.lokalise
    async def test_project_files_upload(self):
        """Test project files upload endpoint."""
        # TODO: Implement when files endpoint is ready
        pytest.skip("Files upload endpoint not yet implemented")

    @pytest.mark.asyncio
    @pytest.mark.lokalise
    async def test_project_files_download(self):
        """Test project files download endpoint."""
        # TODO: Implement when files endpoint is ready
        pytest.skip("Files download endpoint not yet implemented")
