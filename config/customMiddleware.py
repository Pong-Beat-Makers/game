import requests

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.headers.get('Authorization').split()[1]
        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get("http://127.0.0.1:8000/user/token", headers=headers)
        response = self.get_response(request)
        return response