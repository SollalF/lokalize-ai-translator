from app.core.logging import logger
from app.schemas.lokalise import (
    Language,
    LanguageFilters,
    LanguagesListResponse,
    ProjectLanguageFilters,
    ProjectLanguagesResponse,
)

from .base import LokaliseBaseService


class LokaliseLanguagesService(LokaliseBaseService):
    """Service for Lokalise languages operations."""

    async def list_system_languages(
        self, filters: LanguageFilters | None = None
    ) -> LanguagesListResponse:
        """
        List all system languages available in Lokalise.

        Args:
            filters: Optional filters for languages

        Returns:
            LanguagesListResponse with languages list and total count

        Raises:
            HTTPException: For API errors, rate limits, or invalid tokens
        """
        try:
            # Configure API parameters
            params = {}

            if filters:
                if filters.limit is not None:
                    params["limit"] = min(filters.limit, 5000)  # Respect max limit
                if filters.page is not None:
                    params["page"] = filters.page

            # Get languages from Lokalise
            logger.info(f"Fetching system languages with params: {params}")
            languages_response = self.client.system_languages(params)
            logger.info(
                f"Retrieved {len(languages_response.items) if languages_response.items else 0} languages from Lokalise"
            )

            if not languages_response.items:
                logger.warning("No system languages found")
                return LanguagesListResponse(
                    languages=[],
                    total_count=0,
                )

            # Format the response data
            result_languages = []
            processed_count = 0

            for language_data in languages_response.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                processed_count += 1
                lang_id = self._safe_get_attr(language_data, "lang_id", 0)
                logger.debug(f"Processing language {processed_count}: {lang_id}")

                result_languages.append(self._build_language_object(language_data))

            # Get total count from response headers or metadata
            total_count = len(result_languages)
            if hasattr(languages_response, "total_count"):
                total_count = getattr(languages_response, "total_count", total_count)

            logger.info(f"Successfully processed {len(result_languages)} languages")

            return LanguagesListResponse(
                languages=result_languages, total_count=total_count
            )

        except Exception as e:
            self._handle_api_error(e, "listing system languages")
            # Return empty response structure on error (this won't be reached due to exception)
            return LanguagesListResponse(
                languages=[],
                total_count=0,
            )

    async def list_project_languages(
        self, project_id: str, filters: ProjectLanguageFilters | None = None
    ) -> ProjectLanguagesResponse:
        """
        List all languages for a specific project.

        Args:
            project_id: Lokalise project ID
            filters: Optional filters for languages

        Returns:
            ProjectLanguagesResponse with project_id and languages list

        Raises:
            HTTPException: For API errors, rate limits, or invalid tokens
        """
        try:
            # Configure API parameters
            params = {}

            if filters:
                if filters.limit is not None:
                    params["limit"] = min(filters.limit, 5000)  # Respect max limit
                if filters.page is not None:
                    params["page"] = filters.page

            # Get project languages from Lokalise
            logger.info(
                f"Fetching project languages for project {project_id} with params: {params}"
            )
            languages_response = self.client.project_languages(project_id, params)
            logger.info(
                f"Retrieved {len(languages_response.items) if languages_response.items else 0} languages from Lokalise for project {project_id}"
            )

            if not languages_response.items:
                logger.warning(f"No languages found for project {project_id}")
                return ProjectLanguagesResponse(
                    project_id=project_id,
                    languages=[],
                )

            # Format the response data
            result_languages = []
            processed_count = 0

            for language_data in languages_response.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                processed_count += 1
                lang_id = self._safe_get_attr(language_data, "lang_id", 0)
                logger.debug(
                    f"Processing language {processed_count} for project {project_id}: {lang_id}"
                )

                result_languages.append(self._build_language_object(language_data))

            logger.info(
                f"Successfully processed {len(result_languages)} languages for project {project_id}"
            )

            return ProjectLanguagesResponse(
                project_id=project_id, languages=result_languages
            )

        except Exception as e:
            self._handle_api_error(
                e, "listing project languages", f"project {project_id}"
            )
            # Return empty response structure on error (this won't be reached due to exception)
            return ProjectLanguagesResponse(
                project_id=project_id,
                languages=[],
            )

    def _build_language_object(self, language_data) -> Language:
        """Build a Language object from Lokalise API response data."""
        return Language(
            lang_id=self._ensure_int(self._safe_get_attr(language_data, "lang_id", 0)),
            lang_iso=str(self._safe_get_attr(language_data, "lang_iso", "")),
            lang_name=str(self._safe_get_attr(language_data, "lang_name", "")),
            is_rtl=bool(self._safe_get_attr(language_data, "is_rtl", False)),
            plural_forms=list(
                self._safe_get_attr(language_data, "plural_forms", []) or []
            ),
        )


# Create singleton instance
lokalise_languages_service = LokaliseLanguagesService()
