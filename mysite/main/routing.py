from django.urls import re_path
from . import consumers
from django.urls import include, path

websocket_urlpatterns = [
<<<<<<< HEAD
    re_path(r"ws/main/$", consumers.PongConsumer.as_asgi()),
]

=======
    re_path(r'ws/main/(?P<game_id>[^/]+)/$', consumers.PongConsumer.as_asgi())
]
>>>>>>> main
