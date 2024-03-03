from .pong_game import PongGame
from channels.layers import get_channel_layer
import asyncio
from game_data.models import GameDataModel
from channels.db import database_sync_to_async

class PongGameManager:
    def __init__(self):
        self.games = dict()

    async def create_game(self, room_group_name):
        game = PongGame()
        self.games[room_group_name] = game

    async def enroll_player1(self, room_group_name):
        game = self.games[room_group_name]
        channel_layer = get_channel_layer()

        game.player1_channel_name = list(channel_layer.groups[room_group_name].keys())[0]

    async def enroll_player2(self, room_group_name):
        game = self.games[room_group_name]
        channel_layer = get_channel_layer()

        game.player2_channel_name = list(channel_layer.groups[room_group_name].keys())[1]

    async def start_game(self, room_group_name):
        game = self.games[room_group_name]
        channel_layer = get_channel_layer()

        await self.send_player_data(room_group_name)

        while len(channel_layer.groups[room_group_name]) == 2 and game.status == 'play':
            data = game.next_frame()
            data['type'] = 'send_game_status'

            await channel_layer.group_send(room_group_name, data)
            await asyncio.sleep(0.05)

        await self.game_end(room_group_name)

    async def game_end(self, room_group_name):
        game: PongGame = self.games[room_group_name]
        channel_layer = get_channel_layer()
        message = {
            'type': 'send_system_message',
            'message': 'Game End',
        }
        if game.status == 'end':  # 정상 종료
            message['score'] = game.score
        else:  # 탈주 종료
            if game.player1_channel_name not in channel_layer.groups[room_group_name].keys():  # player 1 탈주
                message['score'] = [0, game.winning_score]
            elif game.player2_channel_name not in channel_layer.groups[room_group_name].keys():  # player 2 탈주
                message['score'] = [game.winning_score, 0]

        await database_sync_to_async(GameDataModel.create_match_and_save_game)({
            "user1_nickname": game.player1_nickname,
            "user2_nickname": game.player2_nickname,
            "user1_score": game.score[0],
            "user2_score": game.score[1],
            "match_type": "test"  # TODO: match type에 따른 수정 필요
        })

        await channel_layer.group_send(room_group_name, message)
        self.games.pop(room_group_name)

    def get_game(self, room_group_name):
        return self.games.get(room_group_name)

    # 각 channel에 플레이어 정보 제공
    async def send_player_data(self, room_group_name):
        channel_layer = get_channel_layer()
        game = self.games[room_group_name]
        message = {
            'type': 'send_system_message',
            'message': 'Game Start',
            'player': 1
        }
        await channel_layer.send(game.player1_channel_name, message)
        message['player'] = 2
        await channel_layer.send(game.player2_channel_name, message)


