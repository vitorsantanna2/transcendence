from django.urls import re_path
from . import consumers
from django.urls import include, path

websocket_urlpatterns = [
    re_path(r"ws/main/$", consumers.PongConsumer.as_asgi()),
]

