from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/main/", consumers.PongConsumer.as_asgi()),
    re_path(r"ws/main/(?P<game_id>[^/]+)/$", consumers.PongConsumer.as_asgi()),
]