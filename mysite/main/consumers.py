import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game.ball import Ball
from .game.player import Player
import asyncio

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'pong'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if not hasattr(self, 'player_id'):
            self.player_id = 0
            self.player1 = Player(40, 250, 10, 50, 70, 1)
            self.player2 = Player(710, 250, 10, 50, 70, 2)

        await self.send(text_data=json.dumps({
            'player_id': self.player_id
        }))

        if not hasattr(self, 'ball'):
            self.ball = Ball(15, 400, 300, 5.0, 5.0, 800, 600)

        self.send_player1_pos = asyncio.create_task(self.update_player_pos(1))
        self.send_player2_pos = asyncio.create_task(self.update_player_pos(2))
        self.send_ball_pos = asyncio.create_task(self.update_ball_pos())
        

    async def disconnect(self):
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
                self.player1.move_up()
            elif direction == 'down':
                self.player1.move_down()
        if player_id == 2:
            if direction == 'up':
                self.player2.move_up()
            elif direction == 'down':
                self.player2.move_down()
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