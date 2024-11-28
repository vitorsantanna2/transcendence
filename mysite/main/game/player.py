class Player:
	def __init__(self, x_pos, y_pos, speed, width, height, player_id):
		self.speed = speed
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.width = width
		self.height = height
		self.score = 0
		self.rounds = 0
		self.player_id = player_id
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
    def __init__(self, x_pos, y_pos, speed, width, height, player_id):
        super().__init__(x_pos, y_pos, speed, width, height, player_id)
        self.target = y_pos
        self.delay = 0

    def predict_ball(self, ball, screen_width, screen_height):
        position_x = ball.x
        position_y = ball.y
        velocity_x = ball.speed_x
        velocity_y = ball.speed_y

        while 0 < position_x < screen_width:
            position_x += velocity_x
            position_y += velocity_y
            if position_y <= 0 or position_y >= screen_height:
                velocity_y *= -1

        return position_y

    def movement(self, ball, screen_width, screen_height):
        player_center = self.height // 2

        if self.delay > 0:
            self.delay -= 1
        else:
            self.target = self.predict_ball(ball, screen_width, screen_height)
            self.delay = 100

        if self.centery < self.target - player_center and self.bottom < screen_height:
            self.y_pos += self.speed
        elif self.centery > self.target + player_center and self.top > 0:
            self.y_pos -= self.speed

    @property
    def centery(self):
        return self.y_pos + self.height // 2

    @property
    def top(self):
        return self.y_pos

    @property
    def bottom(self):
        return self.y_pos + self.height