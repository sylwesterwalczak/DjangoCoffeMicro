import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'story_service.settings')
django.setup()


import pika
import json

from story.views import check_story

queue_name = os.environ.get('PURCHASE')

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

channel.queue_declare(queue=queue_name)

def callback(ch, method, properties, body):
    recived_data = json.loads(body)
    check_story(recived_data, properties)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print('Start Consuming - Story Queue')

channel.start_consuming()
channel.close()
