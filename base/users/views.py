from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

# Create your views here.

def login(request):
	return render(request, "login.html")

def register(request):
	timestamp = datetime.now().timestamp()
	return render(request, "register.html", {"timestamp": timestamp})