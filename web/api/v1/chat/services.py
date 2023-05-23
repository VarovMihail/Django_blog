from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTHandler:
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            print(access_token['user_id'])
            return User.objects.get(id=user_id)
        except (User.DoesNotExist, TokenError):
            return None


