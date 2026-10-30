from fastapi import FastAPI, HTTPException, Path, Query, Response, Depends
from app.services.cache_service import get_cache, set_cache, delete_cache
from app.models.task import (
    CreatedTaskVerify,
    ResponseTaskVerify,
    UpdateTaskVerify,
    TaskListResponseVerify,
)
from app.database import (
    post_task,
    list_tasks_from_db,
    get_task_from_db,
    patch_task_in_db,
    replace_task_in_db,
    delete_task_from_db,
    get_db,
)
from sqlalchemy.orm import Session

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.1",
)


def task_not_found(task_id: int):
    raise HTTPException(
        status_code=404,
        detail={
            "error": {
                "code": "TASK NOT FOUND",
                "message": f"Task with id: {task_id} not found",
                "status": 404,
            }
        },
    )


# GET with Pagination, Filtering ,and Sorting


@app.get("/api/v1/tasks", response_model=TaskListResponseVerify)
def list_tasks(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    completed: bool | None = Query(default=None),
    age: int | None = Query(default=None, ge=18, le=100),
    sort: str = Query(default="id"),
    db: Session = Depends(get_db),
):
    descending = sort.startswith("-")
    sort_field = sort[1:] if descending else sort

    allowed_field = {"id", "title", "age"}

    if sort_field not in allowed_field:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "BAD REQUEST",
                    "message": "Invalid sort field",
                    "status": 400,
                }
            },
        )
    return list_tasks_from_db(db, limit, offset, completed, age, sort)


# GET Method WITH ID
@app.get("/api/v1/tasks/{task_id}", response_model=ResponseTaskVerify)
def get_task(task_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cache_key = f"task:{task_id}"
    cached_task = get_cache(cache_key)
    # Cache hit
    if cached_task is not None:
        return cached_task
    existing_task = get_task_from_db(db, task_id)
    if existing_task is None:
        task_not_found(task_id)
    task_data = ResponseTaskVerify.model_validate(existing_task).model_dump()
    set_cache(cache_key, task_data, ttl=300)
    return existing_task


# POST Method
@app.post("/api/v1/tasks", response_model=ResponseTaskVerify, status_code=201)
def create_task(body: CreatedTaskVerify, db: Session = Depends(get_db)):
    result = post_task(db, **body.model_dump())
    return result


# PATCH Method
@app.patch("/api/v1/tasks/{task_id}", response_model=ResponseTaskVerify)
def update_task(
    update: UpdateTaskVerify, task_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    changed_field_selection = update.model_dump(exclude_unset=True)

    try:
        task = patch_task_in_db(db, task_id, changed_field_selection)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {"code": "BAD REQUEST", "message": str(exc), "status": 400}
            },
        ) from exc
    if task is None:
        task_not_found(task_id)
    cache_key = f"task:{task_id}"
    delete_cache(cache_key)
    return task


# PUT method
@app.put("/api/v1/tasks/{task_id}", response_model=ResponseTaskVerify)
def replace_task(
    body: CreatedTaskVerify, task_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    try:
        task = replace_task_in_db(db, task_id, body.model_dump())
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {"code": "BAD REQUEST", "message": str(exc), "status": 400}
            },
        ) from exc

    if task is None:
        task_not_found(task_id)

    cached_key = f"task:{task_id}"
    delete_cache(cached_key)

    return task


# DELETE method
@app.delete("/api/v1/tasks/{task_id}")
def delete_task(task_id: int = Path(ge=1), db: Session = Depends(get_db)):
    deleted_task = delete_task_from_db(db, task_id)
    if not deleted_task:
        task_not_found(task_id)

    cached_key = f"task:{task_id}"
    delete_cache(cached_key)

    return Response(status_code=204)
