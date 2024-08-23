from django.urls import path
from . import views

urlpatterns = [
	path("login/", views.login_page, name="login"),
	path("register/", views.register, name="register"),
	path("home/", views.home_page, name="home"),
]