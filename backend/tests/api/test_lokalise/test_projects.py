"""
Pytest tests for Lokalise API parity between our service and Lokalise API.
Run with: pytest tests/api/test_lokalise/test_projects.py -v
"""

import pytest

from ...utils.test_parity import manual_comparison, tester


class TestProjectsAPI:
    """Test suite for projects API endpoints."""

    @pytest.mark.asyncio
    async def test_projects_list_with_full_data(self):
        """Test projects list endpoint with statistics and settings."""
        result = await manual_comparison(
            lokalise_endpoint="projects",
            our_endpoint="api/v1/lokalise/projects/",
            params={"include_statistics": 1, "include_settings": 1, "limit": 3},
        )

        assert result["matches"], (
            f"Projects list endpoint mismatch: {result['differences']}"
        )

    @pytest.mark.asyncio
    async def test_projects_list_minimal_data(self):
        """Test projects list endpoint without statistics and settings."""
        result = await manual_comparison(
            lokalise_endpoint="projects",
            our_endpoint="api/v1/lokalise/projects/",
            params={"include_statistics": 0, "include_settings": 0, "limit": 2},
        )

        assert result["matches"], (
            f"Projects list minimal endpoint mismatch: {result['differences']}"
        )

    @pytest.mark.asyncio
    async def test_single_project(self):
        """Test single project endpoint."""
        # First get a project ID
        projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

        if not projects_data.get("projects"):
            pytest.skip("No projects available for testing")

        project_id = projects_data["projects"][0]["project_id"]

        result = await manual_comparison(
            lokalise_endpoint=f"projects/{project_id}",
            our_endpoint=f"api/v1/lokalise/projects/{project_id}",
        )

        assert result["matches"], (
            f"Single project endpoint mismatch: {result['differences']}"
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "params",
        [
            {"include_statistics": 1, "include_settings": 1, "limit": 1},
            {"include_statistics": 0, "include_settings": 1, "limit": 2},
            {"include_statistics": 1, "include_settings": 0, "limit": 1},
            {"limit": 5},
        ],
    )
    async def test_projects_list_parameter_variations(self, params):
        """Test projects list with various parameter combinations."""
        result = await manual_comparison(
            lokalise_endpoint="projects",
            our_endpoint="api/v1/lokalise/projects/",
            params=params,
        )

        assert result["matches"], (
            f"Projects list with params {params} mismatch: {result['differences']}"
        )


class TestProjectCRUDOperations:
    """Test suite for project CRUD operations (create, update, delete, empty)."""

    @pytest.mark.asyncio
    async def test_create_project_not_implemented(self):
        """Test that project creation endpoint is not yet implemented."""
        # Test that POST to projects endpoint returns 501
        from fastapi.testclient import TestClient

        from app.main import app

        client = TestClient(app)
        response = client.post(
            "/api/v1/lokalise/projects/",
            json={"name": "Test Project", "team_id": 511396},
        )

        assert response.status_code == 501, (
            f"Expected 501 Not Implemented, got {response.status_code}: {response.text}"
        )

    @pytest.mark.asyncio
    async def test_update_project_not_implemented(self):
        """Test that project update endpoint is not yet implemented."""
        # Get a project ID first
        projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

        if not projects_data.get("projects"):
            pytest.skip("No projects available for testing")

        project_id = projects_data["projects"][0]["project_id"]

        # Test that PUT to project endpoint returns 501
        from fastapi.testclient import TestClient

        from app.main import app

        client = TestClient(app)
        response = client.put(
            f"/api/v1/lokalise/projects/{project_id}",
            json={"name": "Updated Project Name"},
        )

        assert response.status_code == 501, (
            f"Expected 501 Not Implemented, got {response.status_code}: {response.text}"
        )

    @pytest.mark.asyncio
    async def test_delete_project_not_implemented(self):
        """Test that project deletion endpoint is not yet implemented."""
        # Get a project ID first
        projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

        if not projects_data.get("projects"):
            pytest.skip("No projects available for testing")

        project_id = projects_data["projects"][0]["project_id"]

        # Test that DELETE to project endpoint returns 501
        from fastapi.testclient import TestClient

        from app.main import app

        client = TestClient(app)
        response = client.delete(f"/api/v1/lokalise/projects/{project_id}")

        assert response.status_code == 501, (
            f"Expected 501 Not Implemented, got {response.status_code}: {response.text}"
        )

    @pytest.mark.asyncio
    async def test_empty_project_not_implemented(self):
        """Test that project empty endpoint is not yet implemented."""
        # Get a project ID first
        projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

        if not projects_data.get("projects"):
            pytest.skip("No projects available for testing")

        project_id = projects_data["projects"][0]["project_id"]

        # Test that PUT to project empty endpoint returns 501
        from fastapi.testclient import TestClient

        from app.main import app

        client = TestClient(app)
        response = client.put(f"/api/v1/lokalise/projects/{project_id}/empty")

        assert response.status_code == 501, (
            f"Expected 501 Not Implemented, got {response.status_code}: {response.text}"
        )


class TestFutureEndpoints:
    """Test suite for endpoints that will be implemented in the future."""

    @pytest.mark.asyncio
    async def test_project_keys_not_implemented(self):
        """Test that project keys endpoint is not yet implemented."""
        # Get a project ID first
        projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

        if not projects_data.get("projects"):
            pytest.skip("No projects available for testing")

        project_id = projects_data["projects"][0]["project_id"]

        # This should fail until you implement the keys endpoint
        with pytest.raises(AssertionError, match="501"):
            await manual_comparison(
                lokalise_endpoint=f"projects/{project_id}/keys",
                our_endpoint=f"api/v1/lokalise/projects/{project_id}/keys",
                params={"limit": 5},
            )

    @pytest.mark.asyncio
    async def test_project_languages_not_implemented(self):
        """Test that project languages endpoint is not yet implemented."""
        # Get a project ID first
        projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

        if not projects_data.get("projects"):
            pytest.skip("No projects available for testing")

        project_id = projects_data["projects"][0]["project_id"]

        # This should fail until you implement the languages endpoint
        with pytest.raises(AssertionError, match="501"):
            await manual_comparison(
                lokalise_endpoint=f"projects/{project_id}/languages",
                our_endpoint=f"api/v1/lokalise/projects/{project_id}/languages",
            )


# You can add more test classes here as you implement more endpoints
# class TestKeysAPI:
#     @pytest.mark.asyncio
#     async def test_project_keys_list(self):
#         ...
#
# class TestLanguagesAPI:
#     @pytest.mark.asyncio
#     async def test_project_languages_list(self):
#         ...
