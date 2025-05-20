# your_app/routing.py
from django.urls import path
from .views import SendDateMessage

websocket_urlpatterns = [
    path("api/ws/", SendDateMessage.as_asgi()),
]