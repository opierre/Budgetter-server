import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DashboardConsumer(WebsocketConsumer):
    """
    Dashboard consumer for all data
    """

    room_name = ''
    room_group_name = ''

    def connect(self):
        """
        Accept connection to ws

        :return: None
        """

        self.room_name = f"dashboard"
        self.room_group_name = f"debug_dashboard"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        """
        Override receive
        """

        data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            "dashboard",
            {
                "type": "chat.message",
                "data": data_json
            }
        )
