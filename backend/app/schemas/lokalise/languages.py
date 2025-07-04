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
    cc_iso: str = Field(..., description="Country code, associated with the language")


class LanguageResponse(BaseModel):
    """Response schema for language operations."""

    language: Language


class LanguagesResponse(BaseModel):
    """Response schema for multiple languages."""

    languages: list[Language]


class ProjectLanguagesResponse(BaseModel):
    """Response schema for project languages."""

    project_id: str = Field(..., description="A unique project identifier")
    languages: list[Language] = Field(
        ..., description="List of languages in the project"
    )


class ProjectLanguageResponse(BaseModel):
    """Response schema for retrieving a single project language."""

    project_id: str = Field(..., description="A unique project identifier")
    language: Language = Field(..., description="The language object")


class LanguageUpdateRequest(BaseModel):
    """Request schema for updating a language."""

    lang_iso: str | None = Field(None, description="Language/locale code")
    lang_name: str | None = Field(None, description="Language name")
    plural_forms: list[str] | None = Field(
        None, description="List of supported plural forms"
    )


class LanguageDeleteResponse(BaseModel):
    """Response schema for deleting a language."""

    project_id: str = Field(..., description="A unique project identifier")
    language_deleted: bool = Field(..., description="Whether the language was deleted")
