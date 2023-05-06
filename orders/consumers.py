from channels.generic.websocket import WebsocketConsumer   
import json
from .models import *
from asgiref.sync import async_to_sync, sync_to_async

# class OrderProgress(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['order_id']
#         self.room_group_name = 'order_%s' % self.room_name
#         print(self.room_group_name)
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()
#         self.send(text_data=json.dumps({'status': 'Connected'}))

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        message = json.loads(text_data)
        order_id = message["order_id"]
        order_status = message["order_status"]
        # Update the cart button status for the user with the specified ID
        if order_status == 'Accepted':
            await self.channel_layer.group_send(
                order_id,
                {
                    'type': 'order_accepted',
                    'order_id': order_id
                }
        )
        elif order_status == 'Rejected':
            await self.channel_layer.group_send(
                order_id,
                {
                    'type': 'order_rejected',
                    'order_id': order_id
                }
            )

    async def order_accepted(self, event):
        order_id = event['order_id']
        await self.send(text_data=json.dumps({
            'order_id': order_id,
            'order_status': 'Accepted'
        }))

    async def order_rejected(self, event):
        order_id = event['order_id']
        await self.send(text_data=json.dumps({
            'order_id': order_id,
            'order_status': 'Rejected'
        }))


        
