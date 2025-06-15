from typing import Any

from fastapi import HTTPException

from app.core.logging import logger
from app.schemas.lokalise import CustomTranslationStatus, Translation, TranslationUpdate

from .base import LokaliseBaseService


class LokaliseTranslationsService(LokaliseBaseService):
    """Service for Lokalise translation operations."""

    async def get_translations(
        self,
        project_id: str,
        filter_lang_id: int | None = None,
        filter_is_reviewed: bool | None = None,
        filter_unverified: bool | None = None,
        filter_untranslated: bool | None = None,
        filter_qa_issues: str | None = None,
        filter_active_task_id: int | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[Translation]:
        """
        Fetch translations for a given project with filtering options.

        Args:
            project_id: Lokalise project ID
            filter_lang_id: Return translations only for presented language ID
            filter_is_reviewed: Filter translations which are reviewed
            filter_unverified: Filter translations which are unverified
            filter_untranslated: Filter by untranslated keys
            filter_qa_issues: QA issues to filter by (comma separated)
            filter_active_task_id: Filter translations which are part of given task ID
            limit: Number of items to include (max 5000)
            page: Return results starting from this page

        Returns:
            List of Translation models containing ungrouped translation items

        Raises:
            HTTPException: For API errors, rate limits, or invalid tokens
        """
        try:
            # Configure API parameters
            params = {}

            # Add filters if provided
            if filter_lang_id is not None:
                params["filter_lang_id"] = filter_lang_id
            if filter_is_reviewed is not None:
                params["filter_is_reviewed"] = 1 if filter_is_reviewed else 0
            if filter_unverified is not None:
                params["filter_unverified"] = 1 if filter_unverified else 0
            if filter_untranslated is not None:
                params["filter_untranslated"] = 1 if filter_untranslated else 0
            if filter_qa_issues:
                params["filter_qa_issues"] = filter_qa_issues
            if filter_active_task_id is not None:
                params["filter_active_task_id"] = filter_active_task_id

            # Add pagination
            if limit is not None:
                params["limit"] = min(limit, 5000)  # Respect max limit
            if page is not None:
                params["page"] = page

            # Get translations from Lokalise
            logger.info(
                f"Fetching translations for project {project_id} with params: {params}"
            )
            translations = self.client.translations(project_id, params)
            logger.info(
                f"Retrieved {len(translations.items) if translations.items else 0} translations from Lokalise"
            )

            if not translations.items:
                logger.warning(f"No translations found for project {project_id}")
                return []

            # Format the response
            result = []
            processed_count = 0

            for translation in translations.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                processed_count += 1
                translation_id = self._safe_get_attr(translation, "translation_id", 0)
                logger.debug(
                    f"Processing translation {processed_count}: {translation_id}"
                )

                result.append(
                    self._build_translation_object(
                        translation, self._ensure_int(translation_id)
                    )
                )

            logger.info(
                f"Successfully processed {len(result)} translations for project {project_id}"
            )
            return result

        except Exception as e:
            self._handle_api_error(e, "fetching translations", f"project {project_id}")
            return []

    async def get_translation(
        self,
        project_id: str,
        translation_id: int,
        disable_references: bool = False,
    ) -> Translation:
        """
        Fetch a single translation by ID for a given project.

        Args:
            project_id: Lokalise project ID
            translation_id: Unique translation identifier
            disable_references: Whether to disable key references

        Returns:
            Translation model containing the specific translation item

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or translation not found
        """
        try:
            # Configure API parameters
            params = {}
            if disable_references:
                params["disable_references"] = 1

            # Get translation from Lokalise
            logger.info(
                f"Fetching translation {translation_id} for project {project_id} with params: {params}"
            )
            translation = self.client.translation(project_id, translation_id, params)
            logger.info(f"Retrieved translation {translation_id} from Lokalise")

            if not translation:
                logger.warning(
                    f"Translation {translation_id} not found for project {project_id}"
                )
                raise HTTPException(
                    status_code=404, detail=f"Translation {translation_id} not found"
                )

            result = self._build_translation_object(translation, translation_id)
            logger.info(
                f"Successfully processed translation {translation_id} for project {project_id}"
            )
            return result

        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            self._handle_api_error(
                e, "fetching translation", f"translation {translation_id}"
            )
            # This return will never be reached due to _handle_api_error raising HTTPException
            return Translation(
                translation_id=translation_id, key_id=0, language_iso="", translation=""
            )

    async def update_translation(
        self,
        project_id: str,
        translation_id: int,
        update_data: TranslationUpdate,
    ) -> Translation:
        """
        Update a translation by ID for a given project.

        Args:
            project_id: Lokalise project ID
            translation_id: Unique translation identifier
            update_data: TranslationUpdate schema with the data to update

        Returns:
            Updated Translation model

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or translation not found
        """
        try:
            # Prepare the update data for Lokalise API
            lokalise_data: dict[str, Any] = {
                "translation": update_data.translation,
            }

            # Add optional boolean flags if provided
            if update_data.is_unverified is not None:
                lokalise_data["is_unverified"] = update_data.is_unverified
            if update_data.is_reviewed is not None:
                lokalise_data["is_reviewed"] = update_data.is_reviewed

            # Only add custom translation status IDs if they are explicitly provided and not empty
            # This avoids the "Custom translation statuses not enabled" error
            if (
                update_data.custom_translation_statuses is not None
                and len(update_data.custom_translation_statuses) > 0
            ):
                lokalise_data["custom_translation_status_ids"] = (
                    update_data.custom_translation_statuses
                )

            # Update translation in Lokalise
            logger.info(
                f"Updating translation {translation_id} for project {project_id} with data: {lokalise_data}"
            )
            updated_translation = self.client.update_translation(
                project_id, translation_id, lokalise_data
            )
            logger.info(
                f"Successfully updated translation {translation_id} in Lokalise"
            )

            if not updated_translation:
                logger.warning(
                    f"Translation {translation_id} not found for project {project_id}"
                )
                raise HTTPException(
                    status_code=404, detail=f"Translation {translation_id} not found"
                )

            result = self._build_translation_object(updated_translation, translation_id)
            logger.info(
                f"Successfully processed updated translation {translation_id} for project {project_id}"
            )
            return result

        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            self._handle_api_error(
                e, "updating translation", f"translation {translation_id}"
            )
            # This return will never be reached due to _handle_api_error raising HTTPException
            return Translation(
                translation_id=translation_id, key_id=0, language_iso="", translation=""
            )

    def _build_translation_object(
        self, translation_data: Any, fallback_translation_id: int
    ) -> Translation:
        """Build a Translation object from Lokalise API response data."""
        # Parse custom translation statuses
        custom_statuses = []
        custom_status_data = self._safe_get_attr(
            translation_data, "custom_translation_statuses", []
        )
        if custom_status_data:
            for status in custom_status_data:
                custom_statuses.append(
                    CustomTranslationStatus(
                        status_id=self._safe_get_attr(status, "status_id"),
                        title=self._safe_get_attr(status, "title"),
                        color=self._safe_get_attr(status, "color"),
                    )
                )

        # Get translation content (could be string or dict for plurals)
        translation_content = self._safe_get_attr(translation_data, "translation")

        # Ensure IDs are valid integers
        translation_id_int = self._ensure_int(
            self._safe_get_attr(
                translation_data, "translation_id", fallback_translation_id
            ),
            fallback_translation_id,
        )
        key_id_int = self._ensure_int(
            self._safe_get_attr(translation_data, "key_id", 0)
        )
        segment_number_int = self._ensure_int(
            self._safe_get_attr(translation_data, "segment_number", 1), 1
        )

        return Translation(
            # Core identification
            translation_id=translation_id_int,
            key_id=key_id_int,
            language_iso=str(self._safe_get_attr(translation_data, "language_iso", "")),
            # Content
            translation=translation_content or "",
            # Modification tracking
            modified_at=self._safe_get_attr(translation_data, "modified_at"),
            modified_at_timestamp=self._safe_get_attr(
                translation_data, "modified_at_timestamp"
            ),
            modified_by=self._safe_get_attr(translation_data, "modified_by"),
            modified_by_email=self._safe_get_attr(
                translation_data, "modified_by_email"
            ),
            # Status flags
            is_unverified=bool(
                self._safe_get_attr(translation_data, "is_unverified", False)
            ),
            is_reviewed=bool(
                self._safe_get_attr(translation_data, "is_reviewed", False)
            ),
            reviewed_by=self._safe_get_attr(translation_data, "reviewed_by"),
            # Metrics
            words=self._safe_get_attr(translation_data, "words"),
            # Advanced features
            custom_translation_statuses=custom_statuses,
            task_id=self._safe_get_attr(translation_data, "task_id"),
            segment_number=segment_number_int,
        )
