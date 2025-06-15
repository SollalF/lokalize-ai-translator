from typing import Any

from app.core.logging import logger
from app.schemas.lokalise.projects import (
    Project,
    ProjectFilters,
    ProjectLanguage,
    ProjectSettings,
    ProjectsListResponse,
    ProjectStatistics,
    QAIssues,
)

from .base import LokaliseBaseService


class LokaliseProjectsService(LokaliseBaseService):
    """Service for Lokalise projects operations."""

    async def list_projects(
        self,
        filters: ProjectFilters | None = None,
    ) -> ProjectsListResponse:
        """
        List all projects available to the user.

        Args:
            filters: Optional filters for projects

        Returns:
            ProjectsListResponse with projects list and total count

        Raises:
            HTTPException: For API errors, rate limits, or invalid tokens
        """
        try:
            # Configure API parameters
            params = {}

            if filters:
                if filters.filter_team_id is not None:
                    params["filter_team_id"] = filters.filter_team_id
                if filters.filter_names is not None:
                    params["filter_names"] = filters.filter_names
                if filters.include_statistics is not None:
                    params["include_statistics"] = filters.include_statistics
                if filters.include_settings is not None:
                    params["include_settings"] = filters.include_settings
                if filters.limit is not None:
                    params["limit"] = filters.limit
                if filters.page is not None:
                    params["page"] = filters.page

            # Get projects from Lokalise
            logger.info(f"Fetching projects with params: {params}")
            projects_response = self.client.projects(params)
            logger.info(
                f"Retrieved {len(projects_response.items) if projects_response.items else 0} projects from Lokalise"
            )

            if not projects_response.items:
                logger.warning("No projects found")
                return ProjectsListResponse(
                    projects=[],
                    total_count=0,
                )

            # Format the response data
            result_projects = []
            processed_count = 0

            for project_data in projects_response.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                processed_count += 1
                project_id = self._safe_get_attr(project_data, "project_id", "")
                logger.debug(f"Processing project {processed_count}: {project_id}")

                result_projects.append(self._build_project_object(project_data))

            # Get total count from response headers or metadata
            total_count = len(result_projects)
            if hasattr(projects_response, "total_count"):
                total_count = getattr(projects_response, "total_count", total_count)

            logger.info(f"Successfully processed {len(result_projects)} projects")

            return ProjectsListResponse(
                projects=result_projects, total_count=total_count
            )

        except Exception as e:
            self._handle_api_error(e, "listing projects")
            # Return empty response structure on error (this won't be reached due to exception)
            return ProjectsListResponse(
                projects=[],
                total_count=0,
            )

    def _build_project_object(self, project_data: Any) -> Project:
        """Build a Project object from Lokalise API response data."""

        # Build settings object
        settings_data = self._safe_get_attr(project_data, "settings", {})
        settings = ProjectSettings(
            per_platform_key_names=bool(
                self._safe_get_attr(settings_data, "per_platform_key_names", False)
            ),
            reviewing=bool(self._safe_get_attr(settings_data, "reviewing", False)),
            auto_toggle_unverified=bool(
                self._safe_get_attr(settings_data, "auto_toggle_unverified", False)
            ),
            offline_translation=bool(
                self._safe_get_attr(settings_data, "offline_translation", False)
            ),
            key_editing=bool(self._safe_get_attr(settings_data, "key_editing", False)),
            inline_machine_translations=bool(
                self._safe_get_attr(settings_data, "inline_machine_translations", False)
            ),
            branching=bool(self._safe_get_attr(settings_data, "branching", False)),
            segmentation=bool(
                self._safe_get_attr(settings_data, "segmentation", False)
            ),
            custom_translation_statuses=bool(
                self._safe_get_attr(settings_data, "custom_translation_statuses", False)
            ),
            custom_translation_statuses_allow_multiple=bool(
                self._safe_get_attr(
                    settings_data, "custom_translation_statuses_allow_multiple", False
                )
            ),
            contributor_preview_download_enabled=bool(
                self._safe_get_attr(
                    settings_data, "contributor_preview_download_enabled", False
                )
            ),
        )

        # Build statistics object
        statistics_data = self._safe_get_attr(project_data, "statistics", {})
        qa_issues_data = self._safe_get_attr(statistics_data, "qa_issues", {})

        qa_issues = QAIssues(
            not_reviewed=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "not_reviewed", 0)
            ),
            unverified=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "unverified", 0)
            ),
            spelling_grammar=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "spelling_grammar", 0)
            ),
            inconsistent_placeholders=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "inconsistent_placeholders", 0)
            ),
            inconsistent_html=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "inconsistent_html", 0)
            ),
            different_number_of_urls=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "different_number_of_urls", 0)
            ),
            different_urls=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "different_urls", 0)
            ),
            leading_whitespace=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "leading_whitespace", 0)
            ),
            trailing_whitespace=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "trailing_whitespace", 0)
            ),
            different_number_of_email_address=self._ensure_int(
                self._safe_get_attr(
                    qa_issues_data, "different_number_of_email_address", 0
                )
            ),
            different_email_address=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "different_email_address", 0)
            ),
            different_brackets=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "different_brackets", 0)
            ),
            different_numbers=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "different_numbers", 0)
            ),
            double_space=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "double_space", 0)
            ),
            special_placeholder=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "special_placeholder", 0)
            ),
            unbalanced_brackets=self._ensure_int(
                self._safe_get_attr(qa_issues_data, "unbalanced_brackets", 0)
            ),
        )

        statistics = ProjectStatistics(
            progress_total=float(
                self._safe_get_attr(statistics_data, "progress_total", 0.0)
            ),
            keys_total=self._ensure_int(
                self._safe_get_attr(statistics_data, "keys_total", 0)
            ),
            team=self._ensure_int(self._safe_get_attr(statistics_data, "team", 0)),
            base_words=self._ensure_int(
                self._safe_get_attr(statistics_data, "base_words", 0)
            ),
            qa_issues_total=self._ensure_int(
                self._safe_get_attr(statistics_data, "qa_issues_total", 0)
            ),
            qa_issues=qa_issues,
        )

        # Build languages array
        languages = []
        languages_data = self._safe_get_attr(project_data, "languages", [])
        if languages_data:
            for lang_data in languages_data:
                languages.append(
                    ProjectLanguage(
                        language_id=self._ensure_int(
                            self._safe_get_attr(lang_data, "language_id", 0)
                        ),
                        language_iso=str(
                            self._safe_get_attr(lang_data, "language_iso", "")
                        ),
                        progress=float(self._safe_get_attr(lang_data, "progress", 0.0)),
                        words_to_do=self._ensure_int(
                            self._safe_get_attr(lang_data, "words_to_do", 0)
                        ),
                    )
                )

        return Project(
            project_id=str(self._safe_get_attr(project_data, "project_id", "")),
            project_type=str(
                self._safe_get_attr(project_data, "project_type", "localization_files")
            ),
            name=str(self._safe_get_attr(project_data, "name", "")),
            description=str(self._safe_get_attr(project_data, "description", "")),
            created_at=str(self._safe_get_attr(project_data, "created_at", "")),
            created_at_timestamp=self._ensure_int(
                self._safe_get_attr(project_data, "created_at_timestamp", 0)
            ),
            created_by=self._ensure_int(
                self._safe_get_attr(project_data, "created_by", 0)
            ),
            created_by_email=str(
                self._safe_get_attr(project_data, "created_by_email", "")
            ),
            team_id=self._ensure_int(self._safe_get_attr(project_data, "team_id", 0)),
            base_language_id=self._ensure_int(
                self._safe_get_attr(project_data, "base_language_id", 0)
            ),
            base_language_iso=str(
                self._safe_get_attr(project_data, "base_language_iso", "")
            ),
            settings=settings,
            statistics=statistics,
            languages=languages,
        )


# Create singleton instance
lokalise_projects_service = LokaliseProjectsService()
