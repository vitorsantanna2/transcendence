from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
import bcrypt
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.

def login_page(request):

	if (request.method == "POST"):
		username = request.POST.get("username")
		password = request.POST.get("password")

		print(username)
		print(password)

		user = User.objects.filter(username=username).first()

		if user is not None:
			if not (bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))):
				return HttpResponse("Authentication failed! Invalid username or password", status=401)
			login(request, user)
			return redirect("/auth/home")
		else:
			return HttpResponse("Authentication failed! Invalid username or password", status=401)
	else:
		return render(request, "login.html")

def register(request):
	timestamp = datetime.now().timestamp()
	if (request.method == "GET"):
		return render(request, "register.html", {"timestamp": timestamp})

	name = request.POST.get("name")
	username = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password")
	confirmed_password = request.POST.get("confirmed_password")

	user = User.objects.filter(username=username).exists()

	if user:
		return HttpResponse("Username already exists!", status=409)

	if (password != confirmed_password):
		return HttpResponse("Passwords do not match!", status=400)
	
	hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) # Hash password insert
	
	user = User.objects.create(name=name, username=username, email=email, password=hash_password.decode("utf-8"))
	user.save()

	return redirect("/auth/login")

@login_required(login_url="/auth/login")
def home_page(request):
	return render(request, "home.html")