from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] 
        self.room_group_name = f"chat_{self.room_name}"  

        # Join room group (Redis pub/sub group)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name  # unique for this connection
        )
        
        # Accept the WebSocket connection
        await self.accept()

        print(f"User connected to room: {self.room_group_name}")
    
    async def disconnect(self, close_code):
    # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"User disconnected from {self.room_group_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

    # Send the message to the group (not directly to clients)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # This decides what method to call
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to the WebSocket client
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))

