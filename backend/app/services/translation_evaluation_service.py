# import json
# import re
# from difflib import SequenceMatcher
# from typing import Any

# import sacrebleu

# from app.core.logging import logger
# from app.services.gemini_service import gemini_service
# from app.services.glossary_processor import glossary_processor


# class TranslationEvaluationService:
#     """Service for evaluating translation quality using objective metrics."""

#     def __init__(self):
#         self.glossary_processor = glossary_processor
#         self.llm_service = gemini_service

#     async def evaluate_translation(
#         self,
#         source_text: str,
#         source_lang: str,
#         translated_text: str,
#         target_lang: str,
#         reference_text: str | None = None,
#         project_id: str | None = None,
#     ) -> dict[str, Any]:
#         """
#         Evaluate translation quality using objective metrics.

#         Args:
#             source_text: Original text to be translated
#             source_lang: Source language code
#             translated_text: The translated text to evaluate
#             target_lang: Target language code
#             reference_text: Optional reference translation for comparison
#             project_id: Optional Lokalise project ID for glossary checking

#         Returns:
#             Dictionary containing evaluation results
#         """
#         logger.info("=== STARTING TRANSLATION EVALUATION ===")
#         logger.info(f"Source: '{source_text}' ({source_lang})")
#         logger.info(f"Translation: '{translated_text}' ({target_lang})")
#         logger.info(f"Reference: '{reference_text}'")
#         logger.info(f"Project ID: '{project_id}'")

#         # Step 1: Compute objective metrics
#         metric_scores = self._compute_metrics(translated_text, reference_text)
#         logger.info(f"Computed metrics: {metric_scores}")

#         # Step 2: Check glossary compliance (if project_id provided)
#         glossary_compliance = None
#         if project_id:
#             logger.info("=== CHECKING GLOSSARY COMPLIANCE ===")
#             glossary_compliance = await self._check_glossary_compliance(
#                 source_text, translated_text, source_lang, target_lang, project_id
#             )
#             logger.info(f"Glossary compliance: {glossary_compliance}")

#         # Step 3: Get LLM qualitative feedback
#         logger.info("=== GETTING LLM FEEDBACK ===")
#         llm_feedback = await self._get_llm_feedback(
#             source_text, translated_text, source_lang, target_lang, reference_text
#         )
#         logger.info(f"LLM feedback: {llm_feedback}")

#         # Step 4: Determine overall assessment based on all factors
#         overall_assessment = self._determine_overall_assessment(
#             metric_scores, glossary_compliance, llm_feedback
#         )
#         logger.info(f"Overall assessment: {overall_assessment}")

#         result = {
#             "source_text": source_text,
#             "translated_text": translated_text,
#             "reference_text": reference_text,
#             "source_lang": source_lang,
#             "target_lang": target_lang,
#             "metric_scores": metric_scores,
#             "glossary_compliance": glossary_compliance,
#             "llm_feedback": llm_feedback,
#             "overall_assessment": overall_assessment,
#         }

#         logger.info("=== TRANSLATION EVALUATION COMPLETED ===")
#         return result

#     async def _check_glossary_compliance(
#         self,
#         source_text: str,
#         translated_text: str,
#         source_lang: str,
#         target_lang: str,
#         project_id: str,
#     ) -> dict[str, Any]:
#         """
#         Check glossary compliance by analyzing how terms were handled.

#         Args:
#             source_text: Original source text
#             translated_text: The translated text to evaluate
#             source_lang: Source language code
#             target_lang: Target language code
#             project_id: Lokalise project ID

#         Returns:
#             Dictionary containing glossary compliance results
#         """
#         try:
#             # Find glossary terms in source text
#             logger.info("Finding glossary terms in source text...")
#             found_terms = await self.glossary_processor.find_terms_in_text(
#                 source_text, project_id
#             )
#             logger.info(f"Found {len(found_terms)} glossary terms in source text")

#             if not found_terms:
#                 return {
#                     "terms_found_in_source": [],
#                     "terms_correctly_handled": [],
#                     "terms_incorrectly_handled": [],
#                     "compliance_score": None,
#                     "compliance_summary": "No glossary terms found in source text",
#                 }

#             # Analyze each term's handling in the translation
#             correctly_handled = []
#             incorrectly_handled = []

#             for term_info in found_terms:
#                 logger.info(f"Analyzing term: '{term_info['term']}'")
#                 logger.info(f"  - Forbidden: {term_info['forbidden']}")
#                 logger.info(f"  - Translatable: {term_info['translatable']}")
#                 logger.info(f"  - Matched text: '{term_info['matched_text']}'")

