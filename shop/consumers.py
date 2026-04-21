import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderNotificationConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = "managers"

    async def connect(self):
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    # Получение сообщения из группы и отправка в WS
    async def order_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))
