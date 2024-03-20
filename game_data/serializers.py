from rest_framework import serializers
from .models import *

class GameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = '__all__'

class GameDataSerializer(serializers.ModelSerializer):
    user1_nickname = serializers.CharField(source='user1__nickname', read_only=True)
    user2_nickname = serializers.CharField(source='user2__nickname', read_only=True)
    class Meta(object):
        model = GameDataModel
        fields = ('id', 'user1_nickname', 'user2_nickname', 'user1_score', 'user2_score', 'match_type', 'created_at')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['nickname'] == data['user2_nickname']:
            data['user1_nickname'], data['user2_nickname'] = data['user2_nickname'], data['user1_nickname']
            data['user1_score'], data['user2_score'] = data['user2_score'], data['user1_score']
        return data

