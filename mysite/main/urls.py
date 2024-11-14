from django.urls import path
from . import views
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
    path('inGame/', views.inGame, name='inGame'),
    path('inGame/<str:game_id>/', views.game_id, name='game_id')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)