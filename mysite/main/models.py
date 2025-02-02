from django.db import models
from users.models import UserPong


class Match(models.Model):
    game_id = models.CharField(max_length=50, primary_key=True)
    is_active = models.BooleanField(default=True)
    game_type = models.CharField(max_length=50, default="local")
    player_1 = models.ForeignKey(UserPong, on_delete=models.CASCADE, related_name="p1")
    player_2 = models.ForeignKey(
        UserPong,
        on_delete=models.CASCADE,
        related_name="p2",
        null=True,  # Allow null for games against an AI
        blank=True,  # Allow blank values in forms/admin
    )
    p1_score = models.IntegerField(default=0)
    p2_score = models.IntegerField(default=0)

    def __str__(self):
        if self.player_2:
            return f"Match {self.game_id} between {self.player_1} and {self.player_2}"
        return f"Match {self.game_id} with {self.player_1} vs AI"
