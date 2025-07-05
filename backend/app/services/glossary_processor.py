# import re
# from pathlib import Path
# from typing import Any

# import pandas as pd
# from fastapi import HTTPException

# from app.core.logging import logger
# from app.schemas.lokalise.glossary import (
#     GlossaryTermCreate,
#     GlossaryTermsCreate,
#     GlossaryTermTranslation,
# )
# from app.services.lokalise import lokalise_glossary_service


# class GlossaryProcessor:
#     """
#     Glossary processor that uses Lokalise as backend storage.

#     Handles XLSX file loading to Lokalise and text processing using Lokalise API.
#     All operations are stateless and require project_id parameter.
#     """

#     def __init__(self):
#         # Remove global state - patterns will be request-scoped
#         pass

#     async def load_glossary_from_xlsx(
#         self, file_path: str | Path, project_id: str, source_language: str = "en"
#     ) -> None:
#         """
#         Load glossary data from an XLSX file and upload to Lokalise.

#         Args:
#             file_path: Path to the XLSX file
#             project_id: Lokalise project ID
#             source_language: Source language for terms (default: "en")

#         Raises:
#             HTTPException: If file cannot be read or parsed
#         """
#         try:
#             file_path = Path(file_path)
#             if not file_path.exists():
#                 raise HTTPException(
#                     status_code=404, detail=f"Glossary file not found: {file_path}"
#                 )

#             logger.info(
#                 f"Loading glossary from {file_path} to Lokalise project {project_id}"
#             )

#             # Read the XLSX file
#             df = pd.read_excel(file_path, engine="openpyxl")

#             # Validate required columns
#             required_columns = ["term", "casesensitive", "forbidden", "translatable"]
#             missing_columns = [col for col in required_columns if col not in df.columns]
#             if missing_columns:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"Missing required columns: {missing_columns}",
#                 )

#             # Identify language columns (exclude metadata columns)
#             metadata_columns = {
#                 "term",
#                 "description",
#                 "part_of_speech",
#                 "casesensitive",
#                 "translatable",
#                 "forbidden",
#                 "tags",
#             }

#             # Find language columns (those ending with _description are descriptions)
#             language_columns = []
#             for col in df.columns:
#                 if col not in metadata_columns and not col.endswith("_description"):
#                     language_columns.append(col)

#             logger.info(f"Found languages: {sorted(language_columns)}")

#             # Get existing terms from Lokalise to avoid duplicates
#             existing_terms = {}
#             try:
#                 lokalise_response = await lokalise_glossary_service.get_glossary_terms(
#                     project_id
#                 )
#                 existing_terms = {
#                     term.term.lower(): term for term in lokalise_response.data
#                 }
#                 logger.info(f"Found {len(existing_terms)} existing terms in Lokalise")
#             except Exception as e:
#                 logger.warning(f"Could not fetch existing terms: {e}")

#             # Process each row and prepare for Lokalise
#             terms_to_create = []
#             skipped_terms = []
#             processed_count = 0

#             for _, row in df.iterrows():
#                 term_value = row["term"]
#                 # Handle pandas scalar values properly
#                 term = str(term_value).strip() if not pd.isna(term_value) else ""  # pyright: ignore[reportGeneralTypeIssues]
#                 if not term:
#                     continue

#                 # Skip if term exists in Lokalise
#                 if term.lower() in existing_terms:
#                     skipped_terms.append(term)
#                     continue

#                 # Parse flags
#                 case_sensitive = self._parse_boolean_flag(
#                     row.get("casesensitive", "no")
#                 )
#                 forbidden = self._parse_boolean_flag(row.get("forbidden", "no"))
#                 translatable = self._parse_boolean_flag(row.get("translatable", "yes"))

#                 # Get definition/description
#                 definition = self._get_safe_string_value(row, "description")

