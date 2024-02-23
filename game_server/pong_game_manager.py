from .pong_game import PongGame
from channels.layers import get_channel_layer
import asyncio

class PongGameManager:
    def __init__(self):
        self.games = dict()

    async def start_game(self, room_group_name):
        game = PongGame()
        self.games[room_group_name] = game
        channel_layer = get_channel_layer()
        game.player1_id = list(channel_layer.groups[room_group_name].keys())[0]
        game.player2_id = list(channel_layer.groups[room_group_name].keys())[1]

        while len(channel_layer.groups[room_group_name]) == 2:
            data = game.next_frame()
            data['type'] = 'send_game_status'

            await channel_layer.group_send(room_group_name, data)
            await asyncio.sleep(0.05)

        await channel_layer.group_send(room_group_name, {
            'type': 'send_system_message',
            'message': 'Game End',
        })
        self.games.pop(room_group_name)

    def get_game(self, room_group_name):
        return self.games.get(room_group_name)


