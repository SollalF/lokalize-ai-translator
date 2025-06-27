from pydantic import BaseModel, Field


class File(BaseModel):
    """File object schema for Lokalise API."""

    file_id: int = Field(..., description="A unique identifier of the file")
    filename: str = Field(..., description="File name")
    key_count: int = Field(
        ..., description="Total number of keys, associated with this file"
    )


class FileResponse(BaseModel):
    """Response schema for file operations."""

    file: File


class FilesResponse(BaseModel):
    """Response schema for multiple files."""

    files: list[File]
