# import re
# from typing import Any

# from app.core.logging import logger
# from app.services.gemini_service import gemini_service
# from app.services.glossary_processor import glossary_processor


# class GlossaryAwareTranslationService:
#     """
#     Service for AI translation with glossary awareness.

#     This service wraps glossary terms before translation and verifies them after,
#     ensuring consistent terminology across translations.
#     """

#     def __init__(self):
#         self.translation_provider = gemini_service
#         self.glossary_processor = glossary_processor

#     async def translate_with_glossary(
#         self,
#         source_text: str,
#         source_lang: str,
#         target_lang: str,
#         project_id: str | None = None,
#         preserve_forbidden_terms: bool = True,
#         translate_allowed_terms: bool = True,
#     ) -> dict[str, Any]:
#         """
#         Translate text with glossary term protection and verification.

#         Args:
#             source_text: Text to translate
#             source_lang: Source language code
#             target_lang: Target language code
#             project_id: Lokalise project ID (optional)
#             preserve_forbidden_terms: Whether to preserve forbidden terms
#             translate_allowed_terms: Whether to translate allowed terms

#         Returns:
#             Dictionary containing translation results and verification data
#         """
#         logger.info(
#             f"=== GLOSSARY-AWARE TRANSLATION START ===\n"
#             f"Source text: '{source_text}'\n"
#             f"Source language: {source_lang}\n"
#             f"Target language: {target_lang}\n"
#             f"Project ID: {project_id}\n"
#             f"Preserve forbidden terms: {preserve_forbidden_terms}\n"
#             f"Translate allowed terms: {translate_allowed_terms}"
#         )

#         # If no project_id provided, proceed with regular translation
#         if not project_id:
#             logger.info("No project_id provided, performing regular translation")
#             translated_text = await self.translation_provider.translate_text(
#                 source_text=source_text,
#                 source_lang=source_lang,
#                 target_lang=target_lang,
#             )
#             logger.info(f"Regular translation completed: '{translated_text}'")

#             return {
#                 "translated_text": translated_text,
#                 "source_text": source_text,
#                 "source_lang": source_lang,
#                 "target_lang": target_lang,
#                 "glossary_terms_found": [],
#                 "wrapped_text": source_text,
#                 "verification_results": {
#                     "success": True,
#                     "missing_terms": [],
#                     "warnings": [],
#                     "suggestions": [],
#                     "found_wrapped_terms": {},
#                     "cleaned_text": translated_text,
#                 },
#             }

#         # Step 1: Find glossary terms in source text
#         logger.info("=== STEP 1: Finding glossary terms ===")
#         try:
#             found_terms = await self.glossary_processor.find_terms_in_text(
#                 source_text, project_id
#             )
#             logger.info(f"Found {len(found_terms)} glossary terms in source text")
#             for i, term in enumerate(found_terms):
#                 logger.info(
#                     f"  Term {i + 1}: '{term['term']}' -> '{term['matched_text']}' "
#                     f"(forbidden: {term['forbidden']}, translatable: {term['translatable']}, "
#                     f"position: {term['start']}-{term['end']})"
#                 )
#         except Exception as e:
#             logger.error(f"Error finding glossary terms: {e}", exc_info=True)
#             raise

#         # Step 2: Wrap terms for protection during translation
#         logger.info("=== STEP 2: Wrapping terms for translation ===")
#         try:
#             wrapped_text = await self._wrap_terms_for_translation(
#                 source_text,
#                 found_terms,
#                 preserve_forbidden_terms,
#                 translate_allowed_terms,
#             )
#             logger.info(f"Original text: '{source_text}'")
#             logger.info(f"Wrapped text: '{wrapped_text}'")
#             logger.info(f"Text changed: {source_text != wrapped_text}")
#         except Exception as e:
#             logger.error(f"Error wrapping terms: {e}", exc_info=True)
#             raise

#         # Step 3: Create system prompt for AI translation
#         logger.info("=== STEP 3: Creating system prompt ===")
#         try:
#             system_prompt = self._create_glossary_system_prompt(
#                 found_terms,
#                 target_lang,
#                 preserve_forbidden_terms,
#                 translate_allowed_terms,
#             )
#             logger.info(f"System prompt created (length: {len(system_prompt)})")
#             if system_prompt:
#                 logger.info(f"System prompt preview: {system_prompt[:200]}...")
#             else:
#                 logger.info("No system prompt created (no terms found)")
#         except Exception as e:
#             logger.error(f"Error creating system prompt: {e}", exc_info=True)
#             raise

