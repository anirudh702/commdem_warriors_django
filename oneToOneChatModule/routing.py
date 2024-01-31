import sys
from os import path

from channels.auth import AuthMiddlewareStack

sys.path.append("/Users/anirudh.chawla/python_django/commdem_warriors_same_database")
from channels.routing import ProtocolTypeRouter, URLRouter

from oneToOneChatModule import server

# URLs that handle the WebSocket connection are placed here.

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter([path("whole1/", server.PracticeConsumer)])
        )
    }
)
