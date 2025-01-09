from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import bcrypt
import os
from users.models import UserPong
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from twilio.rest import Client
from .auth import CheckUserExists, ValidateUserInput
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


def loginUser(request):
	if request.method == "GET":
		return render(request, "login.html")

	username = request.POST.get("username")
	password = request.POST.get("password")

	if not ValidateUserInput(username, password):
		return HttpResponse(b"Invalid username or password", status=400)
	
	user = authenticate(username=username, password=password)

	if user:
		refresh = RefreshToken.for_user(user)
		access_token = str(refresh.access_token)

	return HttpResponse(b"Invalid username or password", status=400)

def twoFactorAuth(request):
	if request.method == "POST":
		form_code = request.POST.get("twoFA")
		user_id = request.session["2fa_user_id"]
		verf_service = os.getenv("VERIFICATION_SERVICE")
		if not verf_service:
			return HttpResponse(
				b"Internal server error verification service not found", status=500
			)

		if not user_id:
			return HttpResponse(b"Internal server error lost user_id", status=500)

		
		user = User.objects.filter(id=user_id).first()
		twilio_client = Client(os.getenv("ACCOUNT_SID"), os.getenv("auth_token"))

		verification_check = twilio_client.verify.v2.services(
			verf_service
		).verification_checks.create(to=user.phoneNumber, code=form_code)

		if verification_check.status != "approved":
			return HttpResponse(b"Authentication failed!", status=401)

		del request.session["2fa_user_id"]
		login(request, user)
		return redirect("/auth/home")

	else:
		return render(request, "twofa.html")


def register(request):
	if request.method == "GET":
		return render(request, "register.html")

	name = request.POST.get("name")
	username = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password")
	confirm_pass = request.POST.get("password2")
	phonenumber = request.POST.get("phonenumber")


	if CheckUserExists(username, email):
		return HttpResponse(b"User already exists", status=409)
	
	if password != confirm_pass:
		return HttpResponse(b"Passwords do not match", status=400)

	user = UserPong(
		name=name,
		username=username,
		email=email,
		password=password,
		phoneNumber=phonenumber,
	)

	user.save()

	return redirect("/auth/login")


@login_required(login_url="/auth/login")
def home_page(request):
	return render(request, "home.html")
