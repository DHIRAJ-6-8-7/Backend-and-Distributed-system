from sqlalchemy import URL, create_engine, select, func
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.models import Task

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    port=settings.db_port,
    database=settings.db_name,
    host=settings.db_host,
)

engine = create_engine(
    database_url,
    pool_size=20,
    max_overflow=10,
    pool_timeout=15,
    pool_recycle=1800,
)
SessionLocal = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)


def get_db():
    with SessionLocal() as session:
        yield session


def list_tasks_from_db(
    session: Session,
    limit: int,
    offset: int,
    completed: bool | None,
    age: int | None,
    sort: str,
):
    conditions = []
    if completed is not None:
        conditions.append(Task.completed == completed)

    if age is not None:
        conditions.append(Task.age == age)

    descending = sort.startswith("-")
    sort_field = sort[1:] if descending else sort

    ALLOWED_SORT_FIELDS = {"id", "title", "age"}

    sort_field = sort[1:] if descending else sort

    if sort_field not in ALLOWED_SORT_FIELDS:
        raise ValueError(f"Invalid sort field: {sort_field}")

    sort_column = getattr(Task, sort_field)

    if descending:
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    page_query = (
        select(Task)
        .where(*conditions)
        .order_by(sort_column)
        .limit(limit)
        .offset(offset)
    )
    count_query = select(func.count()).select_from(Task).where(*conditions)
    items = session.execute(page_query).scalars().all()
    total = session.execute(count_query).scalar_one()

    return {"items": items, "limit": limit, "offset": offset, "total": total}


# get with id orm implementation
def get_task_from_db(session: Session, task_id: int):
    statement = select(Task).where(Task.id == task_id)
    task = session.execute(statement).scalar_one_or_none()
    return task


# for post orm implementation
def post_task(session: Session, title: str, completed: bool, age: int):
    try:
        task = Task(title=title, completed=completed, age=age)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except Exception:
        session.rollback()
        raise


# patch orm implementation
def patch_task_in_db(session: Session, task_id: int, update: dict):
    allowed_fields = {"title", "completed", "age"}
    task = session.get(Task, task_id)
    if task is None:
        return None
    if not update:
        raise ValueError("At least one field must be provided")
    for field, value in update.items():
        if field not in allowed_fields:
            raise ValueError(f"Invalid field: {field}")
        if value is None:
            raise ValueError(f"{field} cannot be null")
        setattr(task, field, value)
    session.commit()
    session.refresh(task)
    return task


# put orm implementation
def replace_task_in_db(session: Session, task_id: int, body: dict):
    allowed_fields = {"title", "completed", "age"}

    if set(body) != allowed_fields:
        raise ValueError("Put requires title, completed, age")
    task = session.get(Task, task_id)
    if task is None:
        return None
    task.title = body["title"]
    task.completed = body["completed"]
    task.age = body["age"]
    session.commit()
    return task


# delete orm implementation
def delete_task_from_db(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if task is None:
        return False
    session.delete(task)
    session.commit()
    return True


# for post core implementation
# def post_task(title: str, completed: bool, age: int):
#     with engine.begin() as connection:
#         result = connection.execute(
#             text(f"""
#                 INSERT INTO tasks (
#                     title,
#                     completed,
#                     age
#                 )
#                 VALUES (
#                     :title,
#                     :completed,
#                     :age
#                 )
#                 RETURNING id, title, completed, age;
#                 """),
#             {"title": title, "completed": completed, "age": age},
#         )
#         return dict(result.mappings().one())

# get with id core implementation
# def get_task_from_db(task_id: int):
#     with engine.connect() as connection:
#         result = connection.execute(
#             text("""
#                     SELECT id, title, completed, age
#                     FROM tasks
#                     WHERE id = :task_id
#             """),
#             {"task_id": task_id},
#         )
#         row = result.mappings().one_or_none()
#     return dict(row) if row else None

# patch core implementation
# def patch_task_in_db(task_id: int, update: dict):
#     allowed_field = {"completed", "age", "title"}

#     if not set(update).issubset(allowed_field):
#         raise ValueError("Invalid task field")

#     if not update:
#         return get_task_from_db(task_id)

#     if any(value is None for value in update.values()):
#         raise ValueError("Task fields cannot be null")

#     set_clause = ", ".join(f"{field}= :{field}" for field in update)

#     params = {**update, "task_id": task_id}

#     with engine.begin() as connection:
#         result = connection.execute(
#             text(f"""
#                     UPDATE tasks
#                     SET {set_clause}
#                     WHERE id = :task_id
#                     RETURNING id, title, completed, age
#             """),
#             params,
#         )
#         row = result.mappings().one_or_none()
#     return dict(row) if row else None

# put core implementation
# def replace_task_in_db(task_id: int, body: dict):
#     allowed_fields = {"title", "completed", "age"}

#     if set(body) != allowed_fields:
#         raise ValueError("Put requires title, completed, age")

#     put_clause = ", ".join(f"{field} = :{field}" for field in body)

#     params = {**body, "task_id": task_id}
#     with engine.begin() as connection:
#         result = connection.execute(
#             text(f"""
#                     UPDATE tasks
#                     SET {put_clause}
#                     WHERE id = :task_id
#                     RETURNING id, title, completed, age
#             """),
#             params,
#         )
#         row = result.mappings().one_or_none()
#     return dict(row) if row else None

# delete core implementation
# def delete_task_from_db(task_id: int):
#     with engine.begin() as connection:
#         result = connection.execute(
#             text("""
#                     DELETE FROM tasks
#                     WHERE id = :task_id
#                     RETURNING id
#             """),
#             {"task_id": task_id},
#         )
#         deleted_row = result.first()
#     return deleted_row is not None
