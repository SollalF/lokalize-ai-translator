from typing import Any

from pydantic import BaseModel


class GlossaryTermTranslation(BaseModel):
    """Translation within a glossary term."""

    lang_id: int
    lang_name: str = ""  # Optional for API responses
    lang_iso: str = ""  # Optional for API responses
    translation: str
    description: str = ""  # Optional field


class GlossaryTerm(BaseModel):
    """Complete Glossary Term object from Lokalise API.

    Matches the exact structure returned by GET /projects/{project_id}/glossary-terms
    """

    # Core identification (exact API field names)
    id: int  # API: "id"
    term: str  # API: "term"
    description: str  # API: "description"

    # Boolean flags (exact API field names)
    case_sensitive: bool = False  # API: "caseSensitive" -> snake_case for Python
    translatable: bool = True  # API: "translatable"
    forbidden: bool = False  # API: "forbidden"

    # Nested structures
    translations: list[GlossaryTermTranslation] = []  # API: "translations"
    tags: list[str] = []  # API: "tags"

    # Project and timestamp info (exact API field names)
    project_id: str  # API: "projectId" -> snake_case for Python
    created_at: str | None = None  # API: "createdAt" -> snake_case for Python
    updated_at: str | None = None  # API: "updatedAt" -> snake_case for Python


class GlossaryTermMeta(BaseModel):
    """Meta information from Lokalise API response."""

    count: int
    limit: int | None = None
    cursor: int | None = None
    has_more: bool = False  # API: "hasMore" -> snake_case for Python
    next_cursor: int | None = None  # API: "nextCursor" -> snake_case for Python


class GlossaryTermsResponse(BaseModel):
    """Full response structure matching Lokalise API."""

    data: list[GlossaryTerm]
    meta: GlossaryTermMeta


class GlossaryTermResponse(BaseModel):
    """Response structure for single glossary term API call."""

    data: GlossaryTerm


class GlossaryTermCreate(BaseModel):
    """Schema for creating a new glossary term."""

    term: str
    description: str | None = None
    case_sensitive: bool = False
    translatable: bool = True
    forbidden: bool = False
    translations: list[GlossaryTermTranslation] = []  # Add translations support
    tags: list[str] = []  # Add tags support


class GlossaryTermUpdate(BaseModel):
    """Schema for updating a glossary term."""

    term_id: int  # Keep as term_id for internal use, maps to "id" in API
    term: str | None = None
    description: str | None = None
    case_sensitive: bool | None = None
    translatable: bool | None = None
    forbidden: bool | None = None


class GlossaryTermsCreate(BaseModel):
    """Schema for creating multiple glossary terms."""

    terms: list[GlossaryTermCreate]


class GlossaryTermsCreateMeta(BaseModel):
    """Meta information from Lokalise API create response."""

    count: int
    created: int
    limit: int | None = None
    errors: dict[str, Any] = {}  # Additional fields for errors


class GlossaryTermsCreateResponse(BaseModel):
    """Response structure for create glossary terms API call."""

    data: list[GlossaryTerm]
    meta: GlossaryTermsCreateMeta


class GlossaryTermsUpdate(BaseModel):
    """Schema for updating multiple glossary terms."""

    terms: list[GlossaryTermUpdate]


class GlossaryTermsDeleteResponse(BaseModel):
    """Response structure for delete glossary terms API call."""

    data: "GlossaryTermsDeleteData"


class GlossaryTermsDeleteData(BaseModel):
    """Data structure within delete response."""

    deleted: dict[str, int | list[int]] = {}  # Structure for deleted terms info
    failed: dict[str, int | list[int]] = {}  # Structure for failed deletions info


class GlossaryTermsDelete(BaseModel):
    """Schema for deleting multiple glossary terms."""

    terms: list[int]  # List of term IDs to delete


class GlossaryTermFilters(BaseModel):
    """Query parameters for filtering glossary terms."""

    limit: int | None = None
    cursor: int | None = None


class GlossaryTermsUpdateMeta(BaseModel):
    """Meta information from Lokalise API update response."""

    count: int
    updated: int
    limit: int | None = None
    errors: dict[str, Any] = {}  # Additional fields for errors


class GlossaryTermsUpdateResponse(BaseModel):
    """Response structure for update glossary terms API call."""

    data: list[GlossaryTerm]
    meta: GlossaryTermsUpdateMeta
