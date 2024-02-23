from channels.generic.websocket import AsyncJsonWebsocketConsumer
import asyncio
from .pong_game_manager import PongGameManager

class GameServerConsumer(AsyncJsonWebsocketConsumer):

    game_manager = PongGameManager()
    async def connect(self):
        self.room_id = str(self.scope['url_route']['kwargs']['room_id'])
        self.room_group_name = self.room_id

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        num_of_players = len(self.channel_layer.groups[self.room_group_name])
        if num_of_players == 2:
            asyncio.create_task(GameServerConsumer.game_manager.start_game(self.room_group_name))
        elif num_of_players == 3:
            await self.send_json({
                'error': 'Full Room'
            })
            await self.close()

    async def receive_json(self, content, **kwargs):
        game_manager = GameServerConsumer.game_manager
        game = game_manager.get_game(self.room_group_name)
        if 'move' not in content:
            return
        if content['move'] == 'up':
            game.move_player(self.channel_name, -1)
        elif content['move'] == 'down':
            game.move_player(self.channel_name, +1)
        elif content['move'] == 'stop':
            game.stop_player(self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # my function

    async def send_game_status(self, event):
        await self.send_json(event)

    async def send_system_message(self, event):
        await self.send_json(event)
