from django.urls import re_path
from .consumer import MyWebSocketConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', MyWebSocketConsumer.as_asgi()),
]
