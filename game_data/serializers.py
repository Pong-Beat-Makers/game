from rest_framework import serializers
from .models import *

class GameDataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GameDataModel
        fields = "__all__"
