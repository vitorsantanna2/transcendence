from django.shortcuts import render, redirect
import bcrypt
import os
from users.models import UserPong
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from twilio.rest import Client
from .auth import CheckUserExists, ValidateUserInput
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def loginUser(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    if not ValidateUserInput(username, password):
        return Response({"message": "Invalid username or password"}, status=400)
    
    user = authenticate(username=username, password=password)
    if user:
        # refresh = RefreshToken.for_user(user)
        # access_token = str(refresh.access_token)
        return  Response(
            {"message": "proceed to ask for 2fa password", "user_id": user.id},
            status=200,
        )
    return Response({"message": "Invalid username or password"}, status=400)


@api_view(["POST"])
def twoFactorAuth(request):
    # PLS HELP - this request should only be able to be made by our front-end not any other source!!!
    # this is important for security pourposes. please note this.
    data = JSONParser().parse(request)
    two_fa_code = data["twoFA"]
    user_id = data["user_id"]
    verf_service = os.getenv("VERIFICATION_SERVICE")

    if not user_id:
        return Response(b"no user id provided.", status=500)

    if not verf_service:
        return Response(
            b"Internal server error verification service not found", status=500
        )

    user = UserPong.objects.filter(id=user_id).first()
    if not user:
        return Response(b"Invalid user_id", status=400)

    twilio_client = Client(os.getenv("ACCOUNT_SID"), os.getenv("auth_token"))
    verification_check = twilio_client.verify.v2.services(
        verf_service
    ).verification_checks.create(to=user.phoneNumber, code=two_fa_code)

    if verification_check.status != "approved":
        return Response(b"Authentication failed!", status=401)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    # del request.session["2fa_user_id"]
    # login(request, user)
    return Response(
        {"message": "Authentication failed!", "access_token": access_token}, status=200
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):

	if request.method == "POST":
		data = request.data
		name = data.get("name")
		username = data.get("username")
		email = data.get("email")
		password = data.get("password")
		confirm_pass = data.get("password2")
		phonenumber = data.get("phoneNumber")

		if CheckUserExists(username, email):
			return Response(b"User already exists", status=409)

		if password != confirm_pass:
			return Response(b"Passwords do not match", status=400)

		user = UserPong(
			name=name,
			username=username,
			email=email,
			password=password,
			phoneNumber=phonenumber,
		)

		user.save()
  
		user_data = {
			"id": user.id,
			"name": user.name,
			"username": user.username,
			"email": user.email,
			"phoneNumber": user.phoneNumber,
		}
		return Response(user_data, status=201)

	return Response(b"Invalid request", status=400)


# @api_view(["GET"])
# def home_page(request):
#     return render(request, "home.html")
