from django.shortcuts import render, redirect
from django.db import transaction
from .models import Match
import uuid

def get_id():
    return str(uuid.uuid4())

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
    game_id = get_id()
    while Match.objects.filter(game_id=game_id).exists():
        game_id = get_id()
    match = Match.objects.create(game_id=game_id, is_active=True)
    return redirect('game_id', game_id=game_id)

def game_id(request, game_id):
    return render(request, 'main/inGame.html', {'game_id': game_id})
