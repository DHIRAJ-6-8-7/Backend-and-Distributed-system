from sqlalchemy import text
from app.database import engine

def test_engine_uses_test_database():
    with engine.connect() as connection:
        database_name=connection.execute(
            text("SELECT current_database()")
        ).scalar_one()
        assert database_name == "taskflow_test"
