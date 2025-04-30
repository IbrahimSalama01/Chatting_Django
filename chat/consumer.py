import jwt, json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime

class MyWebSocketConsumer(AsyncWebsocketConsumer):
    clients = []  # Shared across all instances in a single process
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.current_user = None
    async def connect(self):
        token = self.scope['query_string'].decode().split('token=')[-1]
        

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            self.user_id = payload.get('user_id')
            self.current_user = await self.get_user(self.user_id)
            await self.accept()
            if self not in self.clients:
                self.clients.append(self)
                print(f"User {self.current_user} connected.")
        except jwt.ExpiredSignatureError:
            await self.close()
        except jwt.InvalidTokenError:
            await self.close()

    async def disconnect(self, close_code):
        if self in self.clients:
            self.clients.remove(self)
            print(f"User {self.current_user} disconnected.")

    async def receive(self, text_data):
        msg_data = json.loads(text_data)
        new_msg = {
            "message": msg_data['message'],
            "sender": self.current_user.username,
            "type": "received",
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "id": self.current_user.id,
            "avatar": "https://picsum.photos/200"
        }

        for client in self.clients:
            if client.user_id != self.user_id:
                await client.send(json.dumps(new_msg))

        await self.send(text_data="Echo: " + text_data)

    @staticmethod
    async def get_user(user_id):
        # Async-friendly user fetch
        from asgiref.sync import sync_to_async
        return await sync_to_async(User.objects.get)(id=user_id)
