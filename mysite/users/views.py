from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, get_user_model
from users.models import UserPong
from .auth import CheckUserExists
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt
import os
from twilio.rest import Client
from django.conf import settings
from rest_framework.decorators import permission_classes

User = get_user_model()

@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # user = authenticate(username=username, password=password)
        user = UserPong.objects.filter(username=username).first()
        if user:
            # Send 2FA code via Twilio
            twilio_client = Client(
                settings.ACCOUNT_SID, settings.AUTH_TOKEN
            )
            twilio_client.verify.services(
                settings.VERIFICATION_SERVICE
            ).verifications.create(to=user.phoneNumber, channel="sms")

            # Return user ID to frontend
            return Response(
                {"message": "2FA code sent to your phone.", "user_id": user.id},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

@permission_classes([AllowAny])
class TwoFactorAuthView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        code = request.data.get("code")

        if not user_id or not code:
            return Response(
                {"error": "User ID and code are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieve user
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Verify 2FA code via Twilio
        twilio_client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        verification_check = twilio_client.verify.services(
            settings.VERIFICATION_SERVICE
        ).verification_checks.create(to=user.phoneNumber, code=code)

        if verification_check.status != "approved":
            return Response(
                {"error": "Invalid 2FA code."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

@permission_classes([AllowAny])
class RegisterView(APIView):
    def post(self, request):
        name = request.data.get("name")
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_pass = request.data.get("password2")
        phone_number = request.data.get("phonenumber")

        if CheckUserExists(username, email):
            return Response(
                {"error": "User already exists"}, status=status.HTTP_409_CONFLICT
            )

        if password != confirm_pass:
            return Response(
                {"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
            )

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = UserPong(
            name=name,
            username=username,
            email=email,
            password=hashed.decode("utf-8"),
            phoneNumber=phone_number,
        )
        user.save()

        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )


class HomePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"message": "Welcome to the home page!"}, status=status.HTTP_200_OK
        )
