# chat/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room_name = models.CharField(max_length=255)        # e.g., "room1" or "general"
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.room_name}] {self.author}: {self.content}"
