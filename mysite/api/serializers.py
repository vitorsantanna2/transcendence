from rest_framework import serializers
from . import models

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserConversation
        fields = ['id','user1', 'user2', 'created_at']
