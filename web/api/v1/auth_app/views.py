from dj_rest_auth import views as auth_views
from django.contrib.auth import logout as django_logout
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from . import serializers
from .services import PasswordRecoveryEmail, User, UserService, VerifyEmail, full_logout, GithubHandler


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_service = UserService()
        user = user_service.create_user(serializer.validated_data)
        mail = VerifyEmail()
        mail.send_email(user)
        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mail = VerifyEmail()
        mail.verify_email(key=serializer.data['key'])

        return Response(
            {'detail': _('Email verified')},
            status=status.HTTP_200_OK,
        )


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data['email'])
        mail = PasswordRecoveryEmail()
        mail.send_password_recovery_email(user)
        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mail = PasswordRecoveryEmail()
        user = mail.verify_email(token=serializer.data['token'], uid=serializer.data['uid'])
        mail.change_user_password(user, serializer.data['password_1'])
        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )


class GithubInitView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        data = {
            'client_id': settings.SOCIALACCOUNT_PROVIDERS['github']['APP']['client_id_2'],
            'redirect_uri': 'http://localhost:8008/callback/github',
            'scope': 'user email user:email',
            #'scope': 'user:email',
           # 'login': '8605495@mail.ru',
            'state': 'abcd',
        }
        return Response(data)


class GithubCallbackView(GenericAPIView):
    serializer_class = serializers.GithubCallbackSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = GithubHandler()
        access_token = service.get_access_token(serializer.data['code'])
        print(access_token)
        user_data = service.get_user_data(access_token)
        return Response({})
