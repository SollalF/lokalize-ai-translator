from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import Response

from app.schemas.lokalise.projects import (
    ProjectCreateRequest,
    ProjectDeleteResponse,
    ProjectEmptyResponse,
    ProjectResponse,
    ProjectsResponse,
    ProjectUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=ProjectsResponse)
async def list_projects(
    response: Response,
    filter_team_id: int | None = Query(None, description="Limit results to team ID"),
    filter_names: str | None = Query(
        None, description="One or more project names to filter by (comma separated)"
    ),
    include_statistics: int | None = Query(
        1,
        description="Whether to include project statistics. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    include_settings: int | None = Query(
        1,
        description="Whether to include project settings. Possible values are 1 and 0",
        ge=0,
        le=1,
    ),
    limit: int | None = Query(
        100, description="Number of items to include (max 5000)", ge=1, le=5000
    ),
    page: int | None = Query(
        1, description="Return results starting from this page", ge=1
    ),
):
    """
    Retrieves a list of projects available to the user, authorized with a token.

    This endpoint mirrors the Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects

    Requires read_projects OAuth access scope.
    """
    try:
        # TODO: Implement service call to Lokalise API
        # For now, this is a placeholder that will be implemented later
        # when the service layer is ready

        # The service call would look something like:
        # projects_data = await lokalise_projects_service.list_projects(
        #     filter_team_id=filter_team_id,
        #     filter_names=filter_names,
        #     include_statistics=bool(include_statistics),
        #     include_settings=bool(include_settings),
        #     limit=limit,
        #     page=page,
        # )

        # For now, return empty response
        # When service is implemented, this will be replaced with actual data
        projects_data = {"projects": []}

        # The service would also provide total count for X-Total-Count header
        # total_count = projects_data.get("total_count", 0)
        # response.headers["X-Total-Count"] = str(total_count)

        return ProjectsResponse(**projects_data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve projects: {e!s}"
        )


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(request: ProjectCreateRequest):
    """
    Creates a new project in the specified team. Requires Admin role in the team.

    This endpoint mirrors the Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects

    Requires write_projects OAuth access scope.
    """
    try:
        # TODO: Implement service call to Lokalise API
        # For now, this is a placeholder that will be implemented later
        # when the service layer is ready

        # The service call would look something like:
        # project_data = await lokalise_projects_service.create_project(
        #     name=request.name,
        #     team_id=request.team_id,
        #     description=request.description,
        #     languages=request.languages,
        #     base_lang_iso=request.base_lang_iso,
        #     project_type=request.project_type,
        #     is_segmentation_enabled=request.is_segmentation_enabled,
        # )

        # For now, return a mock response structure
        # When service is implemented, this will be replaced with actual data
        mock_project_data = {
            "project": {
                "project_id": "placeholder_project_id",
                "project_type": request.project_type or "localization_files",
                "name": request.name,
                "description": request.description or "",
                "created_at": "2024-01-01T00:00:00Z",
                "created_at_timestamp": 1704067200,
                "created_by": 1,
                "created_by_email": "user@example.com",
                "team_id": request.team_id or 1,
                "base_language_id": 1,
                "base_language_iso": request.base_lang_iso or "en",
                "settings": {
                    "per_platform_key_names": False,
                    "reviewing": False,
                    "auto_toggle_unverified": True,
                    "offline_translation": False,
                    "key_editing": True,
                    "inline_machine_translations": False,
                    "branching": False,
                    "segmentation": request.is_segmentation_enabled or False,
                    "custom_translation_statuses": False,
                    "custom_translation_statuses_allow_multiple": False,
                    "contributor_preview_download_enabled": False,
                },
                "statistics": {
                    "progress_total": 0.0,
                    "keys_total": 0,
                    "team": 1,
                    "base_words": 0,
                    "qa_issues_total": 0,
                    "qa_issues": {
                        "not_reviewed": 0,
                        "unverified": 0,
                        "spelling_grammar": 0,
                        "inconsistent_placeholders": 0,
                        "inconsistent_html": 0,
                        "different_number_of_urls": 0,
                        "different_urls": 0,
                        "leading_whitespace": 0,
                        "trailing_whitespace": 0,
                        "different_number_of_email_address": 0,
                        "different_email_address": 0,
                        "different_brackets": 0,
                        "different_numbers": 0,
                        "double_space": 0,
                        "special_placeholder": 0,
                        "unbalanced_brackets": 0,
                    },
                },
                "languages": [],
            }
        }

        return ProjectResponse(**mock_project_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {e!s}")


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Retrieves a Project object.

    This endpoint mirrors the Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}

    Requires read_projects OAuth access scope.
    """
    try:
        # TODO: Implement service call to Lokalise API
        # For now, this is a placeholder that will be implemented later
        # when the service layer is ready

        # The service call would look something like:
        # project_data = await lokalise_projects_service.get_project(
        #     project_id=project_id
        # )

        # For now, return a mock response structure
        # When service is implemented, this will be replaced with actual data
        mock_project_data = {
            "project": {
                "project_id": project_id,
                "project_type": "localization_files",
                "name": f"Project {project_id}",
                "description": "Sample project description",
                "created_at": "2024-01-01T00:00:00Z",
                "created_at_timestamp": 1704067200,
                "created_by": 1,
                "created_by_email": "user@example.com",
                "team_id": 1,
                "base_language_id": 1,
                "base_language_iso": "en",
                "settings": {
                    "per_platform_key_names": False,
                    "reviewing": True,
                    "auto_toggle_unverified": True,
                    "offline_translation": False,
                    "key_editing": True,
                    "inline_machine_translations": False,
                    "branching": False,
                    "segmentation": False,
                    "custom_translation_statuses": False,
                    "custom_translation_statuses_allow_multiple": False,
                    "contributor_preview_download_enabled": False,
                },
                "statistics": {
                    "progress_total": 75.5,
                    "keys_total": 150,
                    "team": 5,
                    "base_words": 1200,
                    "qa_issues_total": 3,
                    "qa_issues": {
                        "not_reviewed": 1,
                        "unverified": 2,
                        "spelling_grammar": 0,
                        "inconsistent_placeholders": 0,
                        "inconsistent_html": 0,
                        "different_number_of_urls": 0,
                        "different_urls": 0,
                        "leading_whitespace": 0,
                        "trailing_whitespace": 0,
                        "different_number_of_email_address": 0,
                        "different_email_address": 0,
                        "different_brackets": 0,
                        "different_numbers": 0,
                        "double_space": 0,
                        "special_placeholder": 0,
                        "unbalanced_brackets": 0,
                    },
                },
                "languages": [
                    {
                        "lang_id": 1,
                        "lang_iso": "en",
                        "lang_name": "English",
                        "progress": 100.0,
                        "words_to_do": 0,
                    },
                    {
                        "lang_id": 2,
                        "lang_iso": "es",
                        "lang_name": "Spanish",
                        "progress": 68.5,
                        "words_to_do": 378,
                    },
                    {
                        "lang_id": 3,
                        "lang_iso": "fr",
                        "lang_name": "French",
                        "progress": 58.2,
                        "words_to_do": 502,
                    },
                ],
            }
        }

        return ProjectResponse(**mock_project_data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve project: {e!s}"
        )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    request: ProjectUpdateRequest,
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Updates the details of a project. Requires Manage settings admin right.

    This endpoint mirrors the Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}

    Requires write_projects OAuth access scope.
    """
    try:
        # TODO: Implement service call to Lokalise API
        # For now, this is a placeholder that will be implemented later
        # when the service layer is ready

        # The service call would look something like:
        # project_data = await lokalise_projects_service.update_project(
        #     project_id=project_id,
        #     name=request.name,
        #     description=request.description,
        # )

        # For now, return a mock response structure with updated data
        # When service is implemented, this will be replaced with actual data
        mock_project_data = {
            "project": {
                "project_id": project_id,
                "project_type": "localization_files",
                "name": request.name,  # Updated name
                "description": request.description or "",  # Updated description
                "created_at": "2024-01-01T00:00:00Z",
                "created_at_timestamp": 1704067200,
                "created_by": 1,
                "created_by_email": "user@example.com",
                "team_id": 1,
                "base_language_id": 1,
                "base_language_iso": "en",
                "settings": {
                    "per_platform_key_names": False,
                    "reviewing": True,
                    "auto_toggle_unverified": True,
                    "offline_translation": False,
                    "key_editing": True,
                    "inline_machine_translations": False,
                    "branching": False,
                    "segmentation": False,
                    "custom_translation_statuses": False,
                    "custom_translation_statuses_allow_multiple": False,
                    "contributor_preview_download_enabled": False,
                },
                "statistics": {
                    "progress_total": 75.5,
                    "keys_total": 150,
                    "team": 5,
                    "base_words": 1200,
                    "qa_issues_total": 3,
                    "qa_issues": {
                        "not_reviewed": 1,
                        "unverified": 2,
                        "spelling_grammar": 0,
                        "inconsistent_placeholders": 0,
                        "inconsistent_html": 0,
                        "different_number_of_urls": 0,
                        "different_urls": 0,
                        "leading_whitespace": 0,
                        "trailing_whitespace": 0,
                        "different_number_of_email_address": 0,
                        "different_email_address": 0,
                        "different_brackets": 0,
                        "different_numbers": 0,
                        "double_space": 0,
                        "special_placeholder": 0,
                        "unbalanced_brackets": 0,
                    },
                },
                "languages": [
                    {
                        "lang_id": 1,
                        "lang_iso": "en",
                        "lang_name": "English",
                        "progress": 100.0,
                        "words_to_do": 0,
                    },
                    {
                        "lang_id": 2,
                        "lang_iso": "es",
                        "lang_name": "Spanish",
                        "progress": 68.5,
                        "words_to_do": 378,
                    },
                    {
                        "lang_id": 3,
                        "lang_iso": "fr",
                        "lang_name": "French",
                        "progress": 58.2,
                        "words_to_do": 502,
                    },
                ],
            }
        }

        return ProjectResponse(**mock_project_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update project: {e!s}")


@router.delete("/{project_id}", response_model=ProjectDeleteResponse)
async def delete_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Deletes a project.

    This endpoint mirrors the Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}

    Requires write_projects OAuth access scope.
    """
    try:
        # TODO: Implement service call to Lokalise API
        # For now, this is a placeholder that will be implemented later
        # when the service layer is ready

        # The service call would look something like:
        # delete_result = await lokalise_projects_service.delete_project(
        #     project_id=project_id
        # )

        # For now, return a mock response indicating successful deletion
        # When service is implemented, this will be replaced with actual result
        delete_response = {"project_id": project_id, "project_deleted": True}

        return ProjectDeleteResponse(**delete_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {e!s}")


@router.put("/{project_id}/empty", response_model=ProjectEmptyResponse)
async def empty_project(
    project_id: str = Path(..., description="A unique project identifier"),
):
    """
    Deletes all keys and translations from the project. Requires Manage settings admin right.

    This endpoint mirrors the Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/empty

    Requires write_projects OAuth access scope.
    """
    try:
        # TODO: Implement service call to Lokalise API
        # For now, this is a placeholder that will be implemented later
        # when the service layer is ready

        # The service call would look something like:
        # empty_result = await lokalise_projects_service.empty_project(
        #     project_id=project_id
        # )

        # For now, return a mock response indicating successful emptying
        # When service is implemented, this will be replaced with actual result
        empty_response = {"project_id": project_id, "keys_deleted": True}

        return ProjectEmptyResponse(**empty_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to empty project: {e!s}")
