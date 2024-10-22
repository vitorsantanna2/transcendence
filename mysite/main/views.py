from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

# def game(request, game_id):
#     return render(request, 'main/game.html', {'game_id': game_id})
