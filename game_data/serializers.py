from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import *

class GameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ('user_id', 'nickname')


class GameDataSerializer(serializers.ModelSerializer):
    user1_id = serializers.SerializerMethodField()
    user1_nickname = serializers.SerializerMethodField()
    user2_id = serializers.SerializerMethodField()
    user2_nickname = serializers.SerializerMethodField()

    class Meta(object):
        model = GameDataModel
        fields = ('id', 'user1_id', 'user1_nickname', 'user1_score', 'user2_id',
                  'user2_nickname', 'user2_score', 'match_type', 'created_at')

    def get_user1_id(self, obj):
        return obj.user1.user_id if obj.user1 else None
    def get_user1_nickname(self, obj):
        return obj.user1.nickname if obj.user1 else None
    def get_user2_id(self, obj):
        return obj.user2.user_id if obj.user2 else None
    def get_user2_nickname(self, obj):
        return obj.user2.nickname if obj.user2 else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['nickname'] == data['user2_nickname']:
            data['user1_id'], data['user2_id'] \
                = data['user2_id'], data['user1_id']
            data['user1_nickname'], data['user2_nickname'] \
                = data['user2_nickname'], data['user1_nickname']
            data['user1_score'], data['user2_score'] \
                = data['user2_score'], data['user1_score']
        return data

