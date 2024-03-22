from django.db import models, transaction
from django.utils import timezone

# Create your models here.

class GameUser(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    nickname = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'game_user'

class GameDataModel(models.Model):
    created_at = models.DateTimeField()
    user1 = models.ForeignKey(GameUser, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(GameUser, on_delete=models.CASCADE, related_name="user2")
    user1_score = models.IntegerField(default=0)
    user2_score = models.IntegerField(default=0)
    match_type = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'game_data'

    @staticmethod
    def create_match_and_save_game(game_info: dict):
        user1 = GameUser.objects.get(nickname=game_info["user1_nickname"])
        user2 = GameUser.objects.get(nickname=game_info["user2_nickname"])
        user1_score = game_info["user1_score"]
        user2_score = game_info["user2_score"]
        match_type = game_info["match_type"]

        GameDataModel.objects.create(
            created_at=timezone.now(),
            user1=user1,
            user2=user2,
            user1_score=user1_score,
            user2_score=user2_score,
            match_type=match_type,
        )