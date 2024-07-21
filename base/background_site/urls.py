from django.urls import path
from . import views

app_name = "background_site"

urlpatterns = [
	path("", views.home, name="home"),
]