from ast import Lambda
from asyncio import all_tasks

from charset_normalizer.cli import query_yes_no
from fastapi import FastAPI, HTTPException, Path, Query

from app.models.task import CreatedTaskVerify, ResponseTaskVerify, UpdateTaskVerify

app = FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.1")

tasks = {
    1: {"id": 1, "title": "Complete the FastAPI project", "completed": False, "age": 25},
    2: {"id": 2, "title": "Write unit tests", "completed": True, "age": 19},
    7: {"id": 7, "title": "task 7 have that things to do", "completed": False, "age": 30},
}

def task_not_found(task_id: int):
    raise HTTPException(
        status_code=404,
        detail={
            "error": {
                "code": "TASK NOT FOUND",
                "message": f"Task with id: {task_id} not found",
                "status": 404
            }
        }
    )

def task_already_exist(task_id: int):
    raise HTTPException(
        status_code=409,
        detail={
            "error": {
                "code": "TASK ALREADY EXIST",
                "message": f"Task with id: {task_id} already exist",
                "status": 409
            }
        }
    )

#GET with Pagination, Filtering ,and Sorting

@app.get("/api/v1/tasks")
def list_tasks(
    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    offset: int = Query(
        default=0,
        ge=0
    ),
    completed: bool | None = Query(
        default=None
        ),
    age: int | None = Query(
        default=None,
        ge=1,
        le=100
        ),
    sort: str = Query(
        default="id"
    )
):
    all_tasks=list(tasks.values())
    if completed is not None:
        all_tasks = [
            task for task in all_tasks
            if task["completed"] == completed
        ]

    if age is not None:
        all_tasks = [
            task for task in all_tasks
            if task["age"] == age
        ]
    #return true if - is at first
    descending=sort.startswith("-")

    if descending:
        sorting_attribute=sort[1:]
    else:
        sorting_attribute=sort

    allowed_fields={
        "id",
        "title",
        "age"
    }

    if sorting_attribute not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "BAD REQUEST",
                    "message": "Invalid Sort Field",
                    "status": 400
                }
            }
        )

    all_tasks.sort(
        key = lambda task: (
            task[sorting_attribute],
            task["id"]
            ),
        reverse=descending
        )
    total = len(all_tasks)
    items = all_tasks[offset : offset + limit]
    return {
        "items": items,
        "limit": limit,
        "offset": offset,
        "total": total
    }

#GET Method
@app.get("/api/v1/tasks/{task_id}", response_model= ResponseTaskVerify)
def get_task(task_id: int = Path(ge=1, le=100)):
    existing_task=tasks.get(task_id)
    if existing_task is None:
        task_not_found(task_id)
    return existing_task

#POST Method
@app.post("/tasks/{task_id}",
        response_model=ResponseTaskVerify,
        status_code=201
        )
def create_task(
        body: CreatedTaskVerify,
        task_id: int = Path(ge=1, le=1000)
        ):
        if task_id in tasks:
            task_already_exist(task_id)
        new_task={
            "id": task_id,
            **body.model_dump()
        }
        tasks[task_id]=new_task
        return new_task

#Patch Method
@app.patch("/api/v1/tasks/{task_id}", response_model = ResponseTaskVerify)
def update_task(
    update: UpdateTaskVerify,
    task_id: int = Path(ge=1,le=100)
):
    existing_task = tasks.get(task_id)
    if existing_task is None:
        task_not_found(task_id)

    changed_field_selection = update.model_dump(exclude_unset=True)

    existing_task.update(changed_field_selection)
    return existing_task

@app.put("/api/v1/tasks/{task_id}", response_model= ResponseTaskVerify)
def replace_task(
    body: CreatedTaskVerify,
    task_id: int = Path(ge=1, le=100)
):
    existing_task = tasks.get(task_id)
    if existing_task is None:
        task_not_found(task_id)
    tasks[task_id]={
        "id": task_id,
        **body.model_dump()
        }
    return tasks[task_id]

#delete method
@app.delete("/api/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int = Path(ge=1,le=100)):
    existing_task=tasks.get(task_id)
    if existing_task is None:
        task_not_found(task_id)
    del tasks[task_id]
