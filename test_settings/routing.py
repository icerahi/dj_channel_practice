from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter


from apps.channel_practice import routing

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(URLRouter(routing.websocket_urlpattern)),
})