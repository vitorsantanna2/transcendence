from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def login(request):
	return render(request, "login.html")

def register(request):
	if request.method == "GET":
		return render(request, "register.html")
	else:
		username = request.POST.get("username")
		password = request.POST.get("password")
		email = request.POST.get("email")
		return HttpResponse(f"User {username} registered with {email} email")