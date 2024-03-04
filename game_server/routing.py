from django.urls import path

from game_server import consumers

websocket_urlpatterns = [
    path("ws/game/<uuid:room_id>/", consumers.GameServerConsumer.as_asgi()),
]