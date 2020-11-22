from django.urls import path

from apps.channel_practice import consumers

websocket_urlpattern=[
    path('ws/get_data/',consumers.MyConsumer.as_asgi()),
    path('notice/',consumers.TestConsumer.as_asgi()),
]
