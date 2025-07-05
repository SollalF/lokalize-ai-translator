"""
Segments endpoints for Lokalise API.
"""

from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.lokalise.segments import (
    ProjectSegmentResponse,
    ProjectSegmentsResponse,
    SegmentUpdateRequest,
)

router = APIRouter(prefix="/keys", tags=["segments"])


@router.get("/{key_id}/segments/{language_iso}", response_model=ProjectSegmentsResponse)
async def list_key_segments(
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    language_iso: str = Path(..., description="Language code"),
    disable_references: int | None = Query(
        0,
        description="Whether to disable key references. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    filter_is_reviewed: int | None = Query(
        None,
        description="Filter segments by reviewed status. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    filter_unverified: int | None = Query(
        None,
        description="Filter segments by unverified status. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    filter_untranslated: int | None = Query(
        None,
        description="Filter segments by untranslated status. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    filter_qa_issues: int | None = Query(
        None,
        description="Filter segments by QA issues status. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
) -> ProjectSegmentsResponse:
    """
    List segments for a key.

    Lists all segments for a specific key and language with optional filtering.

    Args:
        project_id: A unique project identifier
        key_id: A unique identifier of the key
        language_iso: Language code
        disable_references: Whether to disable key references (0 or 1)
        filter_is_reviewed: Filter by reviewed status (0 or 1)
        filter_unverified: Filter by unverified status (0 or 1)
        filter_untranslated: Filter by untranslated status (0 or 1)
        filter_qa_issues: Filter by QA issues status (0 or 1)

    Returns:
        ProjectSegmentsResponse: Project segments with project_id and segments array
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get(
    "/{key_id}/segments/{language_iso}/{segment_number}",
    response_model=ProjectSegmentResponse,
)
async def retrieve_key_segment(
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    language_iso: str = Path(..., description="Language code"),
    segment_number: int = Path(..., description="Segment number"),
    disable_references: int | None = Query(
        0,
        description="Whether to disable key references. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
) -> ProjectSegmentResponse:
    """
    Retrieve a Segment object.

    Retrieves a Segment object for a specific key, language, and segment number.

    Args:
        project_id: A unique project identifier
        key_id: A unique identifier of the key
        language_iso: Language code
        segment_number: Segment number
        disable_references: Whether to disable key references (0 or 1)

    Returns:
        ProjectSegmentResponse: Project segment with project_id and single segment object
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put(
    "/{key_id}/segments/{language_iso}/{segment_number}",
    response_model=ProjectSegmentResponse,
)
async def update_key_segment(
    request: SegmentUpdateRequest,
    project_id: str = Path(..., description="A unique project identifier"),
    key_id: int = Path(..., description="A unique identifier of the key"),
    language_iso: str = Path(..., description="Language code"),
    segment_number: int = Path(..., description="Segment number"),
) -> ProjectSegmentResponse:
    """
    Update a segment.

    Updates a segment for a specific key, language, and segment number.

    Args:
        request: Segment update data (value, flags, status IDs)
        project_id: A unique project identifier
        key_id: A unique identifier of the key
        language_iso: Language code
        segment_number: Segment number

    Returns:
        ProjectSegmentResponse: Updated segment with project_id and single segment object
    """
    raise HTTPException(status_code=501, detail="Not implemented")
