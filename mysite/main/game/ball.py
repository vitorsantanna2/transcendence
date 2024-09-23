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

    def movement(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def collision(self):
        if self.y <= 0 + self.radius or self.y >= self.height - self.radius:
            self.speed_y *= -1
        if self.x <= 0 + self.radius or self.x >= self.width - self.radius:
            self.speed_x *= -1
        if self.x <= 0 + self.radius or self.x >= self.width - self.radius:
            self.reset_position()

    #     if self.x <= 0 + self.radius:
    #         # player2.score += 1
    #         # if player2.score == game_score:
    #         #     player2.rounds += 1
    #         #     player1.score = 0
    #         #     player2.score = 0
    #         self.reset_position()
    #         print(f"Collision with left wall: speed_x={self.speed_x}, speed_y={self.speed_y}")

    #     if self.x >= self.width - self.radius:
    #         # player1.score += 1
    #         # if player1.score == game_score:
    #         #     player1.rounds += 1
    #         #     player1.score = 0
    #         #     player2.score = 0
    #         self.reset_position()
    #         print(f"Collision with right wall: speed_x={self.speed_x}, speed_y={self.speed_y}")

    #     if (self.x - self.radius <= player1.x + player1.width and
    #         self.y >= player1.y and self.y <= player1.y + player1.height):
    #         self.x = player1.x + player1.width + self.radius
    #         self.speed_x *= -1
    #         print(f"Collision with player1: speed_x={self.speed_x}")

    #     if (self.x + self.radius >= player2.x and
    #         self.y >= player2.y and self.y <= player2.y + player2.height):
    #         self.x = player2.x - self.radius
    #         self.speed_x *= -1
    #         print(f"Collision with player2: speed_x={self.speed_x}")

    def reset_position(self):
        self.x = self.initial_x
        self.y = random.randint(50, self.height - 50)
    
        directions = [-1, 1]
        angles = [(7.0, 3.5), (3.5, 3.5), (3.5, 7.0)]
    
        dir = random.choice(directions)
        speed_x, speed_y = random.choice(angles)
    
        self.speed_x = dir * speed_x
        self.speed_y = speed_y if random.choice([True, False]) else -speed_y
    
        if abs(self.speed_x) < 1:
            self.speed_x = self.initial_speed_x * random.choice([-1, 1])
        if abs(self.speed_y) < 1:
            self.speed_y = self.initial_speed_y * random.choice([-1, 1])