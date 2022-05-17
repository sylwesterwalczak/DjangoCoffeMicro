from .models import Message

from asgiref.sync import async_to_sync
import channels.layers

channel_layer = channels.layers.get_channel_layer()


class MessageUtils:

    def message_to_json(self, message):
        return {
            'id': message.id,
            'purchase_id': message.purchase_id,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def fetch_message(self, purchase_id):

        messages = Message.objects.filter(purchase_id=purchase_id)
        if len(messages) == 0:
            content = {
                'status': 'NO_ITEM',
                'messages': 'Brak zamowienia o takim numerze'
            }
            return content

        content = {
            'status': 'OK',
            'messages': messages
        }

        return content

    def create_message(self, message):
        purchase_id = message.get('order_number')
        message = message.get('message')

        message = Message.objects.create(
            purchase_id=purchase_id,
            content=message
        )

        async_to_sync(channel_layer.group_send)(
            'channel_%s' % purchase_id,
            {
                'type': 'chat_message',
                'message': self.message_to_json(message)
            }
        )