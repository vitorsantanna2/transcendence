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