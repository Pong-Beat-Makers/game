from channels.routing import URLRouter
from django.urls import path, include

from game_server import consumers

sub_url_patterns = [
    path("<uuid:room_id>/", consumers.GameServerConsumer.as_asgi()),
    path("waitingroom/random/", consumers.RandomWaitingRoomConsumer.as_asgi()),
    path("waitingroom/tournament/", consumers.TournamentWaitingRoomConsumer.as_asgi()),
]

websocket_urlpatterns = [
    path("ws/game/", URLRouter(sub_url_patterns)),
]