#                 # Extract translations from language columns
#                 translations = []
#                 for lang_col in language_columns:
#                     translation_text = self._get_safe_string_value(row, lang_col)
#                     if translation_text and translation_text.strip():
#                         # Get description for this language if available
#                         desc_col = f"{lang_col}_description"
#                         translation_desc = (
#                             self._get_safe_string_value(row, desc_col) or ""
#                         )

#                         # Create translation object
#                         # Map common language codes to names
#                         lang_name_map = {
#                             "en": "English",
#                             "en_US": "English (US)",
#                             "fr": "French",
#                             "fr_CA": "French (Canada)",
#                             "es": "Spanish",
#                             "es_419": "Spanish (Latin America)",
#                             "it": "Italian",
#                             "ko": "Korean",
#                             "zh_CN": "Chinese (Simplified)",
#                             "zh_TW": "Chinese (Traditional)",
#                         }

#                         translation = GlossaryTermTranslation(
#                             lang_id=1,  # Use 1 as default - Lokalise will handle mapping
#                             lang_name=lang_name_map.get(lang_col, lang_col)
#                             or lang_col,  # Ensure it's always a string
#                             lang_iso=lang_col,
#                             translation=translation_text.strip(),
#                             description=translation_desc.strip()
#                             if translation_desc
#                             else "",
#                         )
#                         translations.append(translation)
#                         logger.debug(
#                             f"Added translation for {lang_col}: {translation_text.strip()}"
#                         )

#                 # Create glossary term with translations
#                 glossary_term = GlossaryTermCreate(
#                     term=term,
#                     description=definition or f"Glossary term: {term}",
#                     case_sensitive=case_sensitive,
#                     translatable=translatable,
#                     forbidden=forbidden,
#                     translations=translations,
#                 )

#                 # Add detailed logging for debugging
#                 logger.info(f"Created term: {term}")
#                 logger.info(f"  - Description: {definition}")
#                 logger.info(f"  - Translations count: {len(translations)}")
#                 logger.info(
#                     f"  - Translation languages: {[t.lang_iso for t in translations]}"
#                 )
#                 # Log actual translation content
#                 for t in translations:
#                     logger.info(
#                         f"  - Translation {t.lang_iso}: '{t.translation}' (desc: '{t.description}')"
#                     )
#                 logger.debug(f"  - Full term object: {glossary_term}")

#                 terms_to_create.append(glossary_term)
#                 processed_count += 1

#             if not terms_to_create:
#                 logger.info(
#                     f"No new terms to upload. {len(skipped_terms)} terms already exist in Lokalise."
#                 )
#                 return

#             # Upload terms to Lokalise in batches
#             batch_size = 50  # Conservative batch size
#             uploaded_count = 0

#             for i in range(0, len(terms_to_create), batch_size):
#                 batch = terms_to_create[i : i + batch_size]

#                 try:
#                     # Create terms with translations
#                     create_request = GlossaryTermsCreate(terms=batch)
#                     created_response = (
#                         await lokalise_glossary_service.create_glossary_terms(
#                             project_id, create_request
#                         )
#                     )
#                     uploaded_count += len(created_response.data)
#                     logger.info(
#                         f"Uploaded batch of {len(created_response.data)} terms with translations to Lokalise"
#                     )

#                 except Exception as e:
#                     logger.error(f"Error uploading batch {i // batch_size + 1}: {e}")
#                     raise HTTPException(
#                         status_code=500, detail=f"Failed to upload glossary terms: {e}"
#                     ) from e

#             logger.info(
#                 f"Successfully uploaded {uploaded_count} terms with translations to Lokalise project {project_id}"
#             )
#             logger.info(f"Skipped {len(skipped_terms)} existing terms")

#         except Exception as e:
#             logger.error(f"Failed to load glossary from {file_path}: {e}")
#             if isinstance(e, HTTPException):
#                 raise
#             raise HTTPException(
#                 status_code=500, detail=f"Failed to process glossary file: {e!s}"
#             ) from e

