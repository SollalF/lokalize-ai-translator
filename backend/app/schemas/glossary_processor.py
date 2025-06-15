from pydantic import BaseModel, Field


class FoundTerm(BaseModel):
    """Information about a term found in text."""

    term: str = Field(description="The original glossary term")
    matched_text: str = Field(description="The actual text that was matched")
    start: int = Field(description="Start position in the text")
    end: int = Field(description="End position in the text")
    case_sensitive: bool = Field(description="Whether this term is case sensitive")
    forbidden: bool = Field(description="Whether this term is forbidden")
    translatable: bool = Field(description="Whether this term is translatable")
    translations: dict[str, str] = Field(
        description="Available translations by language code"
    )


class TextProcessingRequest(BaseModel):
    """Request for text processing operations."""

    text: str = Field(description="Text to process")
    target_lang: str | None = Field(
        None, description="Target language for replacements"
    )
    wrapper_tag: str = Field("GLOSSARY_TERM", description="Tag name for wrapping terms")


class TextProcessingResponse(BaseModel):
    """Response for text processing operations."""

    original_text: str = Field(description="Original input text")
    processed_text: str = Field(description="Processed text")
    found_terms: list[FoundTerm] = Field(description="Terms found in the text")
    target_lang: str | None = Field(None, description="Target language used")


class TermLookupRequest(BaseModel):
    """Request for term lookup."""

    term: str = Field(description="Term to look up")


class TermLookupResponse(BaseModel):
    """Response for term lookup."""

    term: str = Field(description="The queried term")
    found: bool = Field(description="Whether the term was found")
    translations: dict[str, str] | None = Field(
        None, description="Available translations"
    )
    case_sensitive: bool | None = Field(
        None, description="Whether the term is case sensitive"
    )
    forbidden: bool | None = Field(None, description="Whether the term is forbidden")
    translatable: bool | None = Field(
        None, description="Whether the term is translatable"
    )
    description: str | None = Field(None, description="Term description")
    part_of_speech: str | None = Field(None, description="Part of speech")
    tags: str | None = Field(None, description="Term tags")


class GlossaryStats(BaseModel):
    """Glossary statistics."""

    total_terms: int = Field(description="Total number of terms")
    case_sensitive_terms: int = Field(description="Number of case-sensitive terms")
    case_insensitive_terms: int = Field(description="Number of case-insensitive terms")
    forbidden_terms: int = Field(description="Number of forbidden terms")
    translatable_terms: int = Field(description="Number of translatable terms")
    available_languages: list[str] = Field(description="Available language codes")
    language_count: int = Field(description="Number of available languages")


class GlossaryLoadResponse(BaseModel):
    """Response for glossary loading operations."""

    success: bool = Field(description="Whether the loading was successful")
    message: str = Field(description="Status message")
    stats: GlossaryStats | None = Field(None, description="Glossary statistics")
