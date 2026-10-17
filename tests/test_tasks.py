from email import errors
from inspect import cleandoc
from turtle import title
from urllib import response

from fastapi.testclient import TestClient
from idna import cli
from urllib3 import Retry
from app.models import task
from sqlalchemy import text

from app.main import app
from app.database import engine

client = TestClient(app)

BASE_URL = "/api/v1/tasks"

#create valid task for payload test
def make_task(**overrides):
    task_data = {
        "title": "backend testing for post operation",
        "completed": False,
        "age": 22
    }
    task_data.update(overrides)
    return task_data

#create task through the api
def create_task(**overrides):
    response = client.post(
        BASE_URL,
        json = make_task(**overrides)
    )
    assert response.status_code == 201, response.text
    return response.json()

def test_create_task():
    task_data = make_task(completed = True, age = 25)

    response = client.post(
        BASE_URL,
        json = task_data
    )

    assert response.status_code == 201

    created_task = response.json()

    assert created_task["id"] > 0
    assert created_task["title"] == task_data["title"]
    assert created_task["completed"] == task_data["completed"]
    assert created_task["age"] == task_data["age"]

    with engine.connect() as connection:
        stored_task = connection.execute(
            text("""
                    SELECT id, title, completed, age
                    FROM tasks
                    WHERE id = :task_id
            """),
            {
                "task_id": created_task["id"]
            }
        ).mappings().one_or_none()

    assert stored_task is not None
    assert stored_task["title"] == task_data["title"]
    assert stored_task["completed"] == task_data["completed"]
    assert stored_task["age"] == task_data["age"]

def test_short_title():
    response = client.post(
        BASE_URL,
        json=make_task(title="short")
    )

    assert response.status_code == 422

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                    SELECT COUNT(*)
                    FROM tasks
                    WHERE title= :title
            """),
            {
                "title": "short"
            }
        ).scalar_one()

    assert result == 0

def test_missing_title():
    response = client.post(
        BASE_URL,
        json = {
            "completed": False,
            "age": 99
        }
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert any(
        error["loc"][-1] == "title"
        and error["type"] == "missing"
        for error in errors
    )

def test_invalid_age_is_rejected():
    response = client.post(
        BASE_URL,
        json = make_task(age = 12)
    )

    assert response.status_code == 422

def test_get_task():
    created = create_task( complete = True, age = 99)
    response = client.get(
        f"{BASE_URL}/{created["id"]}"
    )

    assert response.status_code == 200

    task = response.json()

    assert task["id"] == created["id"]
    assert task["title"] == created["title"]
    assert task["completed"] == created["completed"]
    assert task["age"] == created["age"]

def test_get_nonexistent_task_return_404():
    response = client.get(
        f"{BASE_URL}/992932"
    )

    assert response.status_code == 404

def task_with_non_integer_id_return_422():
    response = client.get(
        f"{BASE_URL}/not-integer"
    )

    assert response.status_code == 422

def test_list_all_task():
    first = create_task(
        title = "dhiraj is handsome boy"
    )
    second = create_task(
        title = "shrestha are handsomer",
        age = 19
    )

    response = client.get(BASE_URL)

    assert response.status_code == 200
    body = response.json()

    assert body["total"] == 2
    assert body["limit"] >= 2
    assert body["offset"] == 0

    returned_ids = {task["id"] for task in body["items"]}
    assert returned_ids == {
        first["id"], second["id"]
    }

def test_filter_completed_task():
    completed_task = create_task(
        title = "completed testing",
        age = 89
    )

    create_task(
        title = "pending testing",
        age = 20
    )

    response = client.get(
        BASE_URL,
        params={
            "age": 89
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == completed_task["id"]
    assert body["items"][0]["age"] == 89

def test_sort_by_id_descending():
    first = create_task (
        title = "first task is heavy",
        completed = True
    )

    second = create_task (
        title = "second task is moderate"
    )

    third = create_task (
        title = "third task is light",
        age = 22
    )

    response = client.get(
        BASE_URL,
        params={
            "sort": "-id"
        }
    )

    assert response.status_code == 200
    items = response.json()["items"]

    assert [task["id"] for task in items] == [
        third["id"],
        second["id"],
        first["id"]
    ]

def test_offset_and_limit():
    first = create_task (
        title = "first task is heavy",
        completed = True
    )

    second = create_task (
        title = "second task is moderate"
    )

    third = create_task (
        title = "third task is light",
        age = 22
    )

    response = client.get(
        BASE_URL,
        params={
            "sort": "-id",
            "limit": 1,
            "offset": 1
        }
    )

    assert response.status_code == 200
    body = response.json()

    assert body["total"] == 3
    assert body["limit"] == 1
    assert body["offset"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == second["id"]

def test_patch_updates_only_selected_field():
    created = create_task(
        title="Preserve the task title",
        completed=False,
        age=30,
    )

    response = client.patch(
        f"{BASE_URL}/{created['id']}",
        json={"completed": True},
    )

    assert response.status_code == 200
    task = response.json()

    assert task["id"] == created["id"]
    assert task["completed"] is True
    assert task["title"] == "Preserve the task title"
    assert task["age"] == 30


def test_patch_nonexistent_task_returns_404():
    response = client.patch(
        f"{BASE_URL}/99999999",
        json={"completed": True},
    )

    assert response.status_code == 404


def test_put_replaces_task():
    created = create_task(
        title="Original testing task",
        completed=False,
        age=25,
    )

    replacement = {
        "title": "Replacement testing task",
        "completed": True,
        "age": 40,
    }

    response = client.put(
        f"{BASE_URL}/{created['id']}",
        json=replacement,
    )

    assert response.status_code == 200
    task = response.json()

    assert task["id"] == created["id"]
    assert task["title"] == replacement["title"]
    assert task["completed"] is True
    assert task["age"] == 40


def test_put_nonexistent_task_returns_404():
    response = client.put(
        f"{BASE_URL}/99999999",
        json=make_task(),
    )

    assert response.status_code == 404


def test_delete_task():
    created = create_task()

    response = client.delete(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""

    follow_up = client.get(f"{BASE_URL}/{created['id']}")
    assert follow_up.status_code == 404


def test_delete_nonexistent_task_returns_404():
    response = client.delete(f"{BASE_URL}/99999999")

    assert response.status_code == 404
