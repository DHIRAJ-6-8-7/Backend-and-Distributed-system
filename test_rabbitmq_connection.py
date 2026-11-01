from app.rabbitmq_client import create_rabbitmq_channel

connection, channel = create_rabbitmq_channel()

print("Connection open:", connection.is_open)
print("Channel open:", channel.is_open)

channel.close()
connection.close()

print("Channel closed:", channel.is_closed)
print("Connection closed:", connection.is_closed)
