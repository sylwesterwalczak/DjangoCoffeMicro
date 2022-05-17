import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'purchase_service.settings')
django.setup()

import pika
import json
from purchase.views import change_status

queue_name = os.environ.get('REPLY_PURCHASE')
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
    change_status(recived_data.get('order_number'), properties.content_type)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print('Start Consuming - Purchase Queue')

channel.start_consuming()
channel.close()
