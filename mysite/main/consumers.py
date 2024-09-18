import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game.ball import Ball
from .game.player import Player
import asyncio

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("pong", self.channel_name)
        await self.accept()
        self.player1 = Player(40, 250, 10, 50, 70)
        self.player2 = Player(710, 250, 10, 50, 70)
        self.ball = Ball(15, 400, 300, 5.0, 5.0, 800, 600)
        self.send_ball_position_task = asyncio.create_task(self.send_ball_position_periodically())
        self.send_player1_position_task = asyncio.create_task(self.send_player1_position_periodically())
        self.send_player2_position_task = asyncio.create_task(self.send_player2_position_periodically())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pong", self.channel_name)
        self.send_ball_position_task.cancel()
        self.send_player1_position_task.cancel()
        self.send_player2_position_task.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'player1_position':
            self.player1.x_pos = data['x']
            self.player1.y_pos = data['y']
        elif data['type'] == 'player2_position':
            self.player2.x_pos = data['x']
            self.player2.y_pos = data['y']
        elif data['type'] == 'ball_position':
            self.ball.x = data['x']
            self.ball.y = data['y']
            self.ball.speed_x = data['speed_x']
            self.ball.speed_y = data['speed_y']
            

    async def send_ball_position_periodically(self):
        while True:
            self.ball.movement()
            await self.channel_layer.group_send(
                "pong",
                {
                    "type": "ball_position",
                    "x": self.ball.x,
                    "y": self.ball.y,
                    "speed_x": self.ball.speed_x,
                    "speed_y": self.ball.speed_y
                }
            )
            print(f"Ball position sent: x={self.ball.x}, y={self.ball.y}")
            await asyncio.sleep(0.05)

    async def send_player1_position_periodically(self):
        while True:
            await self.channel_layer.group_send(
                "pong",
                {
                    "type": "player1_position",
                    "x": self.player1.x_pos,
                    "y": self.player1.y_pos
                }
            )
            #print(f"Player 1 position sent: x={self.player1.x_pos}, y={self.player1.y_pos}")
            await asyncio.sleep(0.05)

    async def send_player2_position_periodically(self):
        while True:
            await self.channel_layer.group_send(
                "pong",
                {
                    "type": "player2_position",
                    "x": self.player2.x_pos,
                    "y": self.player2.y_pos
                }
            )
            #print(f"Player 2 position sent: x={self.player2.x_pos}, y={self.player2.y_pos}")
            await asyncio.sleep(0.05)
            
    async def ball_position(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ball_position',
            'x': event['x'],
            'y': event['y'],
            'speed_x': event['speed_x'],
            'speed_y': event['speed_y']
        }))
        print(f"Ball position event sent: x={event['x']}, y={event['y']}")
    
    async def player1_position(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player1_position',
            'x': event['x'],
            'y': event['y']
        }))
        #print(f"Player 1 position event sent: x={event['x']}, y={event['y']}")

    async def player2_position(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player2_position',
            'x': event['x'],
            'y': event['y']
        }))
        #print(f"Player 2 position event sent: x={event['x']}, y={event['y']}")