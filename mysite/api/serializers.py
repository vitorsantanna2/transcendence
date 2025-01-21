from rest_framework import serializers
from . import models
from users.models import UserPong

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserConversation
        fields = ['id','user1', 'user2', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserMessage
        fields = ['id', 'conversation', 'text', 'sender', 'receiver', 'created_at']

class UserPongSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPong
        fields = [
            "id",
            "name",
            "username",
            "email",
            "phoneNumber",
            "profile_image",
        ]
        read_only_fields = ["id", "username", "email"]
