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
        self.send_ball_position_task = asyncio.create_task(self.update_ball_position())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.send_ball_position_task.cancel()
        self.self.send_player1_pos.cancel()
        self.self.send_player2_pos.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        player_id = data['player']
        x_pos = data['x']
        y_pos = data['y']
        if player_id == 1:
            self.player1.x_pos = x_pos
            self.player1.y_pos = y_pos
        elif player_id == 2:
            self.player2.x_pos = x_pos
            self.player2.y_pos = y_pos
        elif data['type'] == 'ball_position':
            self.ball.radius = data['radius']
            self.ball.x = data['x']
            self.ball.y = data['y']
            self.ball.speed_x = data['speed_x']
            self.ball.speed_y = data['speed_y']
            self.ball.width = data['width']
            self.ball.height = data['height']
        # elif data['type'] == 'player1_move':
        #     direction = data['direction']
        #     if direction == 'up':
        #         await self.player1.move_up()
        #     elif direction == 'down':
        #         await self.player1.move_down() 
        # elif data['type'] == 'player2_move':
        #     direction = data['direction']
        #     if direction == 'up':
        #         await self.player2.move_up()
        #     elif direction == 'down':
        #         await self.player2.move_down() 

    async def update_player_pos(self, player_id):
        while True:
            if player_id == 1:
                x = self.player1.x_pos
                y = self.player1.y_pos
            elif player_id == 2:
                x = self.player2.x_pos
                y = self.player2.y_pos

            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": 'player_position',
                        "player": player_id,
                        "x": x,
                        "y": y
                    }
                )
            await asyncio.sleep(0.05)
    
    async def update_ball_position(self):
        while True:
            self.ball.movement()
            self.ball.collision()
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
            'player': player_id,
            'x': event['x'],
            'y': event['y']
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