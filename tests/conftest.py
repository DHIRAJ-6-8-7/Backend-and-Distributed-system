import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

# Override the database name for this pytest process only.
os.environ["DB_NAME"] = "taskflow_test"

from app.database import engine

def verify_test_database():
    with engine.connect() as connection:
        database_name = connection.execute(
            text(
                "SELECT current_database()"
            )
        ).scalar_one()

    if database_name != "taskflow_test":
        raise RuntimeError(
            f"unsafe test database: {database_name}"
        )

def clear_test_task():
    verify_test_database()

    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE tasks RESTART IDENTITY")
        )

@pytest.fixture(autouse=True)
def isolate_test_environment():
    clear_test_task()
    yield
    clear_test_task()
