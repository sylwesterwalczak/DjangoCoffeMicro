import json
import pika

credentials = pika.PlainCredentials('myuser', 'mypassword')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq3',
        heartbeat=600,
        blocked_connection_timeout=300,
        credentials=credentials
    )
)
channel = connection.channel()

def publish(method, body, queue):
    properties = pika.BasicProperties(method)
    print('publish', body)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(body),
        properties=properties,
    )


