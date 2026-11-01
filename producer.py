import json
from app.rabbitmq_client import create_rabbitmq_channel


def publish_task(task_id: int, operation: str):
    connection, channel = create_rabbitmq_channel()

    try:
        channel.queue_declare(queue="task_queue", durable=True)

        message = {"task_id": task_id, "operation": operation}

        channel.basic_publish(
            exchange="", routing_key="task_queue", body=json.dumps(message)
        )

        print(f"Published task: {message}")
    finally:
        connection.close()


if __name__ == "__main__":
    publish_task(task_id=11, operation="generate_report")
