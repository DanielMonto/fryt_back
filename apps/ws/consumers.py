import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class PrivateUsersChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id=self.scope['url_route']['kwargs']['chat_id']
        self.conversation_group_name=f'private_chat_{self.chat_id}'
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )
    async def receive(self, text_data=None, bytes_data=None):
        td=json.loads(text_data)
        message_text=td['message']
        writer=td['writer']
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type':'chat_message',
                'message':str(message_text),
                'writer':str(writer)
            }
        )
        # await save_message(td['conversation'],writer,message_text)
    async def chat_message(self,event):
        message=event['message']
        writer=event['writer']
        await self.send(text_data=json.dumps({
            'message':str(message),
            'writer':str(writer)
        }))