from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent  # app/ -> taskflow/


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    redis_url: str = "redis://localhost:6379/0"

    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/%2F"


settings = Settings()  # type: ignore
