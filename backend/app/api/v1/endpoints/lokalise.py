from fastapi import APIRouter, Query, Response

from app.schemas.lokalise import (
    GlossaryTermResponse,
    GlossaryTermsCreate,
    GlossaryTermsCreateResponse,
    GlossaryTermsDelete,
    GlossaryTermsDeleteResponse,
    GlossaryTermsResponse,
    GlossaryTermsUpdate,
    GlossaryTermsUpdateResponse,
    KeysCreate,
    KeysCreateResponse,
    LanguageFilters,
    LanguagesListResponse,
    ProjectFilters,
    ProjectLanguageFilters,
    ProjectLanguagesResponse,
    ProjectsListResponse,
    Translation,
    TranslationKey,
    TranslationUpdate,
)
from app.services.lokalise import lokalise_service

router = APIRouter()


@router.get("/projects", response_model=ProjectsListResponse)
async def list_projects(
    response: Response,
    # Lokalise API parameters (mirroring their naming)
    filter_team_id: int | None = Query(None, description="Limit results to team ID"),
    filter_names: str | None = Query(
        None, description="One or more project names to filter by (comma separated)"
    ),
    include_statistics: int = Query(
        1,
        description="Whether to include project statistics. Possible values are 1 and 0",
    ),
    include_settings: int = Query(
        1,
        description="Whether to include project settings. Possible values are 1 and 0",
    ),
    limit: int | None = Query(
        None, description="Number of items to include (max 5000)", le=5000
    ),
    page: int | None = Query(
        None, description="Return results starting from this page", ge=1
    ),
):
    """
    List all projects available to the user.

    Mirrors Lokalise API structure: GET /projects
    Retrieves a list of projects available to the user, authorized with a token.
    Requires read_projects OAuth access scope.

    Args:
        filter_team_id: Limit results to team ID
        filter_names: One or more project names to filter by (comma separated)
        include_statistics: Whether to include project statistics (1 or 0)
        include_settings: Whether to include project settings (1 or 0)
        limit: Number of items to include (max 5000)
        page: Return results starting from this page

    Returns:
        ProjectsListResponse with projects array and total count
    """
    # Create filters object
    filters = ProjectFilters(
        filter_team_id=filter_team_id,
        filter_names=filter_names,
        include_statistics=include_statistics,
        include_settings=include_settings,
        limit=limit,
        page=page,
    )

    # Get projects from service
    projects_response = await lokalise_service.projects.list_projects(filters)

    # Add X-Total-Count header to match Lokalise API
    if projects_response.total_count is not None:
        response.headers["X-Total-Count"] = str(projects_response.total_count)

    return projects_response


@router.get("/system/languages", response_model=LanguagesListResponse)
async def list_languages(
    response: Response,
    # Lokalise API parameters (mirroring their naming)
    limit: int | None = Query(
        None, description="Number of items to include (max 5000)", le=5000
    ),
    page: int | None = Query(
        None, description="Return results starting from this page", ge=1
    ),
):
    """
    List all system languages available in Lokalise.

    Mirrors Lokalise API structure: GET /system/languages
    Retrieves a list of system languages available in Lokalise.
    Requires read_languages OAuth access scope.

    Args:
        limit: Number of items to include (max 5000)
        page: Return results starting from this page

    Returns:
        LanguagesListResponse with languages array and total count
    """
    # Create filters object
    filters = LanguageFilters(
        limit=limit,
        page=page,
    )

    # Get languages from service
    languages_response = await lokalise_service.languages.list_system_languages(filters)

    # Add X-Total-Count header to match Lokalise API
    if languages_response.total_count is not None:
        response.headers["X-Total-Count"] = str(languages_response.total_count)

    return languages_response


