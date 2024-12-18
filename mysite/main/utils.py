from .game.player import Player, AutoPlayer

def insertDirectoryPath(base, path , type):
	destiny = []
	for app in base:
		temp = path / app / type
		if temp.exists():
			destiny.append(temp)
	return destiny

def create_player(x_pos, y_pos, speed, width, height, player_id, mode, canvas_width, canvas_height):
    if mode == 'local':
        return AutoPlayer(x_pos, y_pos, speed, width, height, player_id, canvas_width, canvas_height)
    else:
        return Player(x_pos, y_pos, speed, width, height, player_id, canvas_width, canvas_height)