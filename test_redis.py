from app.redis_client import redis_client

try:
    print("Redis connection:", redis_client.ping())

    redis_client.set("taskflow:test", "Redis is working", ex=60)

    result = redis_client.get("taskflow:test")

    print("Stored value:", result)

finally:
    redis_client.delete("taskflow:test")
    redis_client.close()
