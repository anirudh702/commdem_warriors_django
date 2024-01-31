import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from oneToOneChatModule.server import PracticeConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commdem_warriors_backend.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(
            [
                path("practice", PracticeConsumer.as_asgi())
                # you can define all your routers here
            ]
        )
        # Just HTTP for now. (We can add other protocols later.)
    }
)
