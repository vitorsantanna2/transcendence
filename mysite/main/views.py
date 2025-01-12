from django.shortcuts import render, redirect, get_object_or_404
from .models import Match
import uuid
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/auth/login/')
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

def localgame(request):
    game_id = str(uuid.uuid4())
    Match.objects.create(game_id=game_id, is_active=True, game_type='local')
    return redirect('local_id', game_id=game_id)

def onlinegame(request):
    game_id = str(uuid.uuid4())
    Match.objects.create(game_id=game_id, is_active=True, game_type='online')
    return redirect('online_id', game_id=game_id)

def local_id(request, game_id):
    return render(request, 'main/localgame.html', {'game_id': game_id})

def online_id(request, game_id):
    return render(request, 'main/onlinegame.html', {'game_id': game_id})
