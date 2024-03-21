from config.verifying_user import verifying_user
# 인증 서버에서 인증 받아 오는 함수,
def authenticate(token):
    try:
        return verifying_user(token)
    except:
        return None

