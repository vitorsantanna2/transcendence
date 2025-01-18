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

