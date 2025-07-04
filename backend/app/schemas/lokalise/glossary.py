from typing import Any

from pydantic import BaseModel, Field


class GlossaryTermTranslation(BaseModel):
    """Translation within a glossary term."""

    lang_id: int = Field(..., description="Language ID")
    lang_name: str = Field("", description="Language name (optional for API responses)")
    lang_iso: str = Field(
        "", description="Language ISO code (optional for API responses)"
    )
    translation: str = Field(..., description="Translation of the term")
    description: str = Field(
        "", description="Description of the translation (optional)"
    )


class GlossaryTermTranslationUpdate(BaseModel):
    """Translation object for glossary term updates."""

    lang_id: int = Field(..., description="Language ID")
    translation: str = Field(..., description="Translation of the term")
    description: str | None = Field(None, description="Description of the translation")


class GlossaryTerm(BaseModel):
    """Complete Glossary Term object from Lokalise API.

    Matches the exact structure returned by GET /projects/{project_id}/glossary-terms
    """

    # Core identification
    id: int = Field(..., description="A unique identifier of the glossary term")
    term: str = Field(..., description="The term added to the glossary")
    description: str = Field(..., description="Explanation of the term")

    # Boolean flags
    case_sensitive: bool = Field(
        False, description="Indicates whether term is case-sensitive"
    )
    translatable: bool = Field(
        True, description="Indicates whether the term should be translatable or not"
    )
    forbidden: bool = Field(
        False, description="If true, the term must not be used in translations"
    )

    # Nested structures
    translations: list[GlossaryTermTranslation] = Field(
        default_factory=list, description="List of translations for the term"
    )
    tags: list[str] = Field(
        default_factory=list, description="List of tags for the term"
    )

    # Project and timestamp info
    project_id: str = Field(..., description="Project ID for which the term resides")
    created_at: str | None = Field(
        None, description="Creation date and time of the term"
    )
    updated_at: str | None = Field(
        None, description="Last updated date and time of the term"
    )


class GlossaryTermMeta(BaseModel):
    """Meta information from Lokalise API response."""

    count: int = Field(..., description="Total number of terms")
    limit: int | None = Field(None, description="Number of items per page")
    cursor: int | None = Field(None, description="Current cursor position")
    has_more: bool = Field(False, description="Whether there are more items available")
    next_cursor: int | None = Field(None, description="Cursor for the next page")


class GlossaryTermsResponse(BaseModel):
    """Full response structure matching Lokalise API."""

    data: list[GlossaryTerm] = Field(..., description="List of glossary terms")
    meta: GlossaryTermMeta = Field(..., description="Pagination and count metadata")


class GlossaryTermResponse(BaseModel):
    """Response structure for single glossary term API call."""

    data: GlossaryTerm = Field(..., description="Single glossary term object")


class GlossaryTermCreate(BaseModel):
    """Schema for creating a new glossary term."""

    term: str = Field(..., description="The term to add to the glossary")
    description: str = Field(..., description="Explanation of the term (required)")
    case_sensitive: bool = Field(..., description="Whether the term is case-sensitive")
    translatable: bool = Field(
        ..., description="Whether the term should be translatable"
    )
    forbidden: bool = Field(
        ..., description="If true, the term must not be used in translations"
    )
    translations: list[GlossaryTermTranslation] = Field(
        default_factory=list, description="List of translations for the term"
    )
    tags: list[str] = Field(
        default_factory=list, description="List of tags for the term"
    )


class GlossaryTermUpdate(BaseModel):
    """Schema for updating a glossary term."""

    id: int = Field(..., description="A unique identifier of the glossary term")
    term: str | None = Field(None, description="The term added to the glossary")
    description: str | None = Field(None, description="Explanation of the term")
    case_sensitive: bool | None = Field(
        None, description="Indicates whether term is case-sensitive"
    )
    translatable: bool | None = Field(
        None, description="Indicates whether the term should be translatable or not"
    )
    forbidden: bool | None = Field(
        None, description="If true, the term must not be used in translations"
    )
    translations: list[GlossaryTermTranslationUpdate] | None = Field(
        None, description="List of translations for the term"
    )
    tags: list[str] | None = Field(None, description="List of tags for the term")


class GlossaryTermsCreate(BaseModel):
    """Schema for creating multiple glossary terms."""

    terms: list[GlossaryTermCreate] = Field(
        ..., description="List of glossary terms to create"
    )


class GlossaryTermsCreateMeta(BaseModel):
    """Meta information from Lokalise API create response."""

    count: int = Field(..., description="Total number of terms processed")
    created: int = Field(..., description="Number of terms successfully created")
    limit: int | None = Field(None, description="Number of items per page")
    errors: dict[str, Any] = Field(
        default_factory=dict, description="Errors encountered during creation"
    )


class GlossaryTermsCreateResponse(BaseModel):
    """Response structure for create glossary terms API call."""

    data: list[GlossaryTerm] = Field(..., description="List of created glossary terms")
    meta: GlossaryTermsCreateMeta = Field(
        ..., description="Creation operation metadata"
    )


class GlossaryTermsUpdate(BaseModel):
    """Schema for updating multiple glossary terms."""

    terms: list[GlossaryTermUpdate] = Field(
        ..., description="List of glossary terms to update"
    )


class GlossaryTermsDeleteResponse(BaseModel):
    """Response structure for delete glossary terms API call."""

    data: "GlossaryTermsDeleteData" = Field(
        ..., description="Deletion operation results"
    )


class GlossaryTermsDeletedInfo(BaseModel):
    """Information about successfully deleted terms."""

    count: int = Field(..., description="Number of deleted terms")
    ids: list[int] = Field(..., description="List of deleted term IDs")


class GlossaryTermsDeleteFailedInfo(BaseModel):
    """Information about failed deletions."""

    count: int = Field(..., description="Number of failed deletions")
    ids: list[int] = Field(..., description="List of failed term IDs")
    message: str = Field(..., description="Error message for failed deletions")


class GlossaryTermsDeleteData(BaseModel):
    """Data structure within delete response."""

    deleted: GlossaryTermsDeletedInfo = Field(
        ..., description="Information about deleted terms"
    )
    failed: GlossaryTermsDeleteFailedInfo = Field(
        ..., description="Information about failed deletions"
    )


class GlossaryTermsDelete(BaseModel):
    """Schema for deleting multiple glossary terms."""

    terms: list[int] = Field(..., description="List of term IDs to delete")


class GlossaryTermFilters(BaseModel):
    """Query parameters for filtering glossary terms."""

    limit: int | None = Field(None, description="Number of items to include")
    cursor: int | None = Field(None, description="Cursor position for pagination")


class GlossaryTermsUpdateMeta(BaseModel):
    """Meta information from Lokalise API update response."""

    count: int = Field(..., description="Total number of terms processed")
    updated: int = Field(..., description="Number of terms successfully updated")
    limit: int | None = Field(None, description="Number of items per page")
    errors: dict[str, Any] = Field(
        default_factory=dict, description="Errors encountered during update"
    )


class GlossaryTermsUpdateResponse(BaseModel):
    """Response structure for update glossary terms API call."""

    data: list[GlossaryTerm] = Field(..., description="List of updated glossary terms")
    meta: GlossaryTermsUpdateMeta = Field(..., description="Update operation metadata")
