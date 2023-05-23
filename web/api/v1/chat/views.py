from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .serializers import CheckUserTokenSerializer, JWTUserSerializer
from .services import JWTHandler


class OpenChatView(APIView):
    def get(self, request):
        jwt = request.COOKIES[settings.JWT_AUTH_COOKIE]
        user_id = request.query_params['user_id']
        url = f'{settings.CHAT_URL}/chat/init/?jwt={jwt}&user_id={user_id}'
        data = {
            'url': url
        }
        print(f'{request.COOKIES}')
        return Response(data)


class CheckUserTokenView(GenericAPIView):
    serializer_class = CheckUserTokenSerializer
    permission_classes = ()

    def post(self, request):
        print(f'{request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = JWTHandler().get_user_from_token(serializer.data['jwt'])
        if not user:
            raise ValidationError('User Does Not Exist')
        serializer = JWTUserSerializer(user, context=self.get_serializer_context())
        return Response(serializer.data)


