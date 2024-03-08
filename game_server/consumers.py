from channels.generic.websocket import AsyncJsonWebsocketConsumer
import asyncio
from .pong_game_manager import PongGameManager
from .pong_game import PongGame
from .authentication import authenticate
import uuid

unauthenticated_room = 'unauthenticated_room'

class WaitingRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(unauthenticated_room, self.channel_name)

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(unauthenticated_room, self.channel_name)
        except:
            pass



    async def receive_json(self, content, **kwargs):
        if 'token' not in content.keys():
            await self.close()
        user = authenticate(content['token'])
        if not user:
            await self.send_json({
                'error': 'Invalid token'
            })
            await self.close()
        self.scope['user'] = user
        await self.channel_layer.group_discard(unauthenticated_room, self.channel_name)


class TournamentWaitingRoomConsumer(WaitingRoomConsumer):
    waiting_list = {}  # channel_name -> user



class RandomWaitingRoomConsumer(WaitingRoomConsumer):
    waiting_list = {}  # channel_name -> user
    async def connect(self):
        await super().connect()

    async def receive_json(self, content, **kwargs):
        await super().receive_json(content, **kwargs)
        self.waiting_list[self.channel_name] = self.scope['user']
        user_cnt = len(self.waiting_list)
        if user_cnt == 2:
            channel_names = list(self.waiting_list.keys())
            message = {
                'type': 'send_room_id',
                'room_id': str(uuid.uuid4()),
                'user_nicknames': [self.waiting_list[channel_names[0]]['nickname'],
                                   self.waiting_list[channel_names[1]]['nickname']]
            }
            for i in self.waiting_list.keys():
                await self.channel_layer.send(i, message)

    async def disconnect(self, close_code):
        await super().disconnect(close_code)
        self.waiting_list.pop(self.channel_name)


    async def send_room_id(self, event):
        # room_id, player1_nick, player2_nick, who
        message: dict = event.copy()
        message.pop('type')
        if message['user_nicknames'][0] == self.scope['user']['nickname']:
            message['player'] = 1
        elif message['user_nicknames'][1] == self.scope['user']['nickname']:
            message['player'] = 2
        await self.send_json(message)
        await self.close()



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
