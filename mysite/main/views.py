import uuid

from django.shortcuts import
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from users.models import UserPong
from .models import Match

@permission_classes([IsAuthenticated])
class LocalGameView(APIView):
    def post(self, request):
        user = request.user
        game_id = str(uuid.uuid4())
        
        # Create the match for a local game against an AI (player_2 is not set)
        Match.objects.create(
            game_id=game_id,
            is_active=True,
            game_type="local",
            player_1=user,
            # player_2 is intentionally left as None for an AI opponent.
        )
        
        return Response(
            {"game_id": game_id},
            status=status.HTTP_201_CREATED,
        )


@permission_classes([IsAuthenticated])
class OnlineGameView(APIView):

    def post(self, request):
        user = request.user
        # Extract the opponent's user id from the JSON payload
        opponent_user_id = request.data.get("opponent_user")
        if not opponent_user_id:
            return Response(
                {"error": "Opponent user ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieve the opponent user object from the database
        opponent_user = get_object_or_404(UserPong, pk=opponent_user_id)

        game_id = str(uuid.uuid4())
        # Create the match with both players set.
        Match.objects.create(
            game_id=game_id,
            is_active=True,
            game_type="online",
            player_1=user,
            player_2=opponent_user
        )
        
        return Response(
            {"game_id": game_id},
            status=status.HTTP_201_CREATED,
        )

def local_id(request, game_id):
    return render(request, "main/localgame.html", {"game_id": game_id})


def online_id(request, game_id):
    return render(request, "main/onlinegame.html", {"game_id": game_id})


## OLD!!!
def index(request):
    return render(request, "main/index.html")


def perfil(request):
    return render(request, "main/perfil.html")


def login(request):
    return render(request, "main/login.html")


def registration(request):
    return render(request, "main/registration.html")


def configuration(request):
    return render(request, "main/configuration.html")


def game(request):
    return render(request, "main/game.html")


def tournament(request):
    return render(request, "main/tournament.html")


def base(request):
    return render(request, "main/base.html")


def chat(request):
    return render(request, "main/chat.html")


def tournamentRoom(request):
    return render(request, "main/tournamentRoom.html")
