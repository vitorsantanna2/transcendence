import json
from channels.generic.websocket import AsyncWebsocketConsumer
from  .game.ball import Ball
from .game.player import Player, AutoPlayer
import asyncio

class PongConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(args, kwargs)
		self.player1 = None
		self.player2 = None
		self.ball = None
		self.send_ball_position_task = None
		self.send_player1_position_task = None
		self.send_player2_position_task = None
		self.gamer_score = 0

	async def connect(self):
		print("WebSocket connected!")
		await self.channel_layer.group_add("pong", self.channel_name)
		await self.accept()
		self.player1 = Player(40, 250, 10, 50, 70)
		self.player2 = Player(710, 250, 10, 50, 70)
		self.ball = Ball(15, 400, 300, 5.0, 5.0, 800, 600)
		self.send_ball_position_task = asyncio.create_task(self.send_ball_position_periodically())
		self.send_player1_position_task = asyncio.create_task(self.send_player1_position_periodically())
		self.send_player2_position_task = asyncio.create_task(self.send_player2_position_periodically())

	async def disconnect(self, close_code):
		print("WebSocket disconnected!")
		await self.channel_layer.group_discard("pong", self.channel_name)
		self.send_ball_position_task.cancel()
		self.send_player1_position_task.cancel()
		self.send_player2_position_task.cancel()

	async def receive(self, text_data):
		try:
			data = json.loads(text_data)
		except json.JSONDecodeError:
			print("Falha ao decodificar JSON.")
			return

		await self.channel_layer.group_send(
			"pong",
			{
				"type": "ball_position",
				"text": text_data,
			},
		)

		await self.channel_layer.group_send(
			"pong",
			{
				"type": "player1_position",
				"text": text_data,
			},
		)

		await self.channel_layer.group_send(
			"pong",
			{
				"type": "player2_position",
				"text": text_data,
			},
		)

	async def player1_position(self, event):
		data = json.loads(event['text'])
		if data['type'] == 'player1_position':
			self.player1.x_pos = data['x']
			self.player1.y_pos = data['y']
			self.player1.speed = data['speed']
			await self.send(text_data=json.dumps({
				'type': 'player1_position',
				'x': self.player1.x_pos,
				'y': self.player1.y_pos,
				'speed': self.player1.speed,
			}))

	async def player2_position(self, event):
		data = json.loads(event['text'])
		if data['type'] == 'player2_position':
			self.player2.x_pos = data['x']
			self.player2.y_pos = data['y']
			self.player2.speed = data['speed']
			await self.send(text_data=json.dumps({
				'type': 'player2_position',
				'x': self.player2.x_pos,
				'y': self.player2.y_pos,
				'speed': self.player2.speed,
			}))

	async def ball_position(self, event):
		data = json.loads(event['text'])
		if data['type'] == 'ball_position':
			self.ball.x = data['x']
			self.ball.y = data['y']
			await self.send(text_data=json.dumps({
				'type': 'ball_position',
				'x': self.ball.x,
				'y': self.ball.y
			}))

	async def send_ball_position_periodically(self):
		while True:
			self.ball.movement()
			self.ball.collision(self.player1, self.player2, self.gamer_score)
			await self.send(text_data=json.dumps({
				'type': 'ball_position',
				'x': self.ball.rect.x,
				'y': self.ball.rect.y
			}))
			await asyncio.sleep(0.05)

	async def send_player1_position_periodically(self):
		while True:
			await self.send(text_data=json.dumps({
				'type': 'player1_position',
				'x': self.player1.rect.x,
				'y': self.player1.rect.y,
				'speed': self.player1.speed
			}))
			await asyncio.sleep(0.05)

	async def send_player2_position_periodically(self):
		while True:
			await self.send(text_data=json.dumps({
				'type': 'player2_position',
				'x': self.player2.rect.x,
				'y': self.player2.rect.y,
				'speed': self.player2.speed
			}))
			await asyncio.sleep(0.05)