@router.get("/projects/{project_id}/languages", response_model=ProjectLanguagesResponse)
async def list_project_languages(
    project_id: str,
    response: Response,
    # Lokalise API parameters (mirroring their naming)
    limit: int | None = Query(
        None, description="Number of items to include (max 5000)", le=5000
    ),
    page: int | None = Query(
        None, description="Return results starting from this page", ge=1
    ),
):
    """
    List all languages for a specific project.

    Mirrors Lokalise API structure: GET /projects/{project_id}/languages
    Retrieves a list of project languages.
    Requires read_languages OAuth access scope.

    Args:
        project_id: A unique project identifier
        limit: Number of items to include (max 5000)
        page: Return results starting from this page

    Returns:
        ProjectLanguagesResponse with project_id and languages array
    """
    # Create filters object
    filters = ProjectLanguageFilters(
        limit=limit,
        page=page,
    )

    # Get project languages from service
    project_languages_response = (
        await lokalise_service.languages.list_project_languages(project_id, filters)
    )

    # Add X-Total-Count header for project languages (total based on languages count)
    # Note: Project languages endpoint doesn't return total_count, so we use the length
    response.headers["X-Total-Count"] = str(len(project_languages_response.languages))

    return project_languages_response


@router.get("/projects/{project_id}/keys", response_model=list[TranslationKey])
async def get_keys(
    project_id: str,
    # Core Lokalise API parameters (mirroring their naming)
    include_translations: int = Query(
        1, description="Whether to include translations. Possible values are 1 and 0"
    ),
    include_comments: int = Query(
        0, description="Whether to include comments. Possible values are 1 and 0"
    ),
    include_screenshots: int = Query(
        0,
        description="Whether to include URL to screenshots. Possible values are 1 and 0",
    ),
    # Filter parameters (matching Lokalise naming)
    filter_translation_lang_ids: str | None = Query(
        None, description="One or more language ID to filter by (comma separated)"
    ),
    filter_tags: str | None = Query(
        None, description="One or more tags to filter by (comma separated)"
    ),
    filter_platforms: str | None = Query(
        None,
        description="One or more platforms to filter by (comma separated). Possible values are ios, android, web and other",
    ),
    filter_untranslated: int = Query(
        0, description="Filter by untranslated keys. Possible values are 1 and 0"
    ),
    filter_archived: str = Query(
        "include",
        description="One archived filter. Possible values are include, exclude and only",
    ),
    filter_keys: str | None = Query(
        None, description="One or more key name to filter by (comma separated)"
    ),
    filter_key_ids: str | None = Query(
        None, description="One or more key identifiers to filter by (comma separated)"
    ),
    # Pagination (basic support)
    limit: int | None = Query(
        None, description="Number of items to include (max 500)", le=500
    ),
    page: int | None = Query(
        1, description="Return results starting from this page", ge=1
    ),
    # Custom extensions (not in original Lokalise API)
    reviewed_only: bool = Query(
        False, description="[Extension] Filter to show only reviewed translations"
    ),
):
    """
    Get keys for a specific project with filtering options.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/keys

    Args:
        project_id: A unique project identifier
        include_translations: Whether to include translations (1 or 0)
        include_comments: Whether to include comments (1 or 0)
        include_screenshots: Whether to include screenshots (1 or 0)
        filter_translation_lang_ids: Language IDs to filter by (comma separated)
        filter_tags: Tags to filter by (comma separated)
        filter_platforms: Platforms to filter by (comma separated: ios, android, web, other)
        filter_untranslated: Filter by untranslated keys (1 or 0)
        filter_archived: Archived filter (include, exclude, only)
        filter_keys: Key names to filter by (comma separated)
        filter_key_ids: Key identifiers to filter by (comma separated)
        limit: Number of items to include (max 500)
        page: Return results starting from this page
        reviewed_only: [Extension] Filter to show only reviewed translations

    Returns:
        List of keys with comprehensive translation status and metadata
    """
    # Convert Lokalise-style parameters to our internal format
    target_language = None
    if filter_translation_lang_ids:
        # For now, take the first language ID (could be extended to support multiple)
        target_language = filter_translation_lang_ids.split(",")[0].strip()

    untranslated_only = bool(filter_untranslated)

    # Parse comma-separated lists
    platform_list = filter_platforms.split(",") if filter_platforms else None
    tag_list = filter_tags.split(",") if filter_tags else None
    key_list = filter_keys.split(",") if filter_keys else None
    key_id_list = filter_key_ids.split(",") if filter_key_ids else None

    # Get keys from service
    # Now we can call the service with or without a target language
    all_keys = await lokalise_service.get_keys(
        project_id, target_language, untranslated_only
    )

    # Apply additional filters
    filtered_keys = []
    for key in all_keys:
        # Filter by archived status
        if filter_archived == "exclude" and key.is_archived:
            continue
        elif filter_archived == "only" and not key.is_archived:
            continue
        # "include" means no filtering by archived status

        # Filter by platforms
        if platform_list and not any(
            platform.strip() in key.platforms for platform in platform_list
        ):
            continue

        # Filter by tags
        if tag_list and not any(tag.strip() in key.tags for tag in tag_list):
            continue

        # Filter by key names
        if key_list:
            if isinstance(key.key_name, str):
                key_name_str = key.key_name
            else:
                key_name_str = (
                    key.key_name.web if key.key_name and key.key_name.web else ""
                )
            if not any(key_filter.strip() in key_name_str for key_filter in key_list):
                continue

        # Filter by key IDs
        if key_id_list and str(key.key_id) not in [kid.strip() for kid in key_id_list]:
            continue

        # Filter by review status (custom extension)
        if (
            reviewed_only
            and key.translation_metadata
            and not key.translation_metadata.is_reviewed
        ):
            continue

        filtered_keys.append(key)

    # Apply pagination
    if limit and page:
        start_index = (page - 1) * limit
        end_index = start_index + limit
        filtered_keys = filtered_keys[start_index:end_index]

    return filtered_keys


