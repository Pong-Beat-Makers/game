from rest_framework import serializers
from .models import *

class GameDataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GameDataModel
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['nickname'] == data['user2_nickname']:
            data['user1_nickname'], data['user2_nickname'] = data['user2_nickname'], data['user1_nickname']
            data['user1_score'], data['user2_score'] = data['user2_score'], data['user1_score']
        return data

