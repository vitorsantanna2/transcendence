from django.shortcuts import render, get_object_or_404
from .models import Game

def index(request):
    return render(request, 'main/index.html')

def perfil(request):
    return render(request, 'main/perfil.html')

def login(request):
    return render(request, 'main/login.html')

def registration(request):
    return render(request, 'main/registration.html')

def configuration(request):
    return render(request, 'main/configuration.html')

def game(request):
    return render(request, 'main/game.html')

def tournament(request):
    return render(request, 'main/tournament.html')

def base(request):
    return render(request, 'main/base.html')

def chat(request):
    return render(request, 'main/chat.html')

def tournamentRoom(request):
    return render(request, 'main/tournamentRoom.html')

def inGame(request):
    return render(request, 'main/inGame.html')

def game_id(request, game_id):
    game_instance = get_object_or_404(Game, id=game_id)
    return render(request, 'main/inGame.html', {'game_instance': game_instance})
