from django.urls import path
from . import views

urlpatterns = [
    # Conversations #
    path('conversations/create/', views.CreateConversation, name='create_conversation'),
]
