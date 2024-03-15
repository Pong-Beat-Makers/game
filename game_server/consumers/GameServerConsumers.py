import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from game_server.authentication import authenticate
from game_server.pong_game import PongGame
from game_server.pong_game_manager import PongGameManager


class GameServerConsumer(AsyncJsonWebsocketConsumer):
    waiting_list = {}  # channel_name -> user

    game_manager = PongGameManager()

    async def connect(self):
        self.room_id = str(self.scope['url_route']['kwargs']['room_id'])
        self.room_group_name = self.room_id

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        num_of_players = len(self.channel_layer.groups[self.room_group_name])
        if num_of_players == 1:
            await GameServerConsumer.game_manager.create_game(self.room_group_name)
            await GameServerConsumer.game_manager.enroll_player1(self.room_group_name)
        elif num_of_players == 2:
            await GameServerConsumer.game_manager.enroll_player2(self.room_group_name)
        elif num_of_players == 3:
            await self.send_json({
                'error': 'Full Room'
            })
            await self.close()

    async def receive_json(self, content, **kwargs):
        game_manager = GameServerConsumer.game_manager
        game: PongGame = game_manager.get_game(self.room_group_name)

        if game.player1_nickname == '' or game.player2_nickname == '':
            if 'token' not in content:
                await self.send_system_message({
                    'type': "send_system_message",
                    'message': 'Someone Unauthorized'
                })
            else:
                player = authenticate(content['token'])
                if player is None:
                    await self.send_system_message({
                        'type': "send_system_message",
                        'message': 'Someone Unauthorized'
                    })
                #  인증 성공
                if game.player1_channel_name == self.channel_name:
                    game.player1_nickname = player['nickname']
                elif game.player2_channel_name == self.channel_name:
                    game.player2_nickname = player['nickname']

                if game.player1_nickname != '' and game.player2_nickname != '':
                    asyncio.create_task(GameServerConsumer.game_manager.start_game(self.room_group_name))
            return

        if 'move' not in content:
            return
        if content['move'] == 'up':
            game.set_player_dy(self.channel_name, -1)
        elif content['move'] == 'down':
            game.set_player_dy(self.channel_name, +1)
        elif content['move'] == 'stop':
            game.stop_player(self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # my function

    async def send_game_status(self, event):
        await self.send_json(event)

    async def send_system_message(self, event):
        await self.send_json(event)
        if event['message'] == 'Game End':
            await self.close()
