from abc import ABC, abstractmethod
from typing import Any


class TranslationProvider(ABC):
    """Abstract base class for translation providers."""

    @abstractmethod
    async def translate_text(
        self,
        source_text: str,
        source_lang: str,
        target_lang: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Translate text using the provider's API.

        Args:
            source_text: The text to translate
            source_lang: Source language code (e.g., 'en', 'fr', 'es')
            target_lang: Target language code (e.g., 'en', 'fr', 'es')
            system_prompt: Optional system prompt for enhanced translation context
            **kwargs: Additional provider-specific parameters

        Returns:
            Translated text

        Raises:
            Exception: For API errors, rate limits, or invalid keys
        """
        pass

    @abstractmethod
    def get_supported_languages(self) -> dict[str, str]:
        """
        Get supported language codes and their names.

        Returns:
            Dictionary mapping language codes to language names
        """
        pass
