from typing import Any

from fastapi import HTTPException

from app.core.logging import logger
from app.schemas.lokalise import (
    GlossaryTerm,
    GlossaryTermMeta,
    GlossaryTermResponse,
    GlossaryTermsCreate,
    GlossaryTermsCreateMeta,
    GlossaryTermsCreateResponse,
    GlossaryTermsDelete,
    GlossaryTermsDeleteResponse,
    GlossaryTermsResponse,
    GlossaryTermsUpdate,
    GlossaryTermsUpdateMeta,
    GlossaryTermsUpdateResponse,
)
from app.schemas.lokalise.glossary import GlossaryTermTranslation

from .base import LokaliseBaseService


class LokaliseGlossaryService(LokaliseBaseService):
    """Service for Lokalise glossary operations."""

    async def get_glossary_terms(
        self,
        project_id: str,
        limit: int | None = None,
        cursor: int | None = None,
    ) -> GlossaryTermsResponse:
        """
        Fetch glossary terms for a given project with proper API response structure.

        Args:
            project_id: Lokalise project ID
            limit: Number of items to include (max 500)
            cursor: Return results starting from this cursor

        Returns:
            GlossaryTermsResponse with data and meta fields matching Lokalise API

        Raises:
            HTTPException: For API errors, rate limits, or invalid tokens
        """
        try:
            # Configure API parameters
            params = {}
            if limit is not None:
                params["limit"] = min(limit, 500)  # Respect max limit
            if cursor is not None:
                params["cursor"] = cursor

            # Get glossary terms from Lokalise
            logger.info(
                f"Fetching glossary terms for project {project_id} with params: {params}"
            )
            glossary_terms = self.client.glossary_terms(project_id, params)
            logger.info(
                f"Retrieved {len(glossary_terms.items) if glossary_terms.items else 0} glossary terms from Lokalise"
            )

            if not glossary_terms.items:
                logger.warning(f"No glossary terms found for project {project_id}")
                return GlossaryTermsResponse(
                    data=[],
                    meta=GlossaryTermMeta(
                        count=0,
                        limit=limit,
                        cursor=cursor,
                        has_more=False,
                        next_cursor=None,
                    ),
                )

            # Format the response data
            result_data = []
            processed_count = 0

            for term in glossary_terms.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                processed_count += 1
                term_id = self._safe_get_attr(term, "id", 0)
                logger.debug(f"Processing glossary term {processed_count}: {term_id}")

                result_data.append(
                    self._build_glossary_term_object(term, self._ensure_int(term_id))
                )

            # Build meta information
            meta = GlossaryTermMeta(
                count=len(result_data),
                limit=limit,
                cursor=cursor,
                has_more=False,  # This would come from the API response
                next_cursor=None,  # This would come from the API response
            )

            logger.info(
                f"Successfully processed {len(result_data)} glossary terms for project {project_id}"
            )

            return GlossaryTermsResponse(data=result_data, meta=meta)

        except Exception as e:
            self._handle_api_error(
                e, "fetching glossary terms", f"project {project_id}"
            )
            # Return empty response structure on error
            return GlossaryTermsResponse(
                data=[],
                meta=GlossaryTermMeta(
                    count=0,
                    limit=limit,
                    cursor=cursor,
                    has_more=False,
                    next_cursor=None,
                ),
            )

    async def get_glossary_term(
        self,
        project_id: str,
        term_id: int,
    ) -> GlossaryTermResponse:
        """
        Fetch a single glossary term by ID for a given project.

        Args:
            project_id: Lokalise project ID
            term_id: Unique glossary term identifier

        Returns:
            GlossaryTermResponse with data object matching Lokalise API

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or term not found
        """
        try:
            # Get glossary term from Lokalise
            logger.info(f"Fetching glossary term {term_id} for project {project_id}")
            glossary_term = self.client.glossary_term(project_id, term_id)
            logger.info(f"Retrieved glossary term {term_id} from Lokalise")

            if not glossary_term:
                logger.warning(
                    f"Glossary term {term_id} not found for project {project_id}"
                )
                raise HTTPException(
                    status_code=404, detail=f"Glossary term {term_id} not found"
                )

            result = self._build_glossary_term_object(glossary_term, term_id)
            logger.info(
                f"Successfully processed glossary term {term_id} for project {project_id}"
            )

            # Wrap in data object to match API structure
            return GlossaryTermResponse(data=result)

        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            self._handle_api_error(e, "fetching glossary term", f"term {term_id}")
            # This return will never be reached due to _handle_api_error raising HTTPException
            return GlossaryTermResponse(
                data=GlossaryTerm(id=term_id, term="", description="", project_id="")
            )

    async def _get_language_mapping(self, project_id: str) -> dict[str, int]:
        """
        Get mapping of language ISO codes to language IDs for the project.

        Args:
            project_id: Lokalise project ID

        Returns:
            Dictionary mapping language ISO codes to language IDs
        """
        try:
            # Import here to avoid circular imports
            from app.services.lokalise.languages import lokalise_languages_service

            # Get project languages using the dedicated languages service
            logger.info(f"Fetching project languages for project {project_id}")
            languages_response = (
                await lokalise_languages_service.list_project_languages(project_id)
            )

            logger.info(
                f"Retrieved {len(languages_response.languages)} languages for project {project_id}"
            )

            # Build language mapping
            language_mapping = {}
            for lang in languages_response.languages:
                logger.info(f"  Language: {lang.lang_iso} -> ID {lang.lang_id}")
                language_mapping[lang.lang_iso] = lang.lang_id

            logger.info(
                f"Language mapping for project {project_id}: {language_mapping}"
            )
            return language_mapping

        except Exception as e:
            logger.warning(
                f"Failed to get language mapping for project {project_id}: {e}"
            )
            return {}

    async def create_glossary_terms(
        self,
        project_id: str,
        create_data: GlossaryTermsCreate,
    ) -> GlossaryTermsCreateResponse:
        """
        Create one or more glossary terms in a project.

        Args:
            project_id: Lokalise project ID
            create_data: GlossaryTermsCreate schema with the terms to create

        Returns:
            GlossaryTermsCreateResponse with data array and meta information matching Lokalise API

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or validation errors
        """
        try:
            # Get language mapping for proper language IDs
            language_mapping = await self._get_language_mapping(project_id)

            # If language mapping is empty, use hardcoded mapping based on common Lokalise language IDs
            if not language_mapping:
                logger.warning("Language mapping is empty, using fallback mapping")
                language_mapping = {
                    "zh_TW": 601,
                    "zh_CN": 602,
                    "en": 640,
                    "es_419": 644,
                    "fr": 673,
                    "fr_CA": 674,
                    "ko": 733,
                    "it": 734,
                    "en_US": 1055,
                    "es": 1056,
                }
                logger.info(f"Using fallback language mapping: {language_mapping}")

            # Prepare the terms data for Lokalise SDK
            # Use the exact API format as specified in the documentation
            lokalise_terms = []

            for term in create_data.terms:
                # Build term data according to Lokalise API format
                term_data: dict[str, Any] = {
                    "term": str(term.term),
                    "description": str(
                        term.description or f"Glossary term: {term.term}"
                    ),
                    "caseSensitive": bool(term.case_sensitive or False),
                    "translatable": bool(term.translatable),
                    "forbidden": bool(term.forbidden),
                    "tags": getattr(term, "tags", [])
                    or [],  # Use tags from input or empty array
                }

                # Add translations with proper language IDs
                if term.translations:
                    translations_list = []
                    for t in term.translations:
                        # Get proper language ID from mapping, fallback to 0 if not found
                        lang_id = language_mapping.get(t.lang_iso, 0)
                        if lang_id == 0:
                            logger.warning(
                                f"Language ID not found for {t.lang_iso}, skipping translation"
                            )
                            continue

                        translation_data = {
                            "langId": lang_id,
                            "translation": t.translation,
                        }

                        # Add description if available
                        if t.description:
                            translation_data["description"] = t.description

                        translations_list.append(translation_data)

                    if translations_list:
                        term_data["translations"] = translations_list

                lokalise_terms.append(term_data)

            # Create glossary terms in Lokalise
            logger.info(
                f"Creating {len(create_data.terms)} glossary terms for project {project_id}"
            )

            # Add detailed logging for debugging
            logger.info(f"Number of terms to create: {len(lokalise_terms)}")
            logger.info(f"Type of lokalise_terms: {type(lokalise_terms)}")

            # Log first term structure for debugging
            if lokalise_terms:
                first_term = lokalise_terms[0]
                logger.info(f"First term structure: {first_term}")
                logger.info(f"First term keys: {list(first_term.keys())}")

                # Check translations structure if present
                if first_term.get("translations"):
                    logger.info(
                        f"Number of translations: {len(first_term['translations'])}"
                    )
                    logger.info(f"Translations structure: {first_term['translations']}")
                    for i, trans in enumerate(first_term["translations"]):
                        logger.info(f"Translation {i + 1}: {trans}")
                        logger.info(f"Translation {i + 1} keys: {list(trans.keys())}")
                else:
                    logger.info("No translations found in first term")

            logger.info(f"Full data being sent to Lokalise API: {lokalise_terms}")

            # Try direct list approach - SDK might expect just the list
            created_terms = self.client.create_glossary_terms(
                project_id, lokalise_terms
            )
            logger.info(
                f"Successfully created {len(created_terms.items)} glossary terms with translations in Lokalise for project {project_id}"
            )

            return self._build_create_response(created_terms)

        except HTTPException:
            raise
        except Exception as e:
            self._handle_api_error(
                e, "creating glossary terms", f"project {project_id}"
            )
            # This return will never be reached due to _handle_api_error raising HTTPException
            return GlossaryTermsCreateResponse(
                data=[],
                meta=GlossaryTermsCreateMeta(count=0, created=0, limit=None, errors={}),
            )

    def _build_create_response(self, created_terms) -> GlossaryTermsCreateResponse:
        """Build the create response from Lokalise SDK response."""
        if not created_terms or not created_terms.items:
            logger.warning("No glossary terms were created")
            return GlossaryTermsCreateResponse(
                data=[],
                meta=GlossaryTermsCreateMeta(count=0, created=0, limit=None, errors={}),
            )

        # Format the response data
        result_data = []
        for i, term in enumerate(created_terms.items):
            term_id = self._safe_get_attr(term, "id", 0)
            logger.info(f"Processing created term {i + 1} with ID {term_id}")

            # Log raw term data for debugging
            logger.debug(
                f"Raw term data from API: {term.__dict__ if hasattr(term, '__dict__') else 'No dict available'}"
            )

            # Check if translations exist in the response
            raw_translations = self._safe_get_attr(term, "translations", [])
            logger.info(
                f"Term {term_id} has {len(raw_translations) if raw_translations else 0} translations in response"
            )
            if raw_translations:
                logger.info(f"Raw translations for term {term_id}: {raw_translations}")

            result_data.append(
                self._build_glossary_term_object(term, self._ensure_int(term_id))
            )

        # Build meta information
        meta = GlossaryTermsCreateMeta(
            count=len(result_data),
            created=len(result_data),
            limit=None,
            errors={},
        )

        logger.info(f"Successfully processed {len(result_data)} created glossary terms")
        return GlossaryTermsCreateResponse(data=result_data, meta=meta)

    async def update_glossary_terms(
        self,
        project_id: str,
        update_data: GlossaryTermsUpdate,
    ) -> GlossaryTermsUpdateResponse:
        """
        Update one or more glossary terms in a project.

        Args:
            project_id: Lokalise project ID
            update_data: GlossaryTermsUpdate schema with the terms to update

        Returns:
            GlossaryTermsUpdateResponse with data array and meta information matching Lokalise API

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or validation errors
        """
        try:
            # Prepare the update data for Lokalise API
            lokalise_terms = []
            for term in update_data.terms:
                term_data: dict[str, Any] = {"term_id": term.term_id}

                # Only include fields that are not None, using correct API field names
                if term.term is not None:
                    term_data["term"] = term.term
                if term.description is not None:
                    term_data["description"] = term.description
                if term.case_sensitive is not None:
                    term_data["caseSensitive"] = term.case_sensitive
                if term.translatable is not None:
                    term_data["translatable"] = term.translatable
                if term.forbidden is not None:
                    term_data["forbidden"] = term.forbidden

                lokalise_terms.append(term_data)

            lokalise_data = {"terms": lokalise_terms}

            # Update glossary terms in Lokalise
            logger.info(
                f"Updating {len(update_data.terms)} glossary terms for project {project_id}"
            )
            updated_terms = self.client.update_glossary_terms(project_id, lokalise_data)
            logger.info(
                f"Successfully updated glossary terms in Lokalise for project {project_id}"
            )

            if not updated_terms or not updated_terms.items:
                logger.warning(
                    f"No glossary terms were updated for project {project_id}"
                )
                return GlossaryTermsUpdateResponse(
                    data=[],
                    meta=GlossaryTermsUpdateMeta(
                        count=0, updated=0, limit=None, errors={}
                    ),
                )

            # Format the response data
            result_data = []
            for term in updated_terms.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                term_id = self._safe_get_attr(term, "id", 0)  # Use 'id' field from API
                result_data.append(
                    self._build_glossary_term_object(term, self._ensure_int(term_id))
                )

            # Build meta information
            meta = GlossaryTermsUpdateMeta(
                count=len(result_data),
                updated=len(result_data),  # Number of successfully updated terms
                limit=None,  # No limit applied to updates
                errors={},  # No errors in successful case
            )

            logger.info(
                f"Successfully processed {len(result_data)} updated glossary terms for project {project_id}"
            )

            return GlossaryTermsUpdateResponse(data=result_data, meta=meta)

        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            self._handle_api_error(
                e, "updating glossary terms", f"project {project_id}"
            )
            # Return empty response structure on error
            return GlossaryTermsUpdateResponse(
                data=[],
                meta=GlossaryTermsUpdateMeta(
                    count=0,
                    updated=0,
                    limit=None,
                    errors={"general": "Failed to update glossary terms"},
                ),
            )

    async def delete_glossary_terms(
        self,
        project_id: str,
        delete_data: GlossaryTermsDelete,
    ) -> GlossaryTermsDeleteResponse:
        """
        Delete glossary terms from a project.

        Args:
            project_id: Lokalise project ID
            delete_data: GlossaryTermsDelete schema with the term IDs to delete

        Returns:
            GlossaryTermsDeleteResponse with proper API structure including deleted and failed counts

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or validation errors
        """
        try:
            # Prepare the delete data for Lokalise API
            lokalise_data = {"terms": delete_data.terms}

            # Delete glossary terms in Lokalise
            logger.info(
                f"Deleting {len(delete_data.terms)} glossary terms for project {project_id}"
            )
            # Convert list[int] to list[str | int] for API compatibility
            term_ids: list[str | int] = [str(term_id) for term_id in delete_data.terms]
            result = self.client.delete_glossary_terms(project_id, term_ids)
            logger.info(
                f"Successfully deleted glossary terms in Lokalise for project {project_id}"
            )

            # The Lokalise API should return information about deleted vs failed terms
            # For now, we'll assume all were successful unless the API provides different data
            from app.schemas.lokalise.glossary import GlossaryTermsDeleteData

            response_data = GlossaryTermsDeleteData(
                deleted={"count": len(delete_data.terms), "terms": delete_data.terms},
                failed={"count": 0, "terms": []},
            )

            return GlossaryTermsDeleteResponse(data=response_data)

        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            self._handle_api_error(
                e, "deleting glossary terms", f"project {project_id}"
            )
            # Return proper error response structure
            from app.schemas.lokalise.glossary import GlossaryTermsDeleteData

            error_data = GlossaryTermsDeleteData(
                deleted={"count": 0, "terms": []},
                failed={"count": len(delete_data.terms), "terms": delete_data.terms},
            )
            return GlossaryTermsDeleteResponse(data=error_data)

    def _build_glossary_term_object(
        self, term_data: Any, fallback_term_id: int
    ) -> GlossaryTerm:
        """Build a GlossaryTerm object from Lokalise API response data."""
        # Ensure term_id is valid - API uses 'id' field
        term_id_int = self._ensure_int(
            self._safe_get_attr(term_data, "id", fallback_term_id),
            fallback_term_id,
        )

        # Build translations array
        translations = []
        raw_translations = self._safe_get_attr(term_data, "translations", [])
        if raw_translations:
            for trans in raw_translations:
                # Try both camelCase (API) and snake_case (fallback) field names
                lang_id = self._safe_get_attr(trans, "langId") or self._safe_get_attr(
                    trans, "lang_id", 0
                )
                lang_name = self._safe_get_attr(
                    trans, "langName"
                ) or self._safe_get_attr(trans, "lang_name", "")
                lang_iso = self._safe_get_attr(trans, "langIso") or self._safe_get_attr(
                    trans, "lang_iso", ""
                )

                translations.append(
                    GlossaryTermTranslation(
                        lang_id=self._ensure_int(lang_id),
                        lang_name=str(lang_name),
                        lang_iso=str(lang_iso),
                        translation=str(self._safe_get_attr(trans, "translation", "")),
                        description=str(self._safe_get_attr(trans, "description", "")),
                    )
                )

        return GlossaryTerm(
            # Core identification (API field mapping)
            id=term_id_int,  # API uses 'id'
            term=str(self._safe_get_attr(term_data, "term", "")),
            description=str(
                self._safe_get_attr(term_data, "description", "")
            ),  # API uses 'description'
            # Boolean flags (API field mapping)
            case_sensitive=bool(
                self._safe_get_attr(term_data, "caseSensitive", False)
            ),  # API uses 'caseSensitive'
            translatable=bool(self._safe_get_attr(term_data, "translatable", True)),
            forbidden=bool(self._safe_get_attr(term_data, "forbidden", False)),
            # Translations array
            translations=translations,
            # Tags and project info (API field mapping)
            tags=self._safe_get_attr(term_data, "tags", []) or [],
            project_id=str(
                self._safe_get_attr(term_data, "projectId", "")
            ),  # API uses 'projectId'
            # Timestamps (API field mapping)
            created_at=self._safe_get_attr(
                term_data, "createdAt"
            ),  # API uses 'createdAt'
            updated_at=self._safe_get_attr(
                term_data, "updatedAt"
            ),  # API uses 'updatedAt'
        )
