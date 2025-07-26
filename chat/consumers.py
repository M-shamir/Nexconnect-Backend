from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        user = self.scope["user"]
        

        if not user.is_authenticated:
        
            await self.close()
            print("Unauthenticated user attempted to connect.")
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] 
        self.room_group_name = f"chat_{self.room_name}"  
        
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name 
        )
        
        
        await self.accept()
        print("username",user)
        print(f"User connected to room: {self.room_group_name}")
    
    async def disconnect(self, close_code):
        user = self.scope["user"]
    # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"User disconnected from {user} {self.room_group_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

    
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message", 
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

