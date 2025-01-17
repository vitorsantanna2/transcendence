from django.urls import path
from . import views

urlpatterns = [
    # Conversations #
    path('conversations/create_convers/', views.CreateConversation, name='create_conversation'),
    path('conversations/create_messag/', views.CreateMessage, name='create_message'),
]