#         # Step 4: Perform translation with system prompt
#         logger.info("=== STEP 4: Performing AI translation ===")
#         try:
#             logger.info("Calling translation provider with:")
#             logger.info(f"  Source text: '{wrapped_text}'")
#             logger.info(f"  Source lang: {source_lang}")
#             logger.info(f"  Target lang: {target_lang}")
#             logger.info(
#                 f"  System prompt length: {len(system_prompt) if system_prompt else 0}"
#             )

#             translated_text = await self.translation_provider.translate_text(
#                 source_text=wrapped_text,
#                 source_lang=source_lang,
#                 target_lang=target_lang,
#                 system_prompt=system_prompt,
#             )
#             logger.info(f"AI translation completed: '{translated_text}'")
#         except Exception as e:
#             logger.error(f"Error during AI translation: {e}", exc_info=True)
#             raise

#         # Step 5: Verify and clean up the translation
#         logger.info("=== STEP 5: Verifying translation ===")
#         try:
#             verification_results = await self._verify_translation(
#                 translated_text, found_terms, target_lang
#             )
#             logger.info("Verification completed:")
#             logger.info(f"  Success: {verification_results['success']}")
#             logger.info(
#                 f"  Missing terms: {len(verification_results['missing_terms'])}"
#             )
#             logger.info(f"  Warnings: {len(verification_results['warnings'])}")
#             logger.info(f"  Suggestions: {len(verification_results['suggestions'])}")
#             logger.info(
#                 f"  Found wrapped terms: {len(verification_results['found_wrapped_terms'])}"
#             )
#             logger.info(f"  Cleaned text: '{verification_results['cleaned_text']}'")
#         except Exception as e:
#             logger.error(f"Error during translation verification: {e}", exc_info=True)
#             raise

#         final_result = {
#             "translated_text": verification_results["cleaned_text"],
#             "source_text": source_text,
#             "source_lang": source_lang,
#             "target_lang": target_lang,
#             "glossary_terms_found": found_terms,
#             "wrapped_text": wrapped_text,
#             "verification_results": verification_results,
#         }

#         logger.info("=== GLOSSARY-AWARE TRANSLATION COMPLETED ===")
#         logger.info(f"Final translated text: '{final_result['translated_text']}'")

#         return final_result

#     async def _wrap_terms_for_translation(
#         self,
#         text: str,
#         found_terms: list[dict[str, Any]],
#         preserve_forbidden_terms: bool,
#         translate_allowed_terms: bool,
#     ) -> str:
#         """
#         Wrap terms in the text with special markers for AI protection.

#         Args:
#             text: Source text
#             found_terms: List of found glossary terms
#             preserve_forbidden_terms: Whether to wrap forbidden terms
#             translate_allowed_terms: Whether to wrap translatable terms

#         Returns:
#             Text with terms wrapped in protective markers
#         """
#         logger.info("=== WRAPPING TERMS FOR TRANSLATION ===")
#         logger.info(f"Input text: '{text}'")
#         logger.info(f"Found terms count: {len(found_terms)}")
#         logger.info(f"Preserve forbidden terms: {preserve_forbidden_terms}")
#         logger.info(f"Translate allowed terms: {translate_allowed_terms}")

#         if not found_terms:
#             logger.info("No terms found, returning original text")
#             return text

#         # Sort terms by position (reverse order to maintain positions during replacement)
#         sorted_terms = sorted(found_terms, key=lambda x: x["start"], reverse=True)
#         terms_summary = [f"{t['term']}@{t['start']}-{t['end']}" for t in sorted_terms]
#         logger.info(f"Terms sorted by position (reverse): {terms_summary}")

#         wrapped_text = text
#         wrapped_count = 0
#         skipped_count = 0

#         for term_info in sorted_terms:
#             should_wrap = False