#                 # Check how this term was handled in the translation
#                 is_correctly_handled = await self._analyze_term_handling(
#                     term_info, source_text, translated_text, target_lang, project_id
#                 )

#                 if is_correctly_handled:
#                     correctly_handled.append(term_info)
#                     logger.info("  ✓ Term correctly handled")
#                 else:
#                     incorrectly_handled.append(term_info)
#                     logger.info("  ✗ Term incorrectly handled")

#             # Calculate compliance score
#             total_terms = len(found_terms)
#             correct_terms = len(correctly_handled)
#             compliance_score = (
#                 (correct_terms / total_terms * 100) if total_terms > 0 else None
#             )

#             # Generate compliance summary
#             compliance_summary = self._generate_compliance_summary(
#                 total_terms, correct_terms, incorrectly_handled
#             )

#             return {
#                 "terms_found_in_source": found_terms,
#                 "terms_correctly_handled": correctly_handled,
#                 "terms_incorrectly_handled": incorrectly_handled,
#                 "compliance_score": round(compliance_score, 1)
#                 if compliance_score is not None
#                 else None,
#                 "compliance_summary": compliance_summary,
#             }

#         except Exception as e:
#             logger.error(f"Error checking glossary compliance: {e}", exc_info=True)
#             return {
#                 "terms_found_in_source": [],
#                 "terms_correctly_handled": [],
#                 "terms_incorrectly_handled": [],
#                 "compliance_score": None,
#                 "compliance_summary": f"Error checking glossary compliance: {e}",
#             }

#     async def _analyze_term_handling(
#         self,
#         term_info: dict[str, Any],
#         source_text: str,
#         translated_text: str,
#         target_lang: str,
#         project_id: str,
#     ) -> bool:
#         """
#         Analyze if a specific term was handled correctly in the translation.

#         Args:
#             term_info: Information about the glossary term
#             source_text: Original source text
#             translated_text: The translated text
#             target_lang: Target language code
#             project_id: Lokalise project ID

#         Returns:
#             True if term was handled correctly, False otherwise
#         """
#         term = term_info["term"]
#         matched_text = term_info["matched_text"]
#         forbidden = term_info["forbidden"]
#         translatable = term_info["translatable"]

#         logger.info(
#             f"Analyzing term handling for: '{term}' (matched: '{matched_text}')"
#         )

#         # Case 1: Forbidden terms should be preserved exactly
#         if forbidden:
#             logger.info("Term is forbidden - checking if preserved exactly")
#             # Check if the exact matched text appears in translation
#             if matched_text.lower() in translated_text.lower():
#                 logger.info(
#                     f"Forbidden term '{matched_text}' found preserved in translation"
#                 )
#                 return True
#             else:
#                 logger.info(f"Forbidden term '{matched_text}' NOT found in translation")
#                 return False

#         # Case 2: Translatable terms should be translated according to glossary
#         if translatable:
#             logger.info("Term is translatable - checking if properly translated")
#             # Check if we have translation data in the term_info itself
#             if term_info.get("translations"):
#                 translations = term_info["translations"]
#                 expected_translation = translations.get(target_lang)

#                 if expected_translation:
#                     logger.info(f"Expected translation: '{expected_translation}'")
#                     # Check if expected translation appears in the translated text
#                     # Use case-insensitive search but be more precise about word boundaries
#                     pattern = re.compile(
#                         re.escape(expected_translation.lower()), re.IGNORECASE
#                     )
#                     if pattern.search(translated_text.lower()):
#                         logger.info(
#                             f"Expected translation '{expected_translation}' found in translation"
#                         )
#                         return True
#                     else:
#                         logger.info(
#                             f"Expected translation '{expected_translation}' NOT found in translation"
#                         )
#                         logger.info(f"Actual translation contains: '{translated_text}'")
#                         return False
#                 else:
#                     logger.info(
#                         f"No translation found for language '{target_lang}' in glossary"
#                     )
#                     # If no specific translation available, we can't verify compliance
#                     return False
#             else:
#                 logger.info("No translation data found in term info")
#                 return False

#         # Case 3: Non-translatable, non-forbidden terms should be preserved
#         logger.info("Term is non-translatable, non-forbidden - checking if preserved")
#         if matched_text.lower() in translated_text.lower():
#             logger.info(f"Non-translatable term '{matched_text}' found preserved")
#             return True
#         else:
#             logger.info(f"Non-translatable term '{matched_text}' NOT found preserved")
#             return False

