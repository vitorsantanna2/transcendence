from django.shortcuts import render

# Create your views here.

# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")