#     async def find_terms_in_text(
#         self, text: str, project_id: str
#     ) -> list[dict[str, Any]]:
#         """
#         Find all glossary terms in the given text using Lokalise data.

#         Args:
#             text: Text to search for terms
#             project_id: Lokalise project ID

#         Returns:
#             List of dictionaries containing found terms with their positions and metadata
#         """
#         logger.info("=== FINDING TERMS IN TEXT ===")
#         logger.info(f"Text to search: '{text}'")
#         logger.info(f"Project ID: {project_id}")

#         if not text:
#             logger.info("Empty text provided, returning no terms")
#             return []

#         # Get terms from Lokalise
#         logger.info("Fetching terms data from Lokalise...")
#         terms_data = await self._get_terms_data(project_id)
#         if not terms_data:
#             logger.warning("No terms data retrieved from Lokalise")
#             return []

#         logger.info(f"Retrieved {len(terms_data)} terms from Lokalise")
#         for term, data in list(terms_data.items())[:5]:  # Log first 5 terms
#             logger.info(
#                 f"  Term: '{term}' -> case_sensitive: {data['case_sensitive']}, "
#                 f"forbidden: {data['forbidden']}, translatable: {data['translatable']}"
#             )

#         if len(terms_data) > 5:
#             logger.info(f"  ... and {len(terms_data) - 5} more terms")

#         # Request-scoped pattern cache for performance within this request
#         request_patterns: dict[str, re.Pattern[str]] = {}

#         found_terms = []

#         # Process case-sensitive terms first
#         logger.info("Processing case-sensitive terms...")
#         case_sensitive_count = 0
#         for term, term_data in terms_data.items():
#             if not term_data["case_sensitive"]:
#                 continue

#             case_sensitive_count += 1
#             logger.debug(f"Checking case-sensitive term: '{term}'")

#             pattern = self._get_word_boundary_pattern_cached(
#                 term, case_sensitive=True, cache=request_patterns
#             )
#             matches = list(pattern.finditer(text))

#             for match in matches:
#                 found_term = {
#                     "term": term,
#                     "matched_text": match.group(),
#                     "start": match.start(),
#                     "end": match.end(),
#                     "case_sensitive": True,
#                     "forbidden": term_data["forbidden"],
#                     "translatable": term_data["translatable"],
#                     "translations": term_data["translations"],
#                 }
#                 found_terms.append(found_term)
#                 logger.info(
#                     f"  Found case-sensitive match: '{match.group()}' at position {match.start()}-{match.end()}"
#                 )

#         logger.info(
#             f"Processed {case_sensitive_count} case-sensitive terms, found {len([t for t in found_terms if t['case_sensitive']])} matches"
#         )

#         # Process case-insensitive terms
#         logger.info("Processing case-insensitive terms...")
#         case_insensitive_count = 0
#         for term, term_data in terms_data.items():
#             if term_data["case_sensitive"]:
#                 continue

#             case_insensitive_count += 1
#             logger.debug(f"Checking case-insensitive term: '{term}'")

#             pattern = self._get_word_boundary_pattern_cached(
#                 term, case_sensitive=False, cache=request_patterns
#             )
#             matches = list(pattern.finditer(text))

#             for match in matches:
#                 # Check if this position is already covered by a case-sensitive match
#                 overlaps = any(
#                     found["start"] <= match.start() < found["end"]
#                     or found["start"] < match.end() <= found["end"]
#                     for found in found_terms
#                 )

#                 if not overlaps:
#                     found_term = {
#                         "term": term,
#                         "matched_text": match.group(),
#                         "start": match.start(),
#                         "end": match.end(),
#                         "case_sensitive": False,
#                         "forbidden": term_data["forbidden"],
#                         "translatable": term_data["translatable"],
#                         "translations": term_data["translations"],
#                     }
#                     found_terms.append(found_term)
#                     logger.info(
#                         f"  Found case-insensitive match: '{match.group()}' at position {match.start()}-{match.end()}"
#                     )
#                 else:
#                     logger.debug(
#                         f"  Skipped overlapping match: '{match.group()}' at position {match.start()}-{match.end()}"
#                     )