@router.post("/projects/{project_id}/keys", response_model=KeysCreateResponse)
async def create_keys(
    project_id: str,
    create_data: KeysCreate,
):
    """
    Create one or more keys in a project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/keys

    Creates one or more keys in the project. Requires Manage keys admin right.
    We recommend sending payload in chunks of up to 500 keys per request.
    Requires write_keys OAuth access scope.

    Args:
        project_id: A unique project identifier
        create_data: KeysCreate schema with the keys to create

    Returns:
        KeysCreateResponse with data array and meta information including creation statistics
    """
    # Create keys via service
    created_keys = await lokalise_service.create_keys(
        project_id=project_id,
        create_data=create_data,
    )

    return created_keys


@router.get("/projects/{project_id}/translations", response_model=list[Translation])
async def get_translations(
    project_id: str,
    # Lokalise API parameters (mirroring their naming)
    disable_references: int = Query(
        0, description="Whether to disable key references. Possible values are 1 and 0"
    ),
    filter_lang_id: int | None = Query(
        None, description="Return translations only for presented language ID"
    ),
    filter_is_reviewed: int | None = Query(
        None,
        description="Filter translations which are reviewed. Possible values are 1 and 0",
    ),
    filter_unverified: int | None = Query(
        None,
        description="Filter translations which are unverified. Possible values are 1 and 0",
    ),
    filter_untranslated: int | None = Query(
        None, description="Filter by untranslated keys. Possible values are 1 and 0"
    ),
    filter_qa_issues: str | None = Query(
        None,
        description="One or more QA issues to filter by (comma separated). Possible values: spelling_and_grammar, placeholders, html, url_count, url, email_count, email, brackets, numbers, leading_whitespace, trailing_whitespace, double_space, special_placeholder, unbalanced_brackets",
    ),
    filter_active_task_id: int | None = Query(
        None, description="Filter translations which are part of given task ID"
    ),
    # Pagination parameters
    pagination: str = Query(
        "offset",
        description="Type of pagination. Possible values are offset and cursor",
    ),
    limit: int = Query(
        100, description="Number of items to include (max 5000)", le=5000, ge=1
    ),
    page: int | None = Query(
        None, description="Return results starting from this page", ge=1
    ),
    cursor: str | None = Query(
        None, description="Return results starting from this cursor"
    ),
):
    """
    Get translations for a specific project with filtering options.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/translations

    Retrieves a list of project translation items, ungrouped.
    You may want to request Keys resource in order to get the structured key/translation pairs for all languages.

    Args:
        project_id: A unique project identifier
        disable_references: Whether to disable key references (1 or 0)
        filter_lang_id: Return translations only for presented language ID
        filter_is_reviewed: Filter translations which are reviewed (1 or 0)
        filter_unverified: Filter translations which are unverified (1 or 0)
        filter_untranslated: Filter by untranslated keys (1 or 0)
        filter_qa_issues: QA issues to filter by (comma separated)
        filter_active_task_id: Filter translations which are part of given task ID
        pagination: Type of pagination (offset or cursor)
        limit: Number of items to include (max 5000)
        page: Return results starting from this page
        cursor: Return results starting from this cursor

    Returns:
        List of ungrouped translation items with comprehensive metadata
    """
    # Convert Lokalise-style boolean parameters
    is_reviewed = None if filter_is_reviewed is None else bool(filter_is_reviewed)
    is_unverified = None if filter_unverified is None else bool(filter_unverified)
    is_untranslated = None if filter_untranslated is None else bool(filter_untranslated)

    # Get translations from service
    translations = await lokalise_service.get_translations(
        project_id=project_id,
        filter_lang_id=filter_lang_id,
        filter_is_reviewed=is_reviewed,
        filter_unverified=is_unverified,
        filter_untranslated=is_untranslated,
        filter_qa_issues=filter_qa_issues,
        filter_active_task_id=filter_active_task_id,
        limit=limit,
        page=page,
    )

    return translations


