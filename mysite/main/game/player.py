class Player:
	def __init__(self, x_pos, y_pos, speed, width, height, player_id, canvas_width, canvas_height):
		self.speed = speed
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.width = width
		self.height = height
		self.score = 0
		self.rounds = 0
		self.player_id = player_id
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
		self.connected = False

	def move_up(self):
		if self.y_pos > 0:
			self.y_pos -= self.speed

	def move_down(self):
		if self.y_pos < 600 - self.height:
			self.y_pos += self.speed

	def reset_position(self, y_position):
		self.y_pos = y_position

class AutoPlayer(Player):
	def __init__(self, x_pos, y_pos, speed, width, height, player_id, canvas_width, canvas_height):
		super().__init__(x_pos, y_pos, speed, width, height, player_id, canvas_width, canvas_height)
		self.target = y_pos
		self.delay = 0

	def predict_ball_position(self, ball, screenWidth, screenHeight):
		pos_x = ball.x
		pos_y = ball.y
		velocity_x = ball.speed_x
		velocity_y = ball.speed_y

		while 0 < pos_x < screenWidth:
			pos_x += velocity_x
			pos_y += velocity_y
			if pos_y <= 0 or pos_y >= screenHeight:
				velocity_y *= -1
		return pos_y
	
	def movement(self, ball, screen_width, screen_height, difficulty):
		player_center = self.height // 2
				
		if self.delay > 0:
			self.delay -= 1
		else:
			self.target = self.predict_ball_position(ball, screen_width, screen_height)
			if difficulty == "easy":
				self.delay = 50
			elif difficulty == "medium":
				self.delay = 70
			elif difficulty == "hard":
				self.delay = 100

		if self.centery < self.target - player_center and self.bottom < 600:
			self.y_pos += self.speed
		elif self.centery > self.target + player_center and self.top > 0:
			self.y_pos -= self.speed
				
		if self.y_pos + self.height > 600:
			self.y_pos = 600 - self.height

	@property
	def centery(self):
		return self.y_pos + self.height // 2

	@property
	def top(self):
		return self.y_pos

	@property
	def bottom(self):
		return self.y_pos + self.height