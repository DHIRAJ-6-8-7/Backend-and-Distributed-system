import json
from mypy.cache import Value
import redis
from typer import TyperException

from app.redis_client import redis_client


def set_cache(key: str, value: dict, ttl: int = 300) -> bool:
    try:
        serialized_value = json.dumps(value)
        redis_client.set(
            name = key,
            value = serialized_value,
            ex = ttl
        )
        return True
    except (redis.RedisError, TypeError, ValueError):
        return False

def get_cache(key: str) -> dict | None:
    try:
        cached_value = redis_client.get(key)
        if cached_value is None:
            return None
        return json.loads(cached_value)
    except (redis.RedisError, TypeError, ValueError):
        return None

def delete_cache(key: str) -> bool:
    try:
        redis_client.delete(key)
        return True
    except redis.RedisError:
        return False
