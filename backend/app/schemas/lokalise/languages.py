from pydantic import BaseModel, Field


class BaseLanguage(BaseModel):
    """Base language model with common fields."""

    lang_id: int = Field(..., description="A unique language identifier in the system")
    lang_iso: str = Field(..., description="Language/locale code")
    lang_name: str = Field(..., description="Language name")


class Language(BaseLanguage):
    """Full language object schema for Lokalise API."""

    is_rtl: bool = Field(..., description="Whether the language is Right-To-Left")
    plural_forms: list[str] = Field(..., description="List of supported plural forms")


class LanguageResponse(BaseModel):
    """Response schema for language operations."""

    language: Language


class LanguagesResponse(BaseModel):
    """Response schema for multiple languages."""

    languages: list[Language]
