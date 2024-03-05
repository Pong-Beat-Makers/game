from rest_framework import exceptions
import requests

def verfying_user(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get('http://127.0.0.1:8000/api/verify', headers=headers)

    if response.status_code != 200:
        return False
    return True