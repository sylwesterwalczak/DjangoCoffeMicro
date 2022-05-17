import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .views import MessageUtils



class PurchaseConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        msg_instance = MessageUtils()
        obj = msg_instance.fetch_message(self.room_name)
        msg_ = self.messages_to_json(obj.get("messages")) if obj.get(
            "status") == "OK" else obj.get("messages")
        content = {
            'messages': msg_
        }
        self.send(text_data=json.dumps(content))

    commands = {
        'fetch_messages': fetch_messages,
    }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.purchase_id,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'channel_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

        
