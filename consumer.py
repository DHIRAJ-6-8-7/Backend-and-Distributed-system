import pika
import json
import sys

from app.rabbitmq_client import create_rabbitmq_channel
from app.database import SessionLocal, claim_task
from app.services.task_service import process_task


def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
        task_id = int(message["task_id"])

        with SessionLocal() as db:
            claimed = claim_task(db, task_id)

            if not claimed:
                print(f"Task {task_id} already claimed or unavailable")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            process_task(db, task_id)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as error:
        print(f"Processing failed: {error}")
        # Ensure we don't crash the channel if basic_nack fails due to a closed connection
        try:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as nack_error:
            print(f"Failed to nack message: {nack_error}")


def start_consumer():
    connection, channel = create_rabbitmq_channel()

    channel.queue_declare(queue="task_queue", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue="task_queue", on_message_callback=callback, auto_ack=False
    )

    print("Waiting for tasks. To exit press CTRL+C")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nStopping consumer gracefully...")
        try:
            # Gracefully stop consuming and close connections
            channel.stop_consuming()
        except Exception:
            pass
        finally:
            if channel.is_open:
                channel.close()
            if connection.is_open:
                connection.close()
        print("Consumer stopped successfully.")


if __name__ == "__main__":
    start_consumer()