#         logger.info(f"Processed {case_insensitive_count} case-insensitive terms")

#         # Sort by position
#         found_terms.sort(key=lambda x: x["start"])

#         logger.info("=== TERM FINDING COMPLETED ===")
#         logger.info(f"Total terms found: {len(found_terms)}")
#         for i, term in enumerate(found_terms):
#             logger.info(
#                 f"  {i + 1}. '{term['matched_text']}' ({term['term']}) at {term['start']}-{term['end']} "
#                 f"[forbidden: {term['forbidden']}, translatable: {term['translatable']}]"
#             )

#         return found_terms

#     async def replace_terms_in_text(
#         self, text: str, target_lang: str, project_id: str
#     ) -> str:
#         """
#         Replace glossary terms in text with their translations for the target language.

#         Args:
#             text: Text to process
#             target_lang: Target language code for translations
#             project_id: Lokalise project ID

#         Returns:
#             Text with terms replaced by their translations
#         """
#         if not text:
#             return text

#         found_terms = await self.find_terms_in_text(text, project_id)
#         if not found_terms:
#             return text

#         # Process replacements from right to left to preserve positions
#         result_text = text
#         for term_info in reversed(found_terms):
#             # Only replace translatable terms
#             if not term_info["translatable"]:
#                 continue

#             # Get translation for target language
#             translation = term_info["translations"].get(target_lang)
#             if translation and translation != term_info["matched_text"]:
#                 start, end = term_info["start"], term_info["end"]
#                 result_text = result_text[:start] + translation + result_text[end:]
#                 logger.debug(
#                     f"Replaced '{term_info['matched_text']}' with '{translation}'"
#                 )

#         return result_text

#     async def wrap_terms_in_text(
#         self, text: str, project_id: str, wrapper_tag: str = "GLOSSARY_TERM"
#     ) -> str:
#         """
#         Wrap glossary terms in text with tags for LLM input protection.

#         Args:
#             text: Text to process
#             project_id: Lokalise project ID
#             wrapper_tag: Tag name to wrap terms with

#         Returns:
#             Text with terms wrapped in tags
#         """
#         if not text:
#             return text

#         # Use find_terms_in_text which already has request-scoped caching
#         found_terms = await self.find_terms_in_text(text, project_id)
#         if not found_terms:
#             return text

#         # Process wrapping from right to left to preserve positions
#         result_text = text
#         for term_info in reversed(found_terms):
#             # Only wrap forbidden terms or important translatable terms
#             if term_info["forbidden"] or (
#                 term_info["translatable"] and len(term_info["translations"]) > 0
#             ):
#                 start, end = term_info["start"], term_info["end"]
#                 matched_text = term_info["matched_text"]
#                 wrapped_text = f"<{wrapper_tag}>{matched_text}</{wrapper_tag}>"
#                 result_text = result_text[:start] + wrapped_text + result_text[end:]
#                 logger.debug(f"Wrapped term '{matched_text}' with {wrapper_tag} tags")

#         return result_text

#     async def get_term_info(self, term: str, project_id: str) -> dict[str, Any] | None:
#         """
#         Get information about a specific term from Lokalise.

#         Args:
#             term: Term to look up
#             project_id: Lokalise project ID

#         Returns:
#             Dictionary with term information or None if not found
#         """
#         terms_data = await self._get_terms_data(project_id)
#         if not terms_data:
#             return None

#         # Try exact match first
#         if term in terms_data:
#             return terms_data[term].copy()

#         # Try case-insensitive match
#         for glossary_term, data in terms_data.items():
#             if not data["case_sensitive"] and glossary_term.lower() == term.lower():
#                 return data.copy()

#         return None

#     async def get_available_languages(self, project_id: str) -> list[str]:
#         """
#         Get list of available languages in the glossary from Lokalise.

