from .game.player import Player, AutoPlayer

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