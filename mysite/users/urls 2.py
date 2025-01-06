from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("twofa/", views.twoFactorAuth, name="twofa"),
    path("register/", views.register, name="register"),
]
