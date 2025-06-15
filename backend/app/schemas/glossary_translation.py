from typing import Any

from pydantic import BaseModel, Field


class GlossaryTranslationRequest(BaseModel):
    """Model for glossary-aware translation request."""

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
    project_id: str | None = Field(
        None, description="Lokalise project ID for glossary operations"
    )
    preserve_forbidden_terms: bool = Field(
        True, description="Whether to preserve forbidden terms unchanged"
    )
    translate_allowed_terms: bool = Field(
        True, description="Whether to translate allowed terms using glossary"
    )


class GlossaryBatchTranslationRequest(BaseModel):
    """Model for glossary-aware batch translation request."""

    texts: list[str] = Field(
        ..., description="List of texts to translate", min_length=1
    )
    source_lang: str = Field(
        ..., description="Source language code", min_length=2, max_length=10
    )
    target_lang: str = Field(
        ..., description="Target language code", min_length=2, max_length=10
    )
    project_id: str | None = Field(
        None, description="Lokalise project ID for glossary operations"
    )
    preserve_forbidden_terms: bool = Field(
        True, description="Whether to preserve forbidden terms unchanged"
    )
    translate_allowed_terms: bool = Field(
        True, description="Whether to translate allowed terms using glossary"
    )


class VerificationResults(BaseModel):
    """Model for translation verification results."""

    success: bool = Field(..., description="Whether verification was successful")
    missing_terms: list[dict[str, Any]] = Field(
        ..., description="List of missing glossary terms"
    )
    warnings: list[str] = Field(..., description="List of warning messages")
    suggestions: list[str] = Field(
        ..., description="List of suggestions for improvements"
    )
    found_wrapped_terms: dict[str, str] = Field(
        ..., description="Terms found in the translation with their values"
    )
    cleaned_text: str = Field(..., description="Translation with wrapper tags removed")


class GlossaryTranslationResponse(BaseModel):
    """Model for glossary-aware translation response."""

    translated_text: str = Field(..., description="Final translated text")
    source_text: str = Field(..., description="Original text")
    source_lang: str = Field(..., description="Source language code")
    target_lang: str = Field(..., description="Target language code")
    glossary_terms_found: list[dict[str, Any]] = Field(
        ..., description="List of glossary terms found in the source text"
    )
    wrapped_text: str = Field(
        ..., description="Source text with glossary terms wrapped"
    )
    verification_results: VerificationResults = Field(
        ..., description="Verification results for the translation"
    )


class GlossaryBatchTranslationResponse(BaseModel):
    """Model for glossary-aware batch translation response."""

    translations: list[GlossaryTranslationResponse] = Field(
        ..., description="List of glossary-aware translations"
    )
