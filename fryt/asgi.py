import os

from channels.auth import AuthMiddlewareStack
from apps.ws import routing
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
            URLRouter(
                routes=routing.websocket_urlpatterns
            )
    ),
    "osSettings":os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
})