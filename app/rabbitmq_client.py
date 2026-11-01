import pika

from app.config import settings


def create_rabbitmq_connection():
    parameters = pika.URLParameters(settings.rabbitmq_url)

    connection = pika.BlockingConnection(parameters)

    return connection


def create_rabbitmq_channel():
    connection = create_rabbitmq_connection()

    channel = connection.channel()

    return connection, channel