#     def _generate_compliance_summary(
#         self,
#         total_terms: int,
#         correct_terms: int,
#         incorrectly_handled: list[dict[str, Any]],
#     ) -> str:
#         """Generate a human-readable compliance summary."""
#         if total_terms == 0:
#             return "No glossary terms found in source text"

#         compliance_percentage = (correct_terms / total_terms) * 100

#         if compliance_percentage == 100:
#             return f"Perfect compliance: All {total_terms} glossary terms handled correctly"
#         elif compliance_percentage >= 80:
#             return f"Good compliance: {correct_terms}/{total_terms} terms handled correctly ({compliance_percentage:.1f}%)"
#         elif compliance_percentage >= 60:
#             return f"Fair compliance: {correct_terms}/{total_terms} terms handled correctly ({compliance_percentage:.1f}%)"
#         else:
#             return f"Poor compliance: Only {correct_terms}/{total_terms} terms handled correctly ({compliance_percentage:.1f}%)"

#     def _compute_metrics(
#         self, translated_text: str, reference_text: str | None
#     ) -> dict[str, Any]:
#         """
#         Compute objective translation metrics using sacrebleu.

#         Args:
#             translated_text: The translated text to evaluate
#             reference_text: Optional reference translation

#         Returns:
#             Dictionary containing computed metric scores
#         """
#         scores: dict[str, float | int | None] = {
#             "bleu": None,
#             "ter": None,
#             "chrf": None,
#             "edit_distance": None,
#         }

#         if not reference_text:
#             logger.info("No reference text provided, skipping metric computation")
#             return scores

#         try:
#             # BLEU score (sentence-level)
#             bleu = sacrebleu.sentence_bleu(translated_text, [reference_text])
#             scores["bleu"] = round(bleu.score, 2)
#             logger.info(f"BLEU score: {scores['bleu']}")

#             # TER score (sentence-level)
#             ter = sacrebleu.sentence_ter(translated_text, [reference_text])
#             scores["ter"] = round(ter.score, 2)
#             logger.info(f"TER score: {scores['ter']}")

#             # chrF score (sentence-level)
#             chrf = sacrebleu.sentence_chrf(translated_text, [reference_text])
#             scores["chrf"] = round(chrf.score, 2)
#             logger.info(f"chrF score: {scores['chrf']}")

#             # Character-level edit distance
#             scores["edit_distance"] = self._compute_edit_distance(
#                 translated_text, reference_text
#             )
#             logger.info(f"Edit distance: {scores['edit_distance']}")

#         except Exception as e:
#             logger.error(f"Error computing metrics: {e}", exc_info=True)

#         return scores

#     def _compute_edit_distance(self, text1: str, text2: str) -> int:
#         """
#         Compute character-level edit distance using difflib.

#         Args:
#             text1: First text
#             text2: Second text

#         Returns:
#             Character-level edit distance
#         """
#         # Use SequenceMatcher to compute similarity ratio
#         matcher = SequenceMatcher(None, text1, text2)
#         # Convert similarity ratio to edit distance
#         max_len = max(len(text1), len(text2))
#         if max_len == 0:
#             return 0
#         similarity = matcher.ratio()
#         edit_distance = int(max_len * (1 - similarity))
#         return edit_distance

#     async def _get_llm_feedback(
#         self,
#         source_text: str,
#         translated_text: str,
#         source_lang: str,
#         target_lang: str,
#         reference_text: str | None = None,
#     ) -> dict[str, Any]:
#         """
#         Get qualitative feedback from LLM about translation quality.

#         Args:
#             source_text: Original source text
#             translated_text: The translated text to evaluate
#             source_lang: Source language code
#             target_lang: Target language code
#             reference_text: Optional reference translation

#         Returns:
#             Dictionary containing LLM feedback
#         """
#         try:
#             # Create evaluation prompt
#             evaluation_prompt = self._create_evaluation_prompt(
#                 source_text, translated_text, source_lang, target_lang, reference_text
#             )

#             logger.info("Sending evaluation request to LLM...")
#             logger.info(f"Prompt length: {len(evaluation_prompt)}")

#             # Get LLM response using the model directly
#             response = self.llm_service.model.generate_content(
#                 evaluation_prompt, generation_config=self.llm_service.generation_config
#             )