#         Args:
#             project_id: Lokalise project ID

#         Returns:
#             Sorted list of available language codes
#         """
#         terms_data = await self._get_terms_data(project_id)
#         if not terms_data:
#             return []

#         languages = set()
#         for term_data in terms_data.values():
#             languages.update(term_data["translations"].keys())

#         return sorted(languages)

#     async def get_stats(self, project_id: str) -> dict[str, Any]:
#         """
#         Get glossary statistics from Lokalise.

#         Args:
#             project_id: Lokalise project ID

#         Returns:
#             Dictionary with glossary statistics
#         """
#         terms_data = await self._get_terms_data(project_id)
#         if not terms_data:
#             return {
#                 "total_terms": 0,
#                 "case_sensitive_terms": 0,
#                 "case_insensitive_terms": 0,
#                 "forbidden_terms": 0,
#                 "translatable_terms": 0,
#                 "available_languages": [],
#                 "language_count": 0,
#             }

#         case_sensitive_count = sum(
#             1 for data in terms_data.values() if data["case_sensitive"]
#         )
#         case_insensitive_count = len(terms_data) - case_sensitive_count
#         forbidden_count = sum(1 for data in terms_data.values() if data["forbidden"])
#         translatable_count = sum(
#             1 for data in terms_data.values() if data["translatable"]
#         )

#         languages = set()
#         for term_data in terms_data.values():
#             languages.update(term_data["translations"].keys())

#         return {
#             "total_terms": len(terms_data),
#             "case_sensitive_terms": case_sensitive_count,
#             "case_insensitive_terms": case_insensitive_count,
#             "forbidden_terms": forbidden_count,
#             "translatable_terms": translatable_count,
#             "available_languages": sorted(languages),
#             "language_count": len(languages),
#         }

#     async def _get_terms_data(self, project_id: str) -> dict[str, dict[str, Any]]:
#         """
#         Get terms data from Lokalise.

#         Args:
#             project_id: Lokalise project ID

#         Returns:
#             Dictionary mapping term names to term data
#         """
#         logger.info("=== FETCHING TERMS DATA FROM LOKALISE ===")
#         logger.info(f"Project ID: {project_id}")

#         try:
#             # Fetch from Lokalise
#             logger.info("Calling Lokalise glossary service...")
#             lokalise_response = await lokalise_glossary_service.get_glossary_terms(
#                 project_id
#             )

#             logger.info("Lokalise response received:")
#             logger.info(f"  Number of terms: {len(lokalise_response.data)}")
#             logger.info(f"  Response meta: {lokalise_response.meta}")

#             terms_data = {}
#             processed_count = 0

#             for term in lokalise_response.data:
#                 if not term.term:
#                     logger.warning(f"Skipping term with empty name: {term}")
#                     continue

#                 processed_count += 1
#                 logger.debug(f"Processing term {processed_count}: '{term.term}'")

#                 # Create term data structure using the updated schema fields
#                 translations_dict: dict[str, str] = {}

#                 # Add translations from the term's translations field
#                 if term.translations:
#                     logger.debug(
#                         f"  Found {len(term.translations)} translations for '{term.term}'"
#                     )
#                     for translation in term.translations:
#                         translations_dict[translation.lang_iso] = (
#                             translation.translation
#                         )
#                         logger.debug(
#                             f"    {translation.lang_iso}: '{translation.translation}'"
#                         )
#                 else:
#                     logger.debug(f"  No translations found for '{term.term}'")

#                 # Add the base term as a translation (usually the primary language)
#                 if term.project_id:  # Use project_id as indicator of valid term
#                     # For now, we'll assume the term itself is in English (this could be configurable)
#                     if "en" not in translations_dict:
#                         translations_dict["en"] = term.term
#                         logger.debug(f"    Added base translation en: '{term.term}'")

