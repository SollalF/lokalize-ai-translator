"""
Lokalise glossary service for managing glossary terms.
"""

from typing import Any

from app.core.logging import logger
from app.schemas.lokalise.glossary import (
    GlossaryTerm,
    GlossaryTermFilters,
    GlossaryTermMeta,
    GlossaryTermsCreate,
    GlossaryTermsCreateMeta,
    GlossaryTermsCreateResponse,
    GlossaryTermsDelete,
    GlossaryTermsDeleteData,
    GlossaryTermsDeletedInfo,
    GlossaryTermsDeleteFailedInfo,
    GlossaryTermsDeleteResponse,
    GlossaryTermsResponse,
    GlossaryTermsUpdate,
    GlossaryTermsUpdateMeta,
    GlossaryTermsUpdateResponse,
    GlossaryTermTranslation,
)

from .base import LokaliseBaseService


class LokaliseGlossaryService(LokaliseBaseService):
    """Service for managing Lokalise glossary terms."""

    async def get_glossary_terms(
        self, project_id: str, limit: int | None = None, cursor: int | None = None
    ) -> GlossaryTermsResponse:
        """
        Fetch all glossary terms for a project.

        Args:
            project_id: ID of the project
            limit: Number of items to include
            cursor: Cursor position for pagination

        Returns:
            GlossaryTermsResponse with terms and metadata

        Raises:
            HTTPException: If the API call fails
        """
        try:
            # Use proper schema for parameters
            filters = GlossaryTermFilters(limit=limit, cursor=cursor)
            params = filters.model_dump(exclude_none=True)

            logger.info(
                f"Fetching glossary terms for project {project_id} with params: {params}"
            )

            response = self.client.glossary_terms(project_id, params)

            # Convert Lokalise response to our schema
            terms = []
            for item in response.items:
                # Create proper GlossaryTermTranslation objects
                translations = []
                for trans in getattr(item, "translations", []) or []:
                    translation = GlossaryTermTranslation(
                        lang_id=getattr(trans, "lang_id", 0),
                        lang_name=getattr(trans, "lang_name", ""),
                        lang_iso=getattr(trans, "lang_iso", ""),
                        translation=getattr(trans, "translation", ""),
                        description=getattr(trans, "description", "") or "",
                    )
                    translations.append(translation)

                term = GlossaryTerm(
                    id=getattr(item, "id", 0),
                    term=getattr(item, "term", ""),
                    description=getattr(item, "description", "") or "",
                    case_sensitive=getattr(item, "case_sensitive", False),
                    translatable=getattr(item, "translatable", True),
                    forbidden=getattr(item, "forbidden", False),
                    translations=translations,
                    tags=list(getattr(item, "tags", [])),
                    project_id=project_id,
                    created_at=getattr(item, "created_at", None),
                    updated_at=getattr(item, "updated_at", None),
                )
                terms.append(term)

            # Build metadata using proper schema
            meta = GlossaryTermMeta(
                count=getattr(response, "count", len(terms)),
                limit=limit,
                cursor=cursor,
                has_more=getattr(response, "has_more", False),
                next_cursor=getattr(response, "next_cursor", None),
            )

            logger.info(f"Retrieved {len(terms)} glossary terms from Lokalise")

            return GlossaryTermsResponse(data=terms, meta=meta)

        except Exception as e:
            self._handle_api_error(e, "get_glossary_terms", project_id)
            # This line will never be reached due to _handle_api_error raising HTTPException
            # But we need it to satisfy the type checker
            raise  # pragma: no cover

    async def get_glossary_term(self, project_id: str, term_id: int) -> GlossaryTerm:
        """
        Fetch a specific glossary term.

        Args:
            project_id: ID of the project
            term_id: ID of the term to fetch

        Returns:
            GlossaryTerm object

        Raises:
            HTTPException: If the API call fails
        """
        try:
            logger.info(f"Fetching glossary term {term_id} for project {project_id}")

            item = self.client.glossary_term(project_id, term_id)

            # Create proper GlossaryTermTranslation objects
            translations = []
            for trans in getattr(item, "translations", []) or []:
                translation = GlossaryTermTranslation(
                    lang_id=getattr(trans, "lang_id", 0),
                    lang_name=getattr(trans, "lang_name", ""),
                    lang_iso=getattr(trans, "lang_iso", ""),
                    translation=getattr(trans, "translation", ""),
                    description=getattr(trans, "description", "") or "",
                )
                translations.append(translation)

            term = GlossaryTerm(
                id=getattr(item, "id", 0),
                term=getattr(item, "term", ""),
                description=getattr(item, "description", "") or "",
                case_sensitive=getattr(item, "case_sensitive", False),
                translatable=getattr(item, "translatable", True),
                forbidden=getattr(item, "forbidden", False),
                translations=translations,
                tags=list(getattr(item, "tags", [])),
                project_id=project_id,
                created_at=getattr(item, "created_at", None),
                updated_at=getattr(item, "updated_at", None),
            )

            logger.info(f"Retrieved glossary term: {term.term}")
            return term

        except Exception as e:
            self._handle_api_error(e, "get_glossary_term", f"{project_id}/{term_id}")
            # This line will never be reached due to _handle_api_error raising HTTPException
            # But we need it to satisfy the type checker
            raise  # pragma: no cover

    async def create_glossary_terms(
        self, project_id: str, request: GlossaryTermsCreate
    ) -> GlossaryTermsCreateResponse:
        """
        Create one or more glossary terms.

        Args:
            project_id: ID of the project
            request: GlossaryTermsCreate with terms to create

        Returns:
            GlossaryTermsCreateResponse with created terms and metadata

        Raises:
            HTTPException: If the API call fails
        """
        try:
            logger.info(
                f"Creating {len(request.terms)} glossary terms for project {project_id}"
            )

            # Convert our schema to Lokalise API format
            terms_data = []
            for term in request.terms:
                term_data: dict[str, Any] = {
                    "term": term.term,
                    "description": term.description,
                    "caseSensitive": term.case_sensitive,
                    "forbidden": term.forbidden,
                    "translatable": term.translatable,
                    "tags": term.tags,
                }

                # Add translations if present
                if term.translations:
                    term_data["translations"] = [
                        {
                            "langId": trans.lang_id,
                            "translation": trans.translation,
                            "description": trans.description or "",
                        }
                        for trans in term.translations
                    ]

                terms_data.append(term_data)

            response = self.client.create_glossary_terms(project_id, terms_data)

            # Convert response to our schema
            created_terms = []
            for item in getattr(response, "items", []):
                # Create proper GlossaryTermTranslation objects
                translations = []
                for trans in getattr(item, "translations", []) or []:
                    translation = GlossaryTermTranslation(
                        lang_id=getattr(trans, "lang_id", 0),
                        lang_name=getattr(trans, "lang_name", ""),
                        lang_iso=getattr(trans, "lang_iso", ""),
                        translation=getattr(trans, "translation", ""),
                        description=getattr(trans, "description", "") or "",
                    )
                    translations.append(translation)

                term = GlossaryTerm(
                    id=getattr(item, "id", 0),
                    term=getattr(item, "term", ""),
                    description=getattr(item, "description", "") or "",
                    case_sensitive=getattr(item, "case_sensitive", False),
                    translatable=getattr(item, "translatable", True),
                    forbidden=getattr(item, "forbidden", False),
                    translations=translations,
                    tags=list(getattr(item, "tags", [])),
                    project_id=project_id,
                    created_at=getattr(item, "created_at", None),
                    updated_at=getattr(item, "updated_at", None),
                )
                created_terms.append(term)

            # Build metadata using proper schema
            meta = GlossaryTermsCreateMeta(
                count=len(created_terms),
                created=len(created_terms),
                limit=None,
                errors={},
            )

            logger.info(f"Successfully created {len(created_terms)} glossary terms")

            return GlossaryTermsCreateResponse(data=created_terms, meta=meta)

        except Exception as e:
            self._handle_api_error(e, "create_glossary_terms", project_id)
            # This line will never be reached due to _handle_api_error raising HTTPException
            # But we need it to satisfy the type checker
            raise  # pragma: no cover

    async def update_glossary_terms(
        self, project_id: str, request: GlossaryTermsUpdate
    ) -> GlossaryTermsUpdateResponse:
        """
        Update one or more glossary terms.

        Args:
            project_id: ID of the project
            request: GlossaryTermsUpdate with terms to update

        Returns:
            GlossaryTermsUpdateResponse with updated terms and metadata

        Raises:
            HTTPException: If the API call fails
        """
        try:
            logger.info(
                f"Updating {len(request.terms)} glossary terms for project {project_id}"
            )

            # Convert our schema to Lokalise API format
            terms_data = []
            for term in request.terms:
                term_data: dict[str, Any] = {"id": term.id}

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
                if term.tags is not None:
                    term_data["tags"] = term.tags

                # Add translations if present
                if term.translations:
                    term_data["translations"] = [
                        {
                            "langId": trans.lang_id,
                            "translation": trans.translation,
                            "description": trans.description or "",
                        }
                        for trans in term.translations
                    ]

                terms_data.append(term_data)

            response = self.client.update_glossary_terms(
                project_id, {"terms": terms_data}
            )

            # Convert response to our schema
            updated_terms = []
            for item in getattr(response, "items", []):
                # Create proper GlossaryTermTranslation objects
                translations = []
                for trans in getattr(item, "translations", []) or []:
                    translation = GlossaryTermTranslation(
                        lang_id=getattr(trans, "lang_id", 0),
                        lang_name=getattr(trans, "lang_name", ""),
                        lang_iso=getattr(trans, "lang_iso", ""),
                        translation=getattr(trans, "translation", ""),
                        description=getattr(trans, "description", "") or "",
                    )
                    translations.append(translation)

                term = GlossaryTerm(
                    id=getattr(item, "id", 0),
                    term=getattr(item, "term", ""),
                    description=getattr(item, "description", "") or "",
                    case_sensitive=getattr(item, "case_sensitive", False),
                    translatable=getattr(item, "translatable", True),
                    forbidden=getattr(item, "forbidden", False),
                    translations=translations,
                    tags=list(getattr(item, "tags", [])),
                    project_id=project_id,
                    created_at=getattr(item, "created_at", None),
                    updated_at=getattr(item, "updated_at", None),
                )
                updated_terms.append(term)

            # Build metadata using proper schema
            meta = GlossaryTermsUpdateMeta(
                count=len(updated_terms),
                updated=len(updated_terms),
                limit=None,
                errors={},
            )

            logger.info(f"Successfully updated {len(updated_terms)} glossary terms")

            return GlossaryTermsUpdateResponse(data=updated_terms, meta=meta)

        except Exception as e:
            self._handle_api_error(e, "update_glossary_terms", project_id)
            # This line will never be reached due to _handle_api_error raising HTTPException
            # But we need it to satisfy the type checker
            raise  # pragma: no cover

    async def delete_glossary_terms(
        self, project_id: str, request: GlossaryTermsDelete
    ) -> GlossaryTermsDeleteResponse:
        """
        Delete multiple glossary terms.

        Args:
            project_id: ID of the project
            request: GlossaryTermsDelete with term IDs to delete

        Returns:
            GlossaryTermsDeleteResponse with deletion results

        Raises:
            HTTPException: If the API call fails
        """
        try:
            logger.info(
                f"Deleting {len(request.terms)} glossary terms from project {project_id}"
            )

            # Convert to proper type for API
            term_ids: list[str | int] = list(request.terms)
            response = self.client.delete_glossary_terms(project_id, term_ids)

            # Extract deletion info from response
            deleted_info = response.get("data", {}).get("deleted", {})
            failed_info = response.get("data", {}).get("failed", {})

            logger.info(f"Successfully deleted {deleted_info.get('count', 0)} terms")
            if failed_info.get("count", 0) > 0:
                logger.warning(f"Failed to delete {failed_info.get('count', 0)} terms")

            return GlossaryTermsDeleteResponse(
                data=GlossaryTermsDeleteData(
                    deleted=GlossaryTermsDeletedInfo(
                        count=deleted_info.get("count", 0),
                        ids=deleted_info.get("ids", []),
                    ),
                    failed=GlossaryTermsDeleteFailedInfo(
                        count=failed_info.get("count", 0),
                        ids=failed_info.get("ids", []),
                        message=failed_info.get("message", ""),
                    ),
                )
            )

        except Exception as e:
            self._handle_api_error(e, "delete_glossary_terms", project_id)
            # This line will never be reached due to _handle_api_error raising HTTPException
            # But we need it to satisfy the type checker
            raise  # pragma: no cover


# Create singleton instance
lokalise_glossary_service = LokaliseGlossaryService()
