from django.urls import path
from dialog import consumer

websocket_urlpatterns = [
    path("ws/dialog", consumer.DialogConsumer.as_asgi()),
]
