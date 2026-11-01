import json
import pika

from app.rabbitmq_client import create_rabbitmq_channel


def publish_task_message(task_id: int):
    connection, channel = create_rabbitmq_channel()

    try:
        channel.queue_declare(queue="task_queue", durable=True)

        channel.confirm_delivery()

        message = {"task_id": task_id}

        channel.basic_publish(
            exchange="",
            routing_key="task_queue",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                content_type="application/json", delivery_mode=2
            ),
            mandatory=True,
        )
        return message

    finally:
        if connection.is_open:
            connection.close()
