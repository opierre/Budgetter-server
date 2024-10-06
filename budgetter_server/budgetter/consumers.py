import json

from channels.generic.websocket import AsyncWebsocketConsumer


class BudgetterConsumer(AsyncWebsocketConsumer):
    """
    Budgetter consumer for all global data
    """

    room_name = None
    room_group_name = None

    async def connect(self):
        """
        Accept connection to ws

        :return: None
        """

        self.room_name = f"budgetter"
        self.room_group_name = f"debug_budgetter"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """
        Override receive
        """

        data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "data": data_json
            }
        )

    async def chat_message(self, event):
        """
        Forward message

        :param event: event sent
        """
        message = event["data"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {
                "data": message
            }
        ))
