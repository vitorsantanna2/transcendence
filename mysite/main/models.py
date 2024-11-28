from django.db import models

class Match(models.Model):
    game_id = models.CharField(max_length=50, primary_key=True)
    is_active = models.BooleanField(default=True)
    game_type = models.CharField(max_length=50, default='localgame')

    def __str__(self):
        return f"Match {self.match_id} between {self.user1} and {self.user2}"