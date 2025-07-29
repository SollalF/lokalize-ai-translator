"""
Lokalise projects service for managing projects via direct API calls.
"""

from app.core.logging import logger
from app.schemas.lokalise.projects import (
    ProjectResponse,
    ProjectsResponse,
)

from .base import LokaliseBaseService


class LokaliseProjectsService(LokaliseBaseService):
    """Service for managing Lokalise projects via direct API calls."""

    async def list_projects(
        self,
        filter_team_id: int | None = None,
        filter_names: str | None = None,
        include_statistics: int | None = 1,
        include_settings: int | None = 1,
        limit: int | None = None,
        page: int | None = None,
    ) -> ProjectsResponse:
        """
        Fetch all projects available to the user.

        Args:
            filter_team_id: Limit results to team ID
            filter_names: One or more project names to filter by (comma separated)
            include_statistics: Whether to include project statistics (0 or 1)
            include_settings: Whether to include project settings (0 or 1)
            limit: Number of items to include (max 5000)
            page: Return results starting from this page

        Returns:
            ProjectsResponse with list of projects

        Raises:
            HTTPException: If the API call fails
        """
        # Build query parameters using dict comprehension
        params = {
            k: v
            for k, v in {
                "filter_team_id": filter_team_id,
                "filter_names": filter_names,
                "include_statistics": include_statistics,
                "include_settings": include_settings,
                "limit": limit,
                "page": page,
            }.items()
            if v is not None
        }

        logger.info(f"Fetching projects with params: {params}")

        # Make direct API call
        data = await self._make_request("GET", "/projects", params=params)

        # Convert response directly to Pydantic model
        projects_response = ProjectsResponse.model_validate(data)

        logger.info(
            f"Retrieved {len(projects_response.projects)} projects from Lokalise"
        )
        return projects_response

    async def get_project(self, project_id: str) -> ProjectResponse:
        """
        Fetch a specific project.

        Args:
            project_id: ID of the project to fetch

        Returns:
            ProjectResponse with project data

        Raises:
            HTTPException: If the API call fails
        """
        logger.info(f"Fetching project {project_id}")

        # Make direct API call
        data = await self._make_request("GET", f"/projects/{project_id}")

        # Convert response directly to Pydantic model
        project_response = ProjectResponse.model_validate(data)

        logger.info(f"Retrieved project: {project_response.project.name}")
        return project_response


# Create singleton instance
lokalise_projects_service = LokaliseProjectsService()
