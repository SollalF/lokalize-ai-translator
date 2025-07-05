from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.lokalise.tasks import (
    ProjectTaskResponse,
    ProjectTasksResponse,
    TaskCreateRequest,
    TaskDeleteResponse,
    TaskUpdateRequest,
)

router = APIRouter(tags=["lokalise-tasks"])


@router.get("/tasks", response_model=ProjectTasksResponse)
async def list_project_tasks(
    response: Response,
    project_id: str = Path(..., description="A unique project identifier"),
    filter_title: str | None = Query(None, description="Set title filter for the list"),
    filter_statuses: str | None = Query(
        None,
        description="One or more task statuses to filter by (comma separated). Possible values are created, queued, in_progress and completed",
    ),
    limit: int | None = Query(
        100, ge=1, le=5000, description="Number of items to include (max 5000)"
    ),
    page: int | None = Query(
        1, ge=1, description="Return results starting from this page"
    ),
):
    """List all tasks in the project.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/tasks

    Requires read_tasks OAuth access scope.
    """
    # Set X-Total-Count header based on results (placeholder)
    response.headers["X-Total-Count"] = "0"

    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/tasks/{task_id}", response_model=ProjectTaskResponse)
async def get_project_task(
    project_id: str = Path(..., description="A unique project identifier"),
    task_id: int = Path(..., description="A unique task identifier"),
):
    """Retrieve a Task object.

    Mirrors Lokalise API endpoint:
    GET https://api.lokalise.com/api2/projects/{project_id}/tasks/{task_id}

    Requires read_tasks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/tasks/{task_id}", response_model=ProjectTaskResponse)
async def update_project_task(
    project_id: str = Path(..., description="A unique project identifier"),
    task_id: int = Path(..., description="A unique task identifier"),
    request: TaskUpdateRequest = ...,
):
    """Update the properties of a task.

    Mirrors Lokalise API endpoint:
    PUT https://api.lokalise.com/api2/projects/{project_id}/tasks/{task_id}

    Updates the properties of a task. Requires Manage tasks admin right.

    Requires write_tasks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/tasks/{task_id}", response_model=TaskDeleteResponse)
async def delete_project_task(
    project_id: str = Path(..., description="A unique project identifier"),
    task_id: int = Path(..., description="A unique task identifier"),
):
    """Delete a task from the project.

    Mirrors Lokalise API endpoint:
    DELETE https://api.lokalise.com/api2/projects/{project_id}/tasks/{task_id}

    Deletes a task from the project. Requires Manage tasks admin right.

    Requires write_tasks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/tasks", response_model=ProjectTaskResponse, status_code=200)
async def create_project_task(
    project_id: str = Path(..., description="A unique project identifier"),
    request: TaskCreateRequest = ...,
):
    """Create a task in the project.

    Mirrors Lokalise API endpoint:
    POST https://api.lokalise.com/api2/projects/{project_id}/tasks

    Creates a task in the project. Requires Manage tasks admin right.
    Keep in mind, that initial_tm_leverage attribute will be empty in server response.
    It's being calculated after the task is created and this process may take some time.

    Requires write_tasks OAuth access scope.
    """
    # TODO: implement service call when services are ready
    raise HTTPException(status_code=501, detail="Not implemented")
