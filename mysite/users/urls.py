from django.urls import path
from . import views
from .twofactor import twoFactorAuth

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        "register/", views.registerUser, name="register"
    ),  # maybe we won't need to change this
    path("login/", views.loginUser, name="login"),
    path("twofa/", views.twoFactorAuth, name="twofa"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
