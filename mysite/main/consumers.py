import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game.ball import Ball
from .game.player import Player
from channels.db import database_sync_to_async
from django.apps import apps
import asyncio
import uuid
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger(__name__)

log.debug("Logging configurado corretamente.")

games = {}

def create_new_game():
    game_id = str(uuid.uuid4())
    games[game_id] = {
        'player1': Player(40, 250, 10, 50, 70, 1),
        'player2': Player(710, 250, 10, 50, 70, 2),
        'ball': Ball(15, 400, 300, 5.0, 5.0, 800, 600),
    }
    return game_id

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        Match = apps.get_model('main', 'Match')
        User = apps.get_model('auth', 'User')

        self.game_id = self.scope['url_route']['kwargs'].get('game_id', None)

        existing_match_qs = await database_sync_to_async(Match.objects.filter)(game_id=self.game_id, is_active=True)
        existing_match = await database_sync_to_async(existing_match_qs.first)()

        if existing_match:
            log.debug(f"Game {self.game_id} already exists. Joining the game.")
        else:
            self.game_id = create_new_game()
            log.debug(f"Creating new game with ID: {self.game_id}")

            self.player1 = games[self.game_id]['player1']
            self.player2 = games[self.game_id]['player2']

            await database_sync_to_async(Match.objects.create)(
                    game_id=self.game_id,
                    is_active=True
                )

            # try:
            #     user1 = await database_sync_to_async(User.objects.get)(id=self.player1.player_id)
            #     user2 = await database_sync_to_async(User.objects.get)(id=self.player2.player_id)

            #     await database_sync_to_async(Match.objects.create)(
            #         game_id=self.game_id,
            #         user1=user1,
            #         user2=user2,
            #         user1_score=self.player1.score,
            #         user2_score=self.player2.score,
            #         is_active=True
            #     )
            # except User.DoesNotExist as e:
            #     log.error(f"User does not exist: {e}")
            #   await self.close()

        log.debug(self.game_id)
        
        self.ball = games[self.game_id]['ball']
        
        self.room_group_name = f'game_{self.game_id}'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'game_id',
            'game_id': self.game_id
        }))
        if not hasattr(self, 'player_id'):
            self.player_id = 1 if len(games[self.game_id]) == 1 else 2
            await self.send(text_data=json.dumps({
                'player_id': self.player_id
            }))

        self.send_player1_pos = asyncio.create_task(self.update_player_pos(1))
        self.send_player2_pos = asyncio.create_task(self.update_player_pos(2))
        self.send_ball_pos = asyncio.create_task(self.update_ball_pos())
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.send_ball_pos.cancel()
        self.send_player1_pos.cancel()
        self.send_player2_pos.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        player_id = data['player']
        direction = data['direction']

        if player_id == 1:
            if direction == 'up':
                self.player1.y_pos -= self.player1.speed
            elif direction == 'down':
                self.player1.y_pos += self.player1.speed
        if player_id == 2:
            if direction == 'up':
                self.player2.y_pos -= self.player2.speed
            elif direction == 'down':
                self.player2.y_pos += self.player2.speed
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ball_position',
                'radius': self.ball.radius,
                'x': self.ball.x,
                'y': self.ball.y,
                'speed_x': self.ball.speed_x,
                'speed_y': self.ball.speed_y,
                'width': self.ball.width,
                'height': self.ball.height
            }
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_position',
                'player': player_id,
                'x': self.player1.x_pos if player_id == 1 else self.player2.x_pos,
                'y': self.player1.y_pos if player_id == 1 else self.player2.y_pos,
                'speed': self.player1.speed if player_id == 1 else self.player2.speed,
                'score': self.player1.score if player_id == 1 else self.player2.score
            }
        )

    async def update_player_pos(self, player_id):
        while True:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": 'player_position',
                    "player": player_id,
                    "x": self.player1.x_pos if player_id == 1 else self.player2.x_pos,
                    "y": self.player1.y_pos if player_id == 1 else self.player2.y_pos,
                    "speed": self.player1.speed if player_id == 1 else self.player2.speed,
                    "player_id": self.player1.player_id if player_id == 1 else self.player2.player_id,
                    "score": self.player1.score if player_id == 1 else self.player2.score
                }
            )
            await asyncio.sleep(0.05)
    
    async def update_ball_pos(self):
        while True:
            self.ball.movement()
            self.ball.collision(self.player1, self.player2)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "ball_position",
                    "radius": self.ball.radius,
                    "x": self.ball.x,
                    "y": self.ball.y,
                    "speed_x": self.ball.speed_x,
                    "speed_y": self.ball.speed_y,
                    "width": self.ball.width,
                    "height": self.ball.height
                }
            )
            await asyncio.sleep(0.05)
            
    async def player_position(self, event):
        player_id = event['player']
        await self.send(text_data=json.dumps({
            'type': 'player_position',
            'player': player_id,
            'x': event['x'],
            'y': event['y'],
            'speed': event['speed'],
            'score': event['score'],
        }))

    async def ball_position(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ball_position',
            'radius': event['radius'],
            'x': event['x'],
            'y': event['y'],
            'speed_x': event['speed_x'],
            'speed_y': event['speed_y'],
            'width': event['width'],
            'height': event['height']
        }))