#             # Determine if we should wrap this term
#             if term_info["forbidden"] and preserve_forbidden_terms:
#                 should_wrap = True
#                 reason = "forbidden term + preserve_forbidden_terms=True"
#             elif term_info["translatable"] and translate_allowed_terms:
#                 should_wrap = True
#                 reason = "translatable term + translate_allowed_terms=True"
#             else:
#                 reason = f"forbidden={term_info['forbidden']}, translatable={term_info['translatable']}, preserve_forbidden={preserve_forbidden_terms}, translate_allowed={translate_allowed_terms}"

#             logger.info(
#                 f"Term '{term_info['term']}' -> should_wrap={should_wrap} ({reason})"
#             )

#             if should_wrap:
#                 start, end = term_info["start"], term_info["end"]
#                 matched_text = term_info["matched_text"]

#                 # Create unique wrapper with term info
#                 term_id = f"{term_info['term']}_{start}_{end}"
#                 wrapped_term = (
#                     f'<GLOSSARY_TERM id="{term_id}">{matched_text}</GLOSSARY_TERM>'
#                 )

#                 old_text = wrapped_text
#                 wrapped_text = wrapped_text[:start] + wrapped_term + wrapped_text[end:]
#                 wrapped_count += 1

#                 logger.info(f"  Wrapped '{matched_text}' with ID '{term_id}'")
#                 logger.info(
#                     f"  Text change: '{old_text[max(0, start - 10) : end + 10]}' -> '{wrapped_text[max(0, start - 10) : start + len(wrapped_term) + 10]}'"
#                 )
#             else:
#                 skipped_count += 1
#                 logger.info(f"  Skipped wrapping '{term_info['term']}'")

#         logger.info("=== WRAPPING COMPLETED ===")
#         logger.info(f"Terms wrapped: {wrapped_count}")
#         logger.info(f"Terms skipped: {skipped_count}")
#         logger.info(f"Final wrapped text: '{wrapped_text}'")

#         return wrapped_text

#     def _create_glossary_system_prompt(
#         self,
#         found_terms: list[dict[str, Any]],
#         target_lang: str,
#         preserve_forbidden_terms: bool,
#         translate_allowed_terms: bool,
#     ) -> str:
#         """
#         Create a system prompt for the AI translator with glossary instructions.

#         Args:
#             found_terms: List of found glossary terms
#             target_lang: Target language code
#             preserve_forbidden_terms: Whether to preserve forbidden terms
#             translate_allowed_terms: Whether to translate allowed terms

#         Returns:
#             System prompt string for the AI translator
#         """
#         if not found_terms:
#             return ""

#         # Categorize terms
#         forbidden_terms = [t for t in found_terms if t["forbidden"]]
#         translatable_terms = [t for t in found_terms if t["translatable"]]

#         prompt_parts = [
#             "GLOSSARY TRANSLATION INSTRUCTIONS:",
#             "",
#             "The text contains special glossary terms marked with <GLOSSARY_TERM> tags.",
#             "Follow these rules strictly:",
#             "",
#         ]

#         if forbidden_terms and preserve_forbidden_terms:
#             prompt_parts.extend(
#                 [
#                     "FORBIDDEN TERMS (DO NOT TRANSLATE):",
#                     "These terms must remain exactly as they appear in the original language:",
#                 ]
#             )
#             for term in forbidden_terms:
#                 prompt_parts.append(f"- {term['term']}")
#             prompt_parts.append("")

#         if translatable_terms and translate_allowed_terms:
#             prompt_parts.extend(
#                 [
#                     "TRANSLATABLE TERMS:",
#                     f"These terms should be translated to {target_lang} using the provided translations:",
#                 ]
#             )
#             for term in translatable_terms:
#                 # Debug logging to see what translations are available
#                 logger.info(
#                     f"DEBUG: Term '{term['term']}' has translations: {term['translations']}"
#                 )
#                 target_translation = term["translations"].get(target_lang)
#                 logger.info(
#                     f"DEBUG: Looking for '{target_lang}' translation, found: '{target_translation}'"
#                 )

#                 if target_translation:
#                     prompt_parts.append(f"- {term['term']} → {target_translation}")
#                     logger.info(
#                         f"DEBUG: Added translation instruction: {term['term']} → {target_translation}"
#                     )
#                 else:
#                     prompt_parts.append(f"- {term['term']} (translate appropriately)")
#                     logger.info(
#                         f"DEBUG: No translation found for {term['term']} in {target_lang}, using fallback"
#                     )
#             prompt_parts.append("")

