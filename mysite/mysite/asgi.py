"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""


import os
from django.core.asgi import get_asgi_application

# Set the environment variable for settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Initialize Django ASGI application early to populate AppRegistry
django_asgi_app = get_asgi_application()

# Import dependencies AFTER initializing Django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Import routing patterns
from main.routing import websocket_urlpatterns
from chat.routing import websocket_urlpatterns2

# Combine routing patterns
url_patterns = (
    websocket_urlpatterns +
    websocket_urlpatterns2
)

# Define ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Use the initialized Django ASGI app
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(url_patterns))
    ),
})

