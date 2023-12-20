import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DashboardConsumer(WebsocketConsumer):
    """
    Dashboard consumer for all data
    """

    def connect(self):
        """
        Accept connection to ws

        :return: None
        """

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"dashboard_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
