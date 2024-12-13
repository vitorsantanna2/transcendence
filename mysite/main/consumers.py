import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game.ball import Ball
from .game.player import Player, AutoPlayer
from asgiref.sync import sync_to_async
import asyncio
import logging
from asyncio import Lock

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.debug("Logging configurado corretamente.")

def create_player(x_pos, y_pos, speed, width, height, player_id, mode, canvas_width, canvas_height):
    if mode == 'local':
        return AutoPlayer(x_pos, y_pos, speed, width, height, player_id, canvas_width, canvas_height)
    else:
        return Player(x_pos, y_pos, speed, width, height, player_id, canvas_width, canvas_height)
    
def predict_ball_position(ballX, ballY, speedX, speedY, screenWidth, screenHeight):
    pos_x = ballX
    pos_y = ballY
    velocity_x = speedX
    velocity_y = speedY

    while 0 < pos_x < screenWidth:
        pos_x += velocity_x
        pos_y += velocity_y
        if pos_y <= 0 or pos_y >= screenHeight:
            velocity_y *= -1
    return pos_y

games = {}
class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import Match
        self.game_id = self.scope['url_route']['kwargs']['game_id']

        self.room_group_name = f'game_{self.game_id}'
        if not self.room_group_name:
            log.error("Room group name is not defined. Closing connection.")
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        match = await sync_to_async(Match.objects.get)(game_id=self.game_id)
        game_type = match.game_type

        if self.game_id not in games:
            games[self.game_id] = {
            'player1': Player(40, 250, 10, 50, 70, 1, 800, 600),
            'player2': await sync_to_async(create_player)(710, 250, 10, 50, 70, 2, game_type, 800, 600),
            'ball': Ball(15, 400, 300, 5.0, 5.0, 800, 600),
            'loop_active': False,
            'players_connected': 0,
            'lock': Lock()
        }
            
        if not games[self.game_id]['loop_active']:
            async with games[self.game_id]['lock']:
                if not games[self.game_id]['loop_active']:
                    games[self.game_id]['loop_active'] = True
                    asyncio.create_task(self.game_loop(self.game_id))
                
        self.player1 = games[self.game_id]['player1']
        self.player2 = games[self.game_id]['player2']
        self.ball = games[self.game_id]['ball']

        if not games[self.game_id]['player1'].connected:
            self.player_id = 1
            games[self.game_id]['player1'].connected = True
        elif not games[self.game_id]['player2'].connected:
            self.player_id = 2
            games[self.game_id]['player2'].connected = True
        else:
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Game is full.'}))
            await self.close()
            return

        games[self.game_id]['players_connected'] += 1

        await self.send(text_data=json.dumps({
            'type': 'game_id',
            'game_id': self.game_id,
            'player_id': self.player_id,
            'game_type': game_type
        }))

        self.send_player1_pos = asyncio.create_task(self.update_player_pos(1))
        self.send_player2_pos = asyncio.create_task(self.update_player_pos(2))
        self.send_ball_pos = asyncio.create_task(self.update_ball_pos())
        

    async def disconnect(self, close_code):
        from asgiref.sync import sync_to_async
        from .models import Match
              
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if hasattr(self, 'send_player1_pos'):
            self.send_player1_pos.cancel()
        if hasattr(self, 'send_player2_pos'):
            self.send_player2_pos.cancel()
        if hasattr(self, 'send_ball_pos'):
            self.send_ball_pos.cancel()

        if self.player_id == 1:
            games[self.game_id]['player1'].connected = False
        elif self.player_id == 2:
            games[self.game_id]['player2'].connected = False

        games[self.game_id]['players_connected'] -= 1

        if games[self.game_id]['players_connected'] == 0:
            del games[self.game_id]
            match = await sync_to_async(Match.objects.get)(game_id=self.game_id)
            match.is_active = False
            await sync_to_async(match.save)()
            match_score = await sync_to_async(Match.objects.get)(game_id=self.game_id)
            match_score.p1_score = self.player1.score
            match_score.p2_score = self.player2.score
            await sync_to_async(match_score.save)()


    async def receive(self, text_data):
        from .models import Match
        match = await sync_to_async(Match.objects.get)(game_id=self.game_id)
        game_type = match.game_type
        data = json.loads(text_data)
        player_id = data['player']
        direction = data['direction']

        if player_id == 1:
            if direction == 'up':
                self.player1.y_pos -= self.player1.speed
            elif direction == 'down':
                self.player1.y_pos += self.player1.speed
        if player_id == 2 and game_type == 'online':
            if direction == 'up':
                self.player2.y_pos -= self.player2.speed
            elif direction == 'down':
                self.player2.y_pos += self.player2.speed
        
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
    
    async def game_loop(self, game_id):
        from .models import Match
        self.delay = 0
        self.target = 0

        while game_id in games and games[game_id]['players_connected'] > 0:
            self.player1 = games[game_id]['player1']
            self.player2 = games[game_id]['player2']

            self.ball.movement()
            self.ball.collision(self.player1, self.player2)

            match = await sync_to_async(Match.objects.get)(game_id=self.game_id)
            game_type = match.game_type
            if game_type == 'local':
                centery = self.player2.height // 2
                bottom = self.player2.y_pos + self.player2.height
                top = self.player2.y_pos
                
                if self.player2.delay > 0:
                    self.delay -= 1
                else:
                    self.target = predict_ball_position(self.ball.x, self.ball.y, self.ball.speed_x, self.ball.speed_y, 800, 600)
                    self.delay = 100

                if centery < self.target and bottom < self.player2.canvas_height:
                    self.player2.y_pos += self.player2.speed
                elif centery > self.target and top > 0:
                    self.player2.y_pos -= self.player2.speed
                
                if self.player2.y_pos + self.player2.height > self.player2.canvas_height:
                    self.player2.y_pos = self.player2.canvas_height - self.player2.height

            await self.channel_layer.group_send(
                f'game_{game_id}',
                {
                    'type': 'update_state',
                    'state': {
                        'ball': {
                            'x': self.ball.x,
                            'y': self.ball.y,
                            'speed_x': self.ball.speed_x,
                            'speed_y': self.ball.speed_y,
                            'radius': self.ball.radius
                        },
                        'players': [
                            {'id': 1, 'x': self.player1.x_pos, 'y': self.player1.y_pos, 'score': self.player1.score},
                            {'id': 2, 'x': self.player2.x_pos, 'y': self.player2.y_pos, 'score': self.player2.score}
                        ]
                    }
                }
            )
            await asyncio.sleep(0.05)

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

    async def update_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update_state',
            'state': event['state']
    }))
    
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
            'score': event['score']
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