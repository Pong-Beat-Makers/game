from django.db import models

# Create your models here.
class TournamentTable(models.Model):
    player1 = models.CharField(max_length=20)
    player2 = models.CharField(max_length=20)
    player3 = models.CharField(max_length=20)
    player4 = models.CharField(max_length=20)

    winner1 = models.CharField(max_length=20, null=True)
    winner2 = models.CharField(max_length=20, null=True)