#                 term_data = {
#                     "translations": translations_dict,
#                     "case_sensitive": term.case_sensitive or False,
#                     "forbidden": term.forbidden or False,
#                     "translatable": term.translatable
#                     if term.translatable is not None
#                     else True,
#                     "description": term.description or "",
#                     "part_of_speech": None,  # Not available in new schema
#                     "tags": list(term.tags) if term.tags else [],
#                 }

#                 terms_data[term.term] = term_data
#                 logger.debug(f"  Processed '{term.term}': {term_data}")

#             logger.info("=== TERMS DATA PROCESSING COMPLETED ===")
#             logger.info(
#                 f"Processed {processed_count} terms from Lokalise project {project_id}"
#             )
#             logger.info(f"Final terms data contains {len(terms_data)} entries")

#             # Log summary of term types
#             case_sensitive_count = sum(
#                 1 for data in terms_data.values() if data["case_sensitive"]
#             )
#             forbidden_count = sum(
#                 1 for data in terms_data.values() if data["forbidden"]
#             )
#             translatable_count = sum(
#                 1 for data in terms_data.values() if data["translatable"]
#             )

#             logger.info("Term type summary:")
#             logger.info(f"  Case sensitive: {case_sensitive_count}")
#             logger.info(f"  Forbidden: {forbidden_count}")
#             logger.info(f"  Translatable: {translatable_count}")

#             return terms_data

#         except Exception as e:
#             logger.error("=== FAILED TO FETCH TERMS FROM LOKALISE ===")
#             logger.error(f"Error type: {type(e).__name__}")
#             logger.error(f"Error message: {e!s}")
#             logger.error(f"Project ID: {project_id}")
#             logger.error("Full error details:", exc_info=True)
#             return {}

#     def _parse_boolean_flag(self, value: Any) -> bool:
#         """Parse boolean flags from various string representations."""
#         if pd.isna(value):
#             return False

#         str_value = str(value).lower().strip()
#         return str_value in {"yes", "true", "1", "y", "on"}

#     def _get_safe_string_value(self, row: pd.Series, column: str) -> str | None:
#         """Safely extract string value from pandas row, handling NaN values."""
#         value = row.get(column)
#         if pd.isna(value):  # pyright: ignore[reportGeneralTypeIssues]
#             return None
#         str_value = str(value).strip()
#         return str_value if str_value else None

#     def _get_word_boundary_pattern(
#         self, term: str, case_sensitive: bool = True
#     ) -> re.Pattern[str]:
#         """
#         Get or create a compiled regex pattern for word boundary matching.

#         Args:
#             term: Term to create pattern for
#             case_sensitive: Whether matching should be case sensitive

#         Returns:
#             Compiled regex pattern
#         """
#         # Escape special regex characters
#         escaped_term = re.escape(term)

#         # Create word boundary pattern
#         pattern = rf"\b{escaped_term}\b"

#         flags = 0 if case_sensitive else re.IGNORECASE
#         return re.compile(pattern, flags)

#     def _get_word_boundary_pattern_cached(
#         self,
#         term: str,
#         case_sensitive: bool = True,
#         cache: dict[str, re.Pattern[str]] | None = None,
#     ) -> re.Pattern[str]:
#         """
#         Get or create a compiled regex pattern for word boundary matching.

#         Args:
#             term: Term to create pattern for
#             case_sensitive: Whether matching should be case sensitive
#             cache: Request-scoped pattern cache

#         Returns:
#             Compiled regex pattern
#         """
#         if cache is None:
#             cache = {}

#         cache_key = f"{term}:{case_sensitive}"

#         if cache_key not in cache:
#             # Escape special regex characters
#             escaped_term = re.escape(term)

#             # Create word boundary pattern
#             pattern = rf"\b{escaped_term}\b"

#             flags = 0 if case_sensitive else re.IGNORECASE
#             cache[cache_key] = re.compile(pattern, flags)

#         return cache[cache_key]


# # Create singleton instance
# glossary_processor = GlossaryProcessor()
