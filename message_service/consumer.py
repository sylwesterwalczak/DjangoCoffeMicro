import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_service.settings')
django.setup()

from django.db.models import F
import pika
import json
from message.views import MessageUtils


queue_name = os.environ.get('MESSAGE_QUEUE')
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
    message = MessageUtils()
    print('recived_data', recived_data)
    message.create_message(recived_data)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print('Start Consuming - Message Queue')

channel.start_consuming()
channel.close()
