from typing import Any

from app.core.logging import logger
from app.schemas.lokalise import (
    KeysCreate,
    KeysCreateResponse,
    PlatformKeyNames,
    TranslationKey,
    TranslationMetadata,
)
from app.schemas.lokalise.keys import KeyCreateMeta

from .base import LokaliseBaseService


class LokaliseKeysService(LokaliseBaseService):
    """Service for Lokalise key operations."""

    async def get_keys(
        self,
        project_id: str,
        target_language: str | None = None,
        untranslated_only: bool = False,
    ) -> list[TranslationKey]:
        """
        Fetch keys for a given project, optionally filtered by target language and translation status.

        Args:
            project_id: Lokalise project ID
            target_language: Target language code (e.g., 'en', 'fr') - Optional
            untranslated_only: If True, returns only untranslated keys. If False, returns all keys.

        Returns:
            List of TranslationKey models containing comprehensive key details and translation status

        Raises:
            HTTPException: For API errors, rate limits, or invalid tokens
        """
        try:
            # Configure API parameters to get comprehensive data
            params = {
                "include_translations": 1,
                "include_comments": 1,
                "include_screenshots": 1,
            }

            # Get keys from Lokalise
            logger.info(f"Fetching keys for project {project_id} with params: {params}")
            keys = self.client.keys(project_id, params)
            logger.info(
                f"Retrieved {len(keys.items) if keys.items else 0} keys from Lokalise"
            )

            if not keys.items:
                logger.warning(f"No keys found for project {project_id}")
                return []

            # Format the response
            result = []
            processed_count = 0

            for key in keys.items:  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                processed_count += 1
                key_id = self._safe_get_attr(key, "key_id", 0)
                logger.debug(f"Processing key {processed_count}: {key_id}")

                # If target_language is specified, find translation for that language
                if target_language:
                    translated_text = None
                    is_translated = False
                    translation_metadata = None

                    key_translations = self._safe_get_attr(key, "translations", [])
                    if key_translations:
                        for translation in key_translations:
                            translation_lang = self._safe_get_attr(
                                translation, "language_iso"
                            )
                            if translation_lang == target_language:
                                translated_text = self._safe_get_attr(
                                    translation, "translation"
                                )
                                is_translated = bool(
                                    translated_text and str(translated_text).strip()
                                )

                                # Extract translation metadata with proper defaults
                                translation_metadata = TranslationMetadata(
                                    translation_id=self._safe_get_attr(
                                        translation, "translation_id"
                                    ),
                                    modified_by=self._safe_get_attr(
                                        translation, "modified_by"
                                    ),
                                    modified_by_email=self._safe_get_attr(
                                        translation, "modified_by_email"
                                    ),
                                    modified_at=self._safe_get_attr(
                                        translation, "modified_at"
                                    ),
                                    modified_at_timestamp=self._safe_get_attr(
                                        translation, "modified_at_timestamp"
                                    ),
                                    is_reviewed=bool(
                                        self._safe_get_attr(
                                            translation, "is_reviewed", False
                                        )
                                    ),
                                    is_unverified=bool(
                                        self._safe_get_attr(
                                            translation, "is_unverified", False
                                        )
                                    ),
                                    reviewed_by=self._safe_get_attr(
                                        translation, "reviewed_by"
                                    ),
                                    words=self._safe_get_attr(translation, "words"),
                                )
                                break

                    # Filter for untranslated only if requested
                    if untranslated_only and is_translated:
                        continue

                    language_code = target_language
                else:
                    # If no target language specified, include key without translation-specific data
                    translated_text = None
                    is_translated = False
                    translation_metadata = None
                    language_code = ""

                # Get source text (usually the first translation or key name)
                source_text = ""
                key_translations = self._safe_get_attr(key, "translations", [])
                if key_translations:
                    first_translation = key_translations[0]
                    source_text = str(
                        self._safe_get_attr(first_translation, "translation", "")
                    )

                # Handle key_name (can be string or object with platform-specific names)
                key_name_value = self._safe_get_attr(key, "key_name")
                if isinstance(key_name_value, dict):
                    key_name = PlatformKeyNames(
                        ios=key_name_value.get("ios"),
                        android=key_name_value.get("android"),
                        web=key_name_value.get("web"),
                        other=key_name_value.get("other"),
                    )
                else:
                    # If it's a string, use it directly
                    key_name = str(key_name_value) if key_name_value else ""

                # Ensure key_id is valid
                key_id_int = self._ensure_int(key_id)

                result.append(
                    TranslationKey(
                        # Basic identification
                        key_id=key_id_int,
                        key_name=key_name,
                        # Content
                        source_text=source_text,
                        translated_text=translated_text,
                        # Translation status
                        is_translated=is_translated,
                        language_code=language_code,
                        # Key metadata with safe defaults
                        created_at=self._safe_get_attr(key, "created_at"),
                        created_at_timestamp=self._safe_get_attr(
                            key, "created_at_timestamp"
                        ),
                        description=self._safe_get_attr(key, "description"),
                        platforms=list(self._safe_get_attr(key, "platforms") or []),
                        tags=list(self._safe_get_attr(key, "tags") or []),
                        # Key properties with safe defaults
                        is_plural=bool(self._safe_get_attr(key, "is_plural", False)),
                        plural_name=self._safe_get_attr(key, "plural_name"),
                        is_hidden=bool(self._safe_get_attr(key, "is_hidden", False)),
                        is_archived=bool(
                            self._safe_get_attr(key, "is_archived", False)
                        ),
                        context=self._safe_get_attr(key, "context"),
                        base_words=self._safe_get_attr(key, "base_words"),
                        char_limit=self._safe_get_attr(key, "char_limit"),
                        # Translation metadata
                        translation_metadata=translation_metadata,
                        # Timestamps
                        modified_at=self._safe_get_attr(key, "modified_at"),
                        modified_at_timestamp=self._safe_get_attr(
                            key, "modified_at_timestamp"
                        ),
                        translations_modified_at=self._safe_get_attr(
                            key, "translations_modified_at"
                        ),
                        translations_modified_at_timestamp=self._safe_get_attr(
                            key, "translations_modified_at_timestamp"
                        ),
                    )
                )

            logger.info(
                f"Successfully processed {len(result)} keys for project {project_id}"
            )
            return result

        except Exception as e:
            self._handle_api_error(e, "fetching keys", f"project {project_id}")
            return []  # This line will never be reached due to _handle_api_error raising HTTPException

    async def create_keys(
        self,
        project_id: str,
        create_data: KeysCreate,
    ) -> KeysCreateResponse:
        """
        Create one or more keys in a project.

        Args:
            project_id: Lokalise project ID
            create_data: KeysCreate schema with the keys to create

        Returns:
            KeysCreateResponse with data array and meta information including creation statistics

        Raises:
            HTTPException: For API errors, rate limits, invalid tokens, or validation errors
        """
        try:
            # Prepare the keys data for Lokalise SDK
            lokalise_keys = []

            for key in create_data.keys:
                # Build key data according to Lokalise API format
                key_data: dict[str, Any] = {
                    "key_name": key.key_name,
                    "platforms": key.platforms,
                }

                # Add optional fields if provided
                if key.description is not None:
                    key_data["description"] = key.description
                if key.filenames is not None:
                    filenames_dict = {}
                    if key.filenames.ios:
                        filenames_dict["ios"] = key.filenames.ios
                    if key.filenames.android:
                        filenames_dict["android"] = key.filenames.android
                    if key.filenames.web:
                        filenames_dict["web"] = key.filenames.web
                    if key.filenames.other:
                        filenames_dict["other"] = key.filenames.other
                    if filenames_dict:
                        key_data["filenames"] = filenames_dict

                if key.tags:
                    key_data["tags"] = key.tags
                if key.comments:
                    key_data["comments"] = [
                        {"comment": c.comment} for c in key.comments
                    ]
                if key.screenshots:
                    screenshots_data = []
                    for screenshot in key.screenshots:
                        screenshot_dict: dict[str, Any] = {"data": screenshot.data}
                        if screenshot.title:
                            screenshot_dict["title"] = screenshot.title
                        if screenshot.description:
                            screenshot_dict["description"] = screenshot.description
                        if screenshot.screenshot_tags:
                            screenshot_dict["screenshot_tags"] = (
                                screenshot.screenshot_tags
                            )
                        screenshots_data.append(screenshot_dict)
                    key_data["screenshots"] = screenshots_data

                if key.translations:
                    translations_data = []
                    for translation in key.translations:
                        trans_dict: dict[str, Any] = {
                            "language_iso": translation.language_iso,
                            "translation": translation.translation,
                        }
                        if translation.is_reviewed:
                            trans_dict["is_reviewed"] = translation.is_reviewed
                        if translation.is_unverified:
                            trans_dict["is_unverified"] = translation.is_unverified
                        if translation.custom_translation_status_ids:
                            trans_dict["custom_translation_status_ids"] = (
                                translation.custom_translation_status_ids
                            )
                        translations_data.append(trans_dict)
                    key_data["translations"] = translations_data

                # Add boolean flags
                if key.is_plural:
                    key_data["is_plural"] = key.is_plural
                if key.plural_name:
                    key_data["plural_name"] = key.plural_name
                if key.is_hidden:
                    key_data["is_hidden"] = key.is_hidden
                if key.is_archived:
                    key_data["is_archived"] = key.is_archived
                if key.context:
                    key_data["context"] = key.context
                if key.char_limit is not None:
                    key_data["char_limit"] = key.char_limit
                if key.custom_attributes:
                    key_data["custom_attributes"] = key.custom_attributes

                # Handle use_automations at the key level if needed
                if create_data.use_automations:
                    key_data["use_automations"] = create_data.use_automations

                lokalise_keys.append(key_data)

            # Create keys in Lokalise using the correct Python SDK method signature
            # The Python SDK expects: create_keys(project_id, keys_array)
            logger.info(
                f"Creating {len(create_data.keys)} keys for project {project_id}"
            )
            logger.debug(f"Keys payload: {lokalise_keys}")

            created_keys = self.client.create_keys(project_id, lokalise_keys)
            logger.info(
                f"Successfully created {len(created_keys.items) if created_keys.items else 0} keys in Lokalise for project {project_id}"
            )

            return self._build_create_keys_response(created_keys)

        except Exception as e:
            self._handle_api_error(e, "creating keys", f"project {project_id}")
            # This return will never be reached due to _handle_api_error raising HTTPException
            return KeysCreateResponse(
                data=[],
                meta=KeyCreateMeta(count=0, created=0, limit=None, errors={}),
            )

    def _build_create_keys_response(self, created_keys) -> KeysCreateResponse:
        """Build the create keys response from Lokalise SDK response."""
        if not created_keys or not created_keys.items:
            logger.warning("No keys were created")
            return KeysCreateResponse(
                data=[],
                meta=KeyCreateMeta(count=0, created=0, limit=None, errors={}),
            )

        # Format the response data
        result_data = []
        for i, key in enumerate(created_keys.items):
            key_id = self._safe_get_attr(key, "key_id", 0)
            logger.info(f"Processing created key {i + 1} with ID {key_id}")

            # Build a TranslationKey object from the created key
            # Handle key_name (can be string or object with platform-specific names)
            key_name_value = self._safe_get_attr(key, "key_name")
            if isinstance(key_name_value, dict):
                key_name = PlatformKeyNames(
                    ios=key_name_value.get("ios"),
                    android=key_name_value.get("android"),
                    web=key_name_value.get("web"),
                    other=key_name_value.get("other"),
                )
            else:
                key_name = str(key_name_value) if key_name_value else ""

            # Get source text from first translation if available
            source_text = ""
            key_translations = self._safe_get_attr(key, "translations", [])
            if key_translations:
                first_translation = key_translations[0]
                source_text = str(
                    self._safe_get_attr(first_translation, "translation", "")
                )

            result_data.append(
                TranslationKey(
                    # Basic identification
                    key_id=self._ensure_int(key_id),
                    key_name=key_name,
                    # Content
                    source_text=source_text,
                    translated_text=None,
                    # Translation status (new keys are typically untranslated)
                    is_translated=False,
                    language_code="",
                    # Key metadata
                    created_at=self._safe_get_attr(key, "created_at"),
                    created_at_timestamp=self._safe_get_attr(
                        key, "created_at_timestamp"
                    ),
                    description=self._safe_get_attr(key, "description"),
                    platforms=list(self._safe_get_attr(key, "platforms") or []),
                    tags=list(self._safe_get_attr(key, "tags") or []),
                    # Key properties
                    is_plural=bool(self._safe_get_attr(key, "is_plural", False)),
                    plural_name=self._safe_get_attr(key, "plural_name"),
                    is_hidden=bool(self._safe_get_attr(key, "is_hidden", False)),
                    is_archived=bool(self._safe_get_attr(key, "is_archived", False)),
                    context=self._safe_get_attr(key, "context"),
                    base_words=self._safe_get_attr(key, "base_words"),
                    char_limit=self._safe_get_attr(key, "char_limit"),
                    # Translation metadata (initially None for new keys)
                    translation_metadata=None,
                    # Timestamps
                    modified_at=self._safe_get_attr(key, "modified_at"),
                    modified_at_timestamp=self._safe_get_attr(
                        key, "modified_at_timestamp"
                    ),
                    translations_modified_at=self._safe_get_attr(
                        key, "translations_modified_at"
                    ),
                    translations_modified_at_timestamp=self._safe_get_attr(
                        key, "translations_modified_at_timestamp"
                    ),
                )
            )

        # Build meta information
        meta = KeyCreateMeta(
            count=len(result_data),
            created=len(result_data),
            limit=None,
            errors={},
        )

        logger.info(f"Successfully processed {len(result_data)} created keys")
        return KeysCreateResponse(data=result_data, meta=meta)
