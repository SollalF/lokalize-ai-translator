from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.files import (
    FileDeleteResponse,
    FileDownloadRequest,
    FileDownloadResponse,
    FileSyncDownloadResponse,
    FileUploadRequest,
    FileUploadResponse,
    ProjectFilesResponse,
)

router = APIRouter(tags=["lokalise-files"])


@router.get("/files", response_model=ProjectFilesResponse)
async def list_project_files(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    filter_filename: str | None = Query(
        None, description="Set filename filter for the list."
    ),
    limit: int | None = Query(
        100, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """List project files along with associated key count.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/files

    Requires read_files OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/files/upload", response_model=FileUploadResponse, status_code=202)
async def upload_file(
    project_id: str = Path(..., description="A unique project identifier"),
    request: FileUploadRequest = ...,
):
    """Queue a localization file for import.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/files/upload

    Queues a localization file for import and returns a 202 response along with a
    Queued process object. Please note that the 302 response code is not currently
    used, but in the future it will be returned if the same file is already in the
    upload queue.

    Requires write_files OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(
    "/files/async-download", response_model=FileDownloadResponse, status_code=200
)
async def download_files_async(
    project_id: str = Path(..., description="A unique project identifier"),
    request: FileDownloadRequest = ...,
):
    """Start a project export process (async download).

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/files/async-download

    Starts a project export process. The progress can be tracked using the list all
    processes API endpoint. Once complete, the download URL can be accessed using
    the Retrieve process API endpoint.

    Requires read_files OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(
    "/files/download", response_model=FileSyncDownloadResponse, status_code=200
)
async def download_files(
    project_id: str = Path(..., description="A unique project identifier"),
    request: FileDownloadRequest = ...,
):
    """Export project files as a .zip bundle (synchronous download).

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/files/download

    Exports project files as a .zip bundle immediately. The generated bundle is
    uploaded to Amazon S3 and stored for 1 month. Returns the direct download URL.

    Note: Starting June 1st, 2025, this endpoint will be limited to projects with
    under 10,000 key-language pairs.

    Requires read_files OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/files/{file_id}", response_model=FileDeleteResponse, status_code=200)
async def delete_file(
    project_id: str = Path(..., description="A unique project identifier"),
    file_id: int = Path(..., description="A unique identifier of the file"),
):
    """Delete a file and its associated keys from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/files/{file_id}

    Deletes a file and its associated keys from the project. This endpoint is only
    supported for "Documents" projects.

    Requires write_files OAuth access scope.
    """
    raise HTTPException(status_code=501, detail="Not implemented")
