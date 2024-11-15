from django.http import HttpResponse
from django.shortcuts import render, redirect
import bcrypt
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.

def login_page(request):

	if (request.method == "POST"):
		username = request.POST.get("username")
		password = request.POST.get("password")

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
	if request.method == "GET":
		return render(request, "register.html")
	
	name = request.POST.get("name")
	username = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password")
	confirm_pass = request.POST.get("password2")


	user = User.objects.filter(username=username)

	if user:
		return HttpResponse("User already exists", status=400)
	
	if password != confirm_pass:
		return HttpResponse("Passwords do not match", status=400)
	
	hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

	user = User(name=name, username=username, email=email, password=hashed.decode("utf-8"))
	user.save()

	return redirect("/auth/login")

@login_required(login_url="/auth/login")
def home_page(request):
	return render(request, "home.html")