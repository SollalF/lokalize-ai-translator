from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    """Model for translation request."""

    source_text: str = Field(..., description="Text to translate", min_length=1)
    source_lang: str = Field(
        ...,
        description="Source language code (e.g., 'en', 'fr', 'es_419')",
        min_length=2,
        max_length=10,
    )
    target_lang: str = Field(
        ...,
        description="Target language code (e.g., 'en', 'fr', 'es_419')",
        min_length=2,
        max_length=10,
    )


class TranslationResponse(BaseModel):
    """Model for translation response."""

    translated_text: str = Field(..., description="Translated text")
    source_text: str = Field(..., description="Original text")
    source_lang: str = Field(..., description="Source language code")
    target_lang: str = Field(..., description="Target language code")


class BatchTranslationRequest(BaseModel):
    """Model for batch translation request."""

    texts: list[str] = Field(
        ..., description="List of texts to translate", min_length=1
    )
    source_lang: str = Field(
        ..., description="Source language code", min_length=2, max_length=10
    )
    target_lang: str = Field(
        ..., description="Target language code", min_length=2, max_length=10
    )


class BatchTranslationResponse(BaseModel):
    """Model for batch translation response."""

    translations: list[TranslationResponse] = Field(
        ..., description="List of translations"
    )