#             if not response.text:
#                 raise Exception("LLM returned empty response")

#             llm_response = response.text.strip()

#             logger.info(f"LLM response received (length: {len(llm_response)})")
#             logger.info(f"LLM response preview: {llm_response[:200]}...")

#             # Parse JSON response
#             cleaned_response = llm_response  # Initialize here to avoid scope issues
#             try:
#                 # Clean up the response - remove markdown code blocks if present
#                 if "```json" in llm_response:
#                     # Extract JSON from markdown code blocks
#                     start = llm_response.find("```json") + 7
#                     end = llm_response.find("```", start)
#                     if end != -1:
#                         cleaned_response = llm_response[start:end].strip()
#                 elif "```" in llm_response:
#                     # Handle generic code blocks
#                     start = llm_response.find("```") + 3
#                     end = llm_response.find("```", start)
#                     if end != -1:
#                         cleaned_response = llm_response[start:end].strip()

#                 logger.info(f"Cleaned response: {cleaned_response[:200]}...")
#                 feedback_data = json.loads(cleaned_response)
#                 logger.info("Successfully parsed LLM feedback JSON")

#                 # Remove numerical scores from the response if they exist
#                 feedback_data.pop("fluency_score", None)
#                 feedback_data.pop("accuracy_score", None)
#                 feedback_data.pop("style_score", None)
#                 feedback_data.pop("overall_score", None)

#                 return feedback_data
#             except json.JSONDecodeError as e:
#                 logger.error(f"Failed to parse LLM response as JSON: {e}")
#                 logger.error(f"Raw response: {llm_response}")
#                 try:
#                     logger.error(f"Cleaned response: {cleaned_response}")
#                 except NameError:
#                     logger.error("Cleaned response variable not available")
#                 # Return fallback feedback
#                 return self._create_fallback_feedback(llm_response)

#         except Exception as e:
#             logger.error(f"Error getting LLM feedback: {e}", exc_info=True)
#             return self._create_error_feedback(str(e))

#     def _create_evaluation_prompt(
#         self,
#         source_text: str,
#         translated_text: str,
#         source_lang: str,
#         target_lang: str,
#         reference_text: str | None = None,
#     ) -> str:
#         """Create a detailed prompt for LLM translation evaluation."""

#         # Language name mapping for better prompts
#         lang_names = {
#             "en": "English",
#             "en_US": "English (US)",
#             "fr": "French",
#             "fr_CA": "French (Canada)",
#             "es": "Spanish",
#             "es_419": "Spanish (Latin America)",
#             "it": "Italian",
#             "ko": "Korean",
#             "zh_CN": "Chinese (Simplified)",
#             "zh_TW": "Chinese (Traditional)",
#         }

#         source_lang_name = lang_names.get(source_lang, source_lang)
#         target_lang_name = lang_names.get(target_lang, target_lang)

#         reference_section = ""
#         if reference_text:
#             reference_section = f"""
# Reference Translation: "{reference_text}"
# """

#         prompt = f"""Please evaluate this translation and provide detailed qualitative feedback in JSON format.

# Source Text ({source_lang_name}): "{source_text}"
# Translation ({target_lang_name}): "{translated_text}"{reference_section}

# Analyze the translation considering:
# 1. **Fluency**: How natural and well-flowing is the translation in the target language?
# 2. **Accuracy**: How well does the translation convey the meaning of the source text?
# 3. **Style**: How appropriate is the style and register for the context?
# 4. **Terminology**: Are technical terms and specialized vocabulary handled correctly?

# Please respond with a JSON object in this exact format:
# {{
#     "strengths": ["strength1", "strength2", ...],
#     "weaknesses": ["weakness1", "weakness2", ...],
#     "specific_comments": [
#         {{"part": "specific text part", "comment": "comment about this part"}},
#         ...
#     ],
#     "suggestions": ["suggestion1", "suggestion2", ...],
#     "summary": "Overall assessment summary in 2-3 sentences"
# }}

# Focus on being constructive and specific in your feedback. Provide actionable insights."""

#         return prompt

#     def _create_fallback_feedback(self, raw_response: str) -> dict[str, Any]:
#         """Create fallback feedback when JSON parsing fails."""
#         return {
#             "strengths": ["Translation provided"],
#             "weaknesses": ["Unable to parse detailed feedback from LLM"],
#             "specific_comments": [],
#             "suggestions": [
#                 "Review translation for accuracy and fluency",
#                 "Consider manual evaluation",
#             ],
#             "summary": f"LLM provided feedback but format was invalid. Raw response preview: {raw_response[:100]}...",
#         }

