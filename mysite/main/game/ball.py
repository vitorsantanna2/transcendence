import random

class Ball:
	def __init__(self, radius, x, y, speed_x, speed_y, width, height):
		self.radius = radius
		self.speed_x = speed_x
		self.speed_y = speed_y
		self.initial_x = x
		self.initial_y = y
		self.initial_speed_x = speed_x
		self.initial_speed_y = speed_y
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		# self.rect = pygame.Rect(width // 2 - radius // 2, height // 2 - radius // 2, radius, radius)

	def movement(self):
		self.x += self.speed_x
		self.y += self.speed_y
		# print(f"Coordenadas da bola: x={self.rect.x}, y={self.rect.y}")

	def collision(self, player1, player2, game_score):
		direction = [0, 1]
		angle = [0, 1, 2]
		dir = random.choice(direction)
		ang = random.choice(angle)
		if self.rect.top <= 0 + self.radius or self.rect.bottom >= self.height - self.radius:
			self.speed_y *= -1
		if self.rect.left <= 0 + self.radius:
			player2.score += 1
			if player2.score == game_score:
				player2.rounds += 1
				player1.score = 0
				player2.score = 0
			self.reset_position()
		if self.rect.right >= self.width - self.radius:
			player1.score += 1
			if player1.score == game_score:
				player1.rounds += 1
				player1.score = 0
				player2.score = 0
			self.reset_position()
		if self.rect.colliderect(player1.rect):
			self.rect.left = player1.rect.right
			self.speed_x *= -1
		if self.rect.colliderect(player2.rect):
			self.rect.right = player2.rect.left
			self.speed_x *= -1

	def reset_position(self):
		self.rect.x = self.initial_x
		direction = [0, 1]
		angle = [0, 1, 2]
		dir = random.choice(direction)
		ang = random.choice(angle)
		if dir == 0:
			if ang == 0:
				self.speed_x = -7.0
				self.speed_y = 3.5
			if ang == 1:
				self.speed_x = -3.5
				self.speed_y = 3.5
			if ang == 2:
				self.speed_x = -3.5
				self.speed_y = 7.0
		if dir == 1:
			if ang == 0:
				self.speed_x = 7.0
				self.speed_y = 3.5
			if ang == 1:
				self.speed_x = 3.5
				self.speed_y = 3.5
			if ang == 2:
				self.speed_x = 3.5
				self.speed_y = 7.0
		self.rect.y = random.randint(50, 550)
		self.speed_x = self.initial_speed_x * random.choice([-1, 1])
		self.speed_y = self.initial_speed_y * random.choice([-1, 1])

