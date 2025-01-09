from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import ChatConsumer
application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    ])
})
