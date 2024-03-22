import requests, os
from rest_framework import exceptions

from game_data.models import GameUser
from game_data.serializers import GameUserSerializer


def verifying_user(access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(os.environ.get('USER_MANAGEMENT_SERVER') + f's2sapi/user-management/user-api/verify/', headers=headers)

    if response.status_code != 200:
        raise exceptions.AuthenticationFailed('token is invalid')
    user_id = response.json()['id']
    nickname = response.json()['nickname']
    try:
        GameUser.objects.get(user_id=user_id)
        return response.json()
    except GameUser.DoesNotExist:
        data = {
            'user_id': user_id,
            'nickname': nickname,
        }
        serializer = GameUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return response.json()