#         prompt_parts.extend(
#             [
#                 "IMPORTANT:",
#                 "1. Keep the <GLOSSARY_TERM> tags around the terms in your translation",
#                 "2. Only translate the content inside the tags according to the rules above",
#                 "3. Translate the rest of the text normally",
#                 "4. Maintain the original structure and formatting",
#                 "",
#             ]
#         )

#         return "\n".join(prompt_parts)

#     async def _verify_translation(
#         self,
#         translated_text: str,
#         original_terms: list[dict[str, Any]],
#         target_lang: str,
#     ) -> dict[str, Any]:
#         """
#         Verify the translation contains expected glossary terms and provide suggestions.

#         Args:
#             translated_text: The translated text with wrapped terms
#             original_terms: Original glossary terms found in source
#             target_lang: Target language code

#         Returns:
#             Dictionary with verification results and suggestions
#         """

#         # Find all wrapped terms in the translation
#         wrapped_pattern = r'<GLOSSARY_TERM id="([^"]+)">([^<]+)</GLOSSARY_TERM>'
#         found_wrapped_terms_list = []

#         for match in re.finditer(wrapped_pattern, translated_text):
#             term_id = match.group(1)
#             term_content = match.group(2)
#             found_wrapped_terms_list.append(
#                 {
#                     "id": term_id,
#                     "content": term_content,
#                     "start": match.start(),
#                     "end": match.end(),
#                 }
#             )

#         # Clean up the translated text by removing tags
#         cleaned_text = re.sub(wrapped_pattern, r"\2", translated_text)

#         # Convert found wrapped terms to dict[str, str] format for schema
#         found_wrapped_terms_dict = {
#             item["id"]: item["content"] for item in found_wrapped_terms_list
#         }

#         # Generate suggestions and warnings
#         suggestions = []
#         warnings = []
#         missing_terms = []
#         has_errors = False

#         for original_term in original_terms:
#             term_id_prefix = f"{original_term['term']}_{original_term['start']}_{original_term['end']}"

#             # Find matching wrapped term in translation
#             matching_wrapped = next(
#                 (wt for wt in found_wrapped_terms_list if wt["id"] == term_id_prefix),
#                 None,
#             )

#             if not matching_wrapped:
#                 missing_terms.append(
#                     {
#                         "term": original_term["term"],
#                         "expected_position": f"{original_term['start']}-{original_term['end']}",
#                         "message": f"Term '{original_term['term']}' was not found in translation",
#                     }
#                 )
#                 suggestions.append(
#                     f"Term '{original_term['term']}' was not found in translation"
#                 )
#                 warnings.append(f"Missing term: {original_term['term']}")
#                 continue

#             # Check if forbidden terms were preserved
#             if original_term["forbidden"]:
#                 if matching_wrapped["content"] != original_term["matched_text"]:
#                     has_errors = True
#                     suggestions.append(
#                         f"Forbidden term '{original_term['term']}' should not be translated"
#                     )
#                     warnings.append(
#                         f"Forbidden term '{original_term['term']}' was incorrectly modified"
#                     )

#             # Check if translatable terms were handled correctly
#             elif original_term["translatable"]:
#                 expected_translation = original_term["translations"].get(target_lang)
#                 if (
#                     expected_translation
#                     and matching_wrapped["content"] != expected_translation
#                 ):
#                     suggestions.append(
#                         f"Term '{original_term['term']}' should be translated as '{expected_translation}'"
#                     )
#                     warnings.append(
#                         f"Term '{original_term['term']}' may not be correctly translated"
#                     )

#         # Determine overall success
#         success = not has_errors and len(missing_terms) == 0

#         logger.info(
#             f"Translation verification completed with {len(suggestions)} suggestions, "
#             f"{len(warnings)} warnings, {len(missing_terms)} missing terms. Success: {success}"
#         )

#         return {
#             "success": success,
#             "missing_terms": missing_terms,
#             "warnings": warnings,
#             "suggestions": suggestions,
#             "found_wrapped_terms": found_wrapped_terms_dict,
#             "cleaned_text": cleaned_text,
#         }


# # Create singleton instance
# glossary_aware_translation_service = GlossaryAwareTranslationService()
