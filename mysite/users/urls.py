from django.urls import path
from . import views
from .twofactor import twoFactorAuth

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("twofa/", twoFactorAuth, name="twofa"),
    path("register/", views.registerUser, name="register"),
]