#     def _create_error_feedback(self, error_message: str) -> dict[str, Any]:
#         """Create error feedback when LLM call fails."""
#         return {
#             "strengths": [],
#             "weaknesses": ["Unable to get LLM feedback due to technical error"],
#             "specific_comments": [],
#             "suggestions": ["Manual review recommended", "Retry evaluation if needed"],
#             "summary": f"Error getting LLM feedback: {error_message}",
#         }

#     def _determine_overall_assessment(
#         self,
#         metric_scores: dict[str, Any],
#         glossary_compliance: dict[str, Any] | None,
#         llm_feedback: dict[str, Any] | None,
#     ) -> str:
#         """
#         Determine overall assessment based on objective metrics, glossary compliance, and LLM feedback.

#         Args:
#             metric_scores: Dictionary containing computed metrics
#             glossary_compliance: Dictionary containing glossary compliance results
#             llm_feedback: Dictionary containing LLM feedback

#         Returns:
#             Overall quality assessment string
#         """
#         assessments = []

#         # Metric-based assessment
#         metric_assessment = self._get_metric_assessment(metric_scores)
#         if metric_assessment:
#             assessments.append(f"Metrics: {metric_assessment}")

#         # Glossary compliance assessment
#         if (
#             glossary_compliance
#             and glossary_compliance.get("compliance_score") is not None
#         ):
#             compliance_score = glossary_compliance["compliance_score"]
#             if compliance_score == 100:
#                 assessments.append("Glossary: Perfect compliance")
#             elif compliance_score >= 80:
#                 assessments.append(
#                     f"Glossary: Good compliance ({compliance_score:.1f}%)"
#                 )
#             elif compliance_score >= 60:
#                 assessments.append(
#                     f"Glossary: Fair compliance ({compliance_score:.1f}%)"
#                 )
#             else:
#                 assessments.append(
#                     f"Glossary: Poor compliance ({compliance_score:.1f}%)"
#                 )
#         elif glossary_compliance:
#             assessments.append("Glossary: No terms to evaluate")

#         # LLM feedback assessment
#         if llm_feedback and llm_feedback.get("summary"):
#             # Use a simple assessment based on the presence of feedback
#             if llm_feedback.get("weaknesses") and len(llm_feedback["weaknesses"]) > len(
#                 llm_feedback.get("strengths", [])
#             ):
#                 assessments.append("LLM: Issues identified")
#             elif llm_feedback.get("strengths"):
#                 assessments.append("LLM: Positive feedback")
#             else:
#                 assessments.append("LLM: Feedback provided")

#         if not assessments:
#             return "No evaluation criteria available"

#         return " | ".join(assessments)

#     def _get_metric_assessment(self, metric_scores: dict[str, Any]) -> str | None:
#         """Get assessment based on metrics only."""
#         # If no metrics available, return None
#         if not any(score is not None for score in metric_scores.values()):
#             return None

#         # Use BLEU as primary metric if available
#         bleu_score = metric_scores.get("bleu")
#         if bleu_score is not None:
#             if bleu_score >= 80:
#                 return "Excellent (BLEU ≥ 80)"
#             elif bleu_score >= 60:
#                 return "Good (BLEU ≥ 60)"
#             elif bleu_score >= 40:
#                 return "Fair (BLEU ≥ 40)"
#             else:
#                 return "Poor (BLEU < 40)"

#         # Fallback to chrF if BLEU not available
#         chrf_score = metric_scores.get("chrf")
#         if chrf_score is not None:
#             if chrf_score >= 80:
#                 return "Excellent (chrF ≥ 80)"
#             elif chrf_score >= 60:
#                 return "Good (chrF ≥ 60)"
#             elif chrf_score >= 40:
#                 return "Fair (chrF ≥ 40)"
#             else:
#                 return "Poor (chrF < 40)"

#         # Fallback to TER (lower is better)
#         ter_score = metric_scores.get("ter")
#         if ter_score is not None:
#             if ter_score <= 20:
#                 return "Excellent (TER ≤ 20)"
#             elif ter_score <= 40:
#                 return "Good (TER ≤ 40)"
#             elif ter_score <= 60:
#                 return "Fair (TER ≤ 60)"
#             else:
#                 return "Poor (TER > 60)"

#         return None


# # Create singleton instance
# translation_evaluation_service = TranslationEvaluationService()
