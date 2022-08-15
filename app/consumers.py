from cgitb import text
from email import message
import json
from unicodedata import name
import webbrowser
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        name = text_data_json["name"]
        message = text_data_json['message']

        print("name:", name, "message:", message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'name':name
            }
        )
    
    def chat_message(self, event):
        message = event['message']
        name = event['name']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'name':name
        }))