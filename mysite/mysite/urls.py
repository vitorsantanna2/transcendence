"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('configuration/', views.configuration, name='configuration'),
    path('game/', views.game, name='game'),
    path('tournament/', views.tournament, name='tournament'),
    path('base/', views.base, name='base'),
    path('chat/', views.chat, name='chat'),
    path('tournamentRoom/', views.tournamentRoom, name='tournamentRoom'),
    path('localgame/', views.localgame, name='localgame'),
    path('localgame/<str:game_id>/', views.local_id, name='local_id'),
    path('onlinegame/', views.onlinegame, name='onlinegame'),
    path('onlinegame/<str:game_id>/', views.online_id, name='online_id')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)