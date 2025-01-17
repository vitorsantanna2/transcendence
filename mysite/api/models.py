from django.conf import settings
from django.db import models
import uuid
from users.models import UserPong

class UserConversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_initiated'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.user1} and {self.user2}"

class UserMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(UserConversation, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(UserPong, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(UserPong, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self):
        return f"Message of {self.sender.username} to {self.receiver.username} - {self.created_at}"