@router.get(
    "/projects/{project_id}/translations/{translation_id}", response_model=Translation
)
async def get_translation(
    project_id: str,
    translation_id: int,
    # Lokalise API parameters (mirroring their naming)
    disable_references: int = Query(
        0, description="Whether to disable key references. Possible values are 1 and 0"
    ),
):
    """
    Get a specific translation by ID for a project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/translations/{translation_id}

    Retrieves a Translation object.

    Args:
        project_id: A unique project identifier
        translation_id: Unique translation identifier
        disable_references: Whether to disable key references (1 or 0)

    Returns:
        Translation object with comprehensive metadata
    """
    # Convert Lokalise-style boolean parameter
    disable_refs = bool(disable_references)

    # Get translation from service
    translation = await lokalise_service.get_translation(
        project_id=project_id,
        translation_id=translation_id,
        disable_references=disable_refs,
    )

    return translation


@router.put(
    "/projects/{project_id}/translations/{translation_id}", response_model=Translation
)
async def update_translation(
    project_id: str,
    translation_id: int,
    update_data: TranslationUpdate,
):
    """
    Update a translation by ID for a project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/translations/{translation_id}

    Updates a translation. Alternatively, use the Multi-key update endpoint to update translations.

    Args:
        project_id: A unique project identifier
        translation_id: Unique translation identifier
        update_data: Translation update data including content and status flags

    Returns:
        Updated Translation object with comprehensive metadata
    """
    # Update translation via service
    updated_translation = await lokalise_service.update_translation(
        project_id=project_id,
        translation_id=translation_id,
        update_data=update_data,
    )

    return updated_translation


