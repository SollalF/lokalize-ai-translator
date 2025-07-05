# from typing import Any

# import google.generativeai as genai
# from fastapi import HTTPException
# from tenacity import (
#     retry,
#     retry_if_exception_type,
#     stop_after_attempt,
#     wait_exponential,
# )

# from app.core.config import get_settings
# from app.core.logging import logger
# from app.services.translation_provider import TranslationProvider


# class GeminiService(TranslationProvider):
#     """Service for interacting with Google Gemini API."""

#     def __init__(self):
#         settings = get_settings()
#         if not settings.GEMINI_API_KEY:
#             raise ValueError("Gemini API key is not configured")

#         # Configure the Gemini API
#         genai.configure(api_key=settings.GEMINI_API_KEY)

#         # Initialize the model
#         self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

#         # Configure generation settings
#         self.generation_config = genai.types.GenerationConfig(
#             temperature=0.1,  # Low temperature for consistent translations
#             top_p=0.8,
#             top_k=40,
#             max_output_tokens=2048,
#         )

#     @retry(
#         stop=stop_after_attempt(3),
#         wait=wait_exponential(multiplier=1, min=4, max=10),
#         retry=retry_if_exception_type((Exception,)),
#         reraise=True,
#     )
#     async def translate_text(
#         self,
#         source_text: str,
#         source_lang: str,
#         target_lang: str,
#         system_prompt: str | None = None,
#         **kwargs: Any,
#     ) -> str:
#         """
#         Translate text using Google Gemini API.

#         Args:
#             source_text: The text to translate
#             source_lang: Source language code (e.g., 'en', 'fr', 'es')
#             target_lang: Target language code (e.g., 'en', 'fr', 'es')
#             system_prompt: Optional system prompt for enhanced context
#             **kwargs: Additional Gemini-specific parameters

#         Returns:
#             Translated text

#         Raises:
#             HTTPException: For API errors, rate limits, or invalid keys
#         """
#         try:
#             # Create the translation prompt
#             prompt = self._create_translation_prompt(
#                 source_text, source_lang, target_lang, system_prompt
#             )

#             logger.info(f"Translating text from {source_lang} to {target_lang}")
#             logger.debug(f"Source text: {source_text[:100]}...")

#             # Generate the translation
#             response = self.model.generate_content(
#                 prompt, generation_config=self.generation_config
#             )

#             # Extract the translated text
#             if response.text:
#                 translated_text = response.text.strip()
#                 logger.debug(f"Translated text: {translated_text[:100]}...")
#                 return translated_text
#             else:
#                 raise HTTPException(
#                     status_code=500, detail="Gemini API returned empty response"
#                 )

#         except Exception as e:
#             error_message = str(e)
#             logger.error(f"Gemini API error: {error_message}")

#             if (
#                 "API_KEY_INVALID" in error_message
#                 or "invalid API key" in error_message.lower()
#             ):
#                 raise HTTPException(
#                     status_code=401, detail="Invalid Gemini API key"
#                 ) from e
#             elif (
#                 "quota exceeded" in error_message.lower()
#                 or "rate limit" in error_message.lower()
#             ):
#                 raise HTTPException(
#                     status_code=429, detail="Gemini API rate limit exceeded"
#                 ) from e
#             elif "timeout" in error_message.lower():
#                 raise HTTPException(
#                     status_code=408, detail="Gemini API request timeout"
#                 ) from e
#             else:
#                 raise HTTPException(
#                     status_code=500, detail=f"Gemini API error: {error_message}"
#                 ) from e

#     def get_supported_languages(self) -> dict[str, str]:
#         """
#         Get supported language codes and their names.

#         Returns:
#             Dictionary mapping language codes to language names
#         """
#         return {
#             "en": "English",
#             "es": "Spanish",
#             "fr": "French",
#             "de": "German",
#             "it": "Italian",
#             "pt": "Portuguese",
#             "ru": "Russian",
#             "ja": "Japanese",
#             "ko": "Korean",
#             "zh": "Chinese",
#             "ar": "Arabic",
#             "hi": "Hindi",
#             "nl": "Dutch",
#             "sv": "Swedish",
#             "da": "Danish",
#             "no": "Norwegian",
#             "fi": "Finnish",
#             "pl": "Polish",
#             "tr": "Turkish",
#             "th": "Thai",
#             "vi": "Vietnamese",
#         }

#     def _create_translation_prompt(
#         self,
#         source_text: str,
#         source_lang: str,
#         target_lang: str,
#         system_prompt: str | None = None,
#     ) -> str:
#         """
#         Create a translation prompt for the Gemini model.

#         Args:
#             source_text: The text to translate
#             source_lang: Source language code
#             target_lang: Target language code
#             system_prompt: Optional additional system instructions

#         Returns:
#             Formatted prompt string
#         """
#         # Language code to full name mapping for better context
#         lang_names = self.get_supported_languages()

#         source_lang_name = lang_names.get(source_lang, source_lang)
#         target_lang_name = lang_names.get(target_lang, target_lang)

#         base_prompt = f"""You are a professional translator. Translate the following text from {source_lang_name} to {target_lang_name}.

# Instructions:
# - Provide only the translated text, no explanations or additional content
# - Maintain the original meaning and tone
# - Preserve any formatting, placeholders, or special characters
# - If the text contains technical terms or proper nouns, keep them appropriate for the target language
# - Ensure the translation is natural and fluent in the target language"""

#         if system_prompt:
#             base_prompt += f"\n\nAdditional Instructions:\n{system_prompt}"

#         prompt = f"""{base_prompt}

# Text to translate:
# {source_text}

# Translation:"""

#         return prompt


# # Create a singleton instance
# gemini_service = GeminiService()
