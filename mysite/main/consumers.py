import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game.ball import Ball
from .game.player import Player
from channels.db import database_sync_to_async
import uuid
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger(__name__)

log.debug("Logging configurado corretamente.")

games = {}

def create_new_game(id):
    games[id] = {
        'player1': Player(40, 250, 10, 50, 70, 1),
        'player2': Player(710, 250, 10, 50, 70, 2),
        'ball': Ball(15, 400, 300, 5.0, 5.0, 800, 600),
    }

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import Match
        self.game_id = str(uuid.uuid4())
        create_new_game(self.game_id)
        match = await database_sync_to_async(Match.objects.create)(game_id=self.game_id, is_active=True)
        database_sync_to_async(Match.save)(match)
        log.debug(f"Creating new game with ID: {self.game_id}")
                
        if self.game_id in games:
            self.player1 = games[self.game_id]['player1']
            self.player2 = games[self.game_id]['player2']
            self.ball = games[self.game_id]['ball']
        else:
            log.error(f"Game ID {self.game_id} not found in games. Closing connection.")
            await self.close()
            return

        log.debug(self.game_id)

        self.room_group_name = f'game_{self.game_id}'
        if not self.room_group_name:
            log.error("Room group name is not defined. Closing connection.")
            await self.close()
            return
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'game_id',
            'game_id': self.game_id
        }))
        if 'player1' in games[self.game_id] and games[self.game_id]['player1'] and not getattr(games[self.game_id]['player1'], 'connected', False):
            self.player_id = 1
            games[self.game_id]['player1'].connected = True
        elif 'player2' in games[self.game_id] and games[self.game_id]['player2'] and not getattr(games[self.game_id]['player2'], 'connected', False):
            self.player_id = 2
            games[self.game_id]['player2'].connected = True
        else:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Game is full. Connection closed.'
            }))
            await self.close()
            return
        
        await self.send(text_data=json.dumps({
            'type': 'game_id',
            'game_id': self.game_id,
            'player_id': self.player_id
        }))

        self.send_player1_pos = asyncio.create_task(self.update_player_pos(1))
        self.send_player2_pos = asyncio.create_task(self.update_player_pos(2))
        self.send_ball_pos = asyncio.create_task(self.update_ball_pos())
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if hasattr(self, 'send_player1_pos'):
            self.send_player1_pos.cancel()
        if hasattr(self, 'send_player2_pos'):
            self.send_player2_pos.cancel()
        if hasattr(self, 'send_ball_pos'):
            self.send_ball_pos.cancel()

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