@router.get(
    "/projects/{project_id}/glossary-terms", response_model=GlossaryTermsResponse
)
async def get_glossary_terms(
    project_id: str,
    # Lokalise API parameters (mirroring their naming)
    limit: int | None = Query(
        None, description="Number of items to include (max 500)", le=500
    ),
    cursor: int | None = Query(
        None, description="Return results starting from this cursor"
    ),
):
    """
    Get glossary terms for a specific project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/glossary-terms

    Retrieves a list of glossary terms.
    Requires read_glossary OAuth access scope.

    Args:
        project_id: A unique project identifier
        limit: Number of items to include (max 500)
        cursor: Return results starting from this cursor

    Returns:
        List of glossary terms with comprehensive metadata
    """
    # Get glossary terms from service
    glossary_terms = await lokalise_service.get_glossary_terms(
        project_id=project_id,
        limit=limit,
        cursor=cursor,
    )

    return glossary_terms


@router.get(
    "/projects/{project_id}/glossary-terms/{term_id}",
    response_model=GlossaryTermResponse,
)
async def get_glossary_term(
    project_id: str,
    term_id: int,
):
    """
    Get a specific glossary term by ID for a project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/glossary-terms/{term_id}

    Retrieves a Glossary Term object wrapped in data structure.
    Requires read_glossary OAuth access scope.

    Args:
        project_id: A unique project identifier
        term_id: A unique glossary term identifier

    Returns:
        GlossaryTermResponse with data object containing the glossary term
    """
    # Get glossary term from service
    glossary_term = await lokalise_service.get_glossary_term(
        project_id=project_id,
        term_id=term_id,
    )

    return glossary_term


@router.post(
    "/projects/{project_id}/glossary-terms", response_model=GlossaryTermsCreateResponse
)
async def create_glossary_terms(
    project_id: str,
    create_data: GlossaryTermsCreate,
):
    """
    Create one or more glossary terms in a project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/glossary-terms

    Creates one or more glossary terms in the project.
    Requires Manage glossary admin right.
    Requires write_glossary OAuth access scope.

    Args:
        project_id: A unique project identifier
        create_data: GlossaryTermsCreate schema with the terms to create

    Returns:
        GlossaryTermsCreateResponse with data array and meta information including creation statistics
    """
    # Create glossary terms via service
    created_terms = await lokalise_service.create_glossary_terms(
        project_id=project_id,
        create_data=create_data,
    )

    return created_terms


@router.put(
    "/projects/{project_id}/glossary-terms", response_model=GlossaryTermsUpdateResponse
)
async def update_glossary_terms(
    project_id: str,
    update_data: GlossaryTermsUpdate,
):
    """
    Update one or more glossary terms in a project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/glossary-terms

    Updates one or more glossary terms in the project.
    Requires Manage glossary admin right.
    Requires write_glossary OAuth access scope.

    Args:
        project_id: A unique project identifier
        update_data: GlossaryTermsUpdate schema with the terms to update

    Returns:
        GlossaryTermsUpdateResponse with data array and meta information including update statistics
    """
    # Update glossary terms via service
    updated_terms = await lokalise_service.update_glossary_terms(
        project_id=project_id,
        update_data=update_data,
    )

    return updated_terms


@router.delete(
    "/projects/{project_id}/glossary-terms", response_model=GlossaryTermsDeleteResponse
)
async def delete_glossary_terms(
    project_id: str,
    delete_data: GlossaryTermsDelete,
):
    """
    Delete glossary terms from a project.

    Mirrors Lokalise API structure and parameters: /projects/{project_id}/glossary-terms

    Deletes all specified glossary terms from the project.
    Requires Manage glossary admin right.
    Requires write_glossary OAuth access scope.

    Args:
        project_id: A unique project identifier
        delete_data: GlossaryTermsDelete schema with list of term IDs to delete

    Returns:
        GlossaryTermsDeleteResponse with data object containing deleted and failed information
    """
    # Delete glossary terms via service
    result = await lokalise_service.delete_glossary_terms(
        project_id=project_id,
        delete_data=delete_data,
    )

    return result
