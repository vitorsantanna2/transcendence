from django.db import models

class Match(models.Model):
    game_id = models.CharField(max_length=50, primary_key=True)
    # user1 = models.ForeignKey('auth.User', related_name='user1_matches', on_delete=models.CASCADE)
    # user2 = models.ForeignKey('auth.User', related_name='user2_matches', on_delete=models.CASCADE)
    # user1_score = models.IntegerField(default=0)
    # user2_score = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Match {self.match_id} between {self.user1} and {self.user2}"