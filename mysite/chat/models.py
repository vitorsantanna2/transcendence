# chat/models.py 

from django.db import models
from django.conf import settings  # Import for AUTH_USER_MODEL
from django.utils import timezone

class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically reference the custom user model
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    room_name = models.CharField(max_length=255)  # e.g., "room1" or "general"
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.room_name}] {self.author}: {self.content}"

class Friendship(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_initiated'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: status, requested_at, accepted_at, etc.
    # status = models.CharField(max_length=50, default='accepted')  

    class Meta:
        unique_together = ('user1', 'user2')  # no duplicate pairs

    def __str__(self):
        return f"{self.user1.username} & {self.user2.username} are friends"

