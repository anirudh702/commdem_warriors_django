from os import path
from channels.auth import AuthMiddlewareStack
import sys
sys.path.append('/Users/anirudh.chawla/python_django/commdem_warriors_same_database')
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from oneToOneChatModule import consumer

# URLs that handle the WebSocket connection are placed here.

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
            URLRouter([
            path('whole1/',consumer.PracticeConsumer)
            ])
        )
})