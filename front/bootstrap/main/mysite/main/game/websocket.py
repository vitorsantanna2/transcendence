import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class PongGame:
    def __init__(self):
        self.channel_layer = get_channel_layer()

    def send_game_state(self, game_state):
        async_to_sync(self.channel_layer.group_send)(
            'pong_group',
            {
                'type': 'game.update',
                'message': game_state
            }
        )

    def handle_command(self, command):
        # Process the command and update the game state
        if command['action'] == 'move_up':
        # Move the player up
            pass
        elif command['action'] == 'move_down':
            # Move the player down
            pass
