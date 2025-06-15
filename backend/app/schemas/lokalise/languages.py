from pydantic import BaseModel, Field


class Language(BaseModel):
    """Complete Language object from Lokalise API."""

    lang_id: int = Field(..., description="A unique language identifier in the system")
    lang_iso: str = Field(..., description="Language/locale code")
    lang_name: str = Field(..., description="Language name")
    is_rtl: bool = Field(..., description="Whether the language is Right-To-Left")
    plural_forms: list[str] = Field(..., description="List of supported plural forms")


class LanguageFilters(BaseModel):
    """Query parameters for filtering system languages."""

    limit: int | None = Field(
        None, description="Number of items to include (max 5000)", le=5000
    )
    page: int | None = Field(
        None, description="Return results starting from this page", ge=1
    )


class LanguagesListResponse(BaseModel):
    """Response structure for list system languages API call with metadata."""

    languages: list[Language] = Field(..., description="Array of language objects")
    total_count: int | None = Field(
        None, description="Total count of languages (from X-Total-Count header)"
    )


class ProjectLanguagesResponse(BaseModel):
    """Response structure for list project languages API call."""

    project_id: str = Field(..., description="A unique project identifier")
    languages: list[Language] = Field(..., description="Array of language objects")


class ProjectLanguageFilters(BaseModel):
    """Query parameters for filtering project languages."""

    limit: int | None = Field(
        None, description="Number of items to include (max 5000)", le=5000
    )
    page: int | None = Field(
        None, description="Return results starting from this page", ge=1
    )
