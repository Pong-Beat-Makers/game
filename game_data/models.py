from django.db import models
from django.utils import timezone

# Create your models here.
class RandomMatchModel(models.Model):
    date = models.DateField(default=timezone.now)
    user1_id = models.IntegerField(default=0)
    user2_id = models.IntegerField(default=0)