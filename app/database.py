import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
load_dotenv()

database_host=os.getenv("DB_HOST")
database_port=int(os.getenv("DB_PORT"))
database_user=os.getenv("DB_USER")
database_name=os.getenv("DB_NAME")
database_password=os.getenv("DB_PASSWORD")

database_url=URL.create(
    drivername="postgresql+psycopg",
    host=database_host,
    username=database_user,
    password=database_password,
    port=database_port,
    database=database_name
)
engine=create_engine(database_url)

#for post
def post_task(
        title: str,
        completed: bool,
        age: int
):
    with engine.begin() as connection:
        result=connection.execute(
            text(
                f"""
                INSERT INTO tasks (
                    title,
                    completed,
                    age
                )
                VALUES (
                    :title,
                    :completed,
                    :age
                )
                RETURNING id, title, completed, age;
                """
            ),
            {
                "title": title,
                "completed": completed,
                "age": age
            }
        )
        return dict(
            result.mappings().one()
        )

def list_tasks_from_db(
        limit: int,
        offset: int,
        completed: bool | None,
        age: int | None,
        sort: str
):
    conditions=[]
    params={}
    if completed is not None:
        conditions.append("completed = :completed")
        params["completed"]=completed

    if age is not None:
        conditions.append("age = :age")
        params["age"]=age

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    else:
        where_clause=""

    descending = sort.startswith("-")
    sort_field = sort[1:] if descending else sort

    direction = "DESC" if descending else "ASC"
    ALLOWED_SORT_FIELDS = {"id", "title", "age"}

    sort_field = sort[1:] if descending else sort

    if sort_field not in ALLOWED_SORT_FIELDS:
        raise ValueError(f"Invalid sort field: {sort_field}")

    page_query = text(f"""
                SELECT id, title, completed, age
                FROM tasks
                {where_clause}
                ORDER BY {sort_field} {direction}
                LIMIT :limit
                OFFSET :offset;
            """)

    count_query = text(f"""
        SELECT COUNT(*)
        FROM tasks
        {where_clause};
        """)

    filter_params = params.copy()

    params.update(
        {
            "limit": limit,
            "offset": offset
        }
    )

    with engine.connect() as connection:
        result = connection.execute(
            page_query,
            params
        )
        items=[dict(row) for row in result.mappings().all()]
        count_result = connection.execute(
            count_query,
            filter_params
        )
        total=count_result.scalar_one()
    return {
        "items": items,
        "limit": limit,
        "offset": offset,
        "total": total
    }

#get with id
def get_task_from_db(task_id: int):
    with engine.connect() as connection:
        result=connection.execute(
            text("""
                    SELECT id, title, completed, age
                    FROM tasks
                    WHERE id = :task_id
            """),
            {
                "task_id": task_id
            }
        )
        row=result.mappings().one_or_none()
    return dict(row) if row else None

#patch
def patch_task_in_db(
        task_id: int,
        update: dict
):
    allowed_field = {
        "completed",
        "age",
        "title"
    }

    if not set(update).issubset(allowed_field):
        raise ValueError("Invalid task field")

    if not update:
        return get_task_from_db(task_id)

    if any(value is None for value in update.values()):
        raise ValueError("Task fields cannot be null")

    set_clause = ", ".join(
        f"{field}= :{field}" for field in update
    )

    params = {**update, "task_id": task_id}

    with engine.begin() as connection:
        result = connection.execute(
            text(f"""
                    UPDATE tasks
                    SET {set_clause}
                    WHERE id = :task_id
                    RETURNING id, title, completed, age
            """),
            params
        )
        row = result.mappings().one_or_none()
    return dict(row) if row else None

#put
def replace_task_in_db(
        task_id: int,
        body: dict
):
    allowed_fields = {"title", "completed", "age"}

    if set(body) != allowed_fields:
        raise ValueError("Put requires title, completed, age")

    put_clause = ", ".join(
        f"{field} = :{field}" for field in body
    )

    params={**body, "task_id": task_id}
    with engine.begin() as connection:
        result = connection.execute(
            text(f"""
                    UPDATE tasks
                    SET {put_clause}
                    WHERE id = :task_id
                    RETURNING id, title, completed, age
            """),
            params
        )
        row = result.mappings().one_or_none()
    return dict(row) if row else None

def delete_task_from_db(task_id: int):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                    DELETE FROM tasks
                    WHERE id = :task_id
                    RETURNING id
            """),
            {
                "task_id": task_id
            }
        )
        deleted_row = result.first()
    return deleted_row is not None
