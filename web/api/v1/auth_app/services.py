from typing import TYPE_CHECKING, NamedTuple, Optional
from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives  #1
from django.db import transaction
from django.template.loader import render_to_string   #2
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.email_services import BaseEmailHandler
from main.decorators import except_shell
from main.tasks import send_information_email

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str


class ConfirmationEmailHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    FRONTEND_PATH = '/confirm'
    TEMPLATE_NAME = 'emails/verify_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'key': self.user.confirmation_key,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'activate_url': self._get_activate_url(),
            },
        }


class UserService:     # класс для обработки всей логики, связанной с юзером
    @staticmethod                                       # зачем? нам нужно будет у объекта его вызывать?
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()  # почему не get? Будет ошибка

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @transaction.atomic()
    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data) # зачем именованый кортеж? Для наглядности user?
        print(f'{data=}')
        print(f'{validated_data=}')
        user = User.objects.create_user(
            email=data.email,
            password=data.password_1,
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=False
        )
        return user

class VerifyEmail:

    def verify_email(self, key: str):
        user = User.get_user_from_key(key)
        print(f'{user = }')
        if not user:
            raise ValidationError('Invalid key')
        if user.is_active:
            raise ValidationError('User is already activated')
        user.is_active = True
        user.save(update_fields=['is_active'])


    def get_activate_url(self, user: User):
        url = reverse('auth_app:account_verification')
        full_url = urljoin(base=settings.FRONTEND_URL, url=url)
        return f"{full_url}?key={user.confirmation_key}"

    def send_email(self, user: User):   # https://django.fun/ru/docs/django/3.1/topics/email/
        data = {'first_name': user.first_name,
                'last_name': user.last_name,
                'key': user.confirmation_key,
                'activate_url': self.get_activate_url(user)
                }

        html_content = render_to_string('auth_app/email/mail_message.html', data)
        message = EmailMultiAlternatives(subject='Подтверждение регистрации', to=[user.email])
        message.attach_alternative(html_content, 'text/html')
        message.send()

class PasswordRecoveryEmail:

    def get_user_from_key(self, uid: str):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User._default_manager.get(pk=uid)        # а так можно? Защищенный метод
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user

    def verify_email(self, token: str, uid: str):
        print(f'{token = } {uid = }')
        user = self.get_user_from_key(uid)
        print(user)
        if not default_token_generator.check_token(user, token):
            raise ValidationError('Invalid key')


    def get_password_recovery_url(self, user: User):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('auth_app:reset_email_sent')
        full_url = urljoin(base=settings.FRONTEND_URL, url=url)
        return f"{full_url}?uid={uid}&token={token}"

    def send_password_recovery_email(self, user: User):
        data = {'first_name': user.first_name,
                'last_name': user.last_name,
                'activate_url': self.get_password_recovery_url(user)
                }
        print(data)

        html_content = render_to_string('auth_app/email/mail_reset_password.html', data)
        message = EmailMultiAlternatives(subject='Восстановление пароля', to=[user.email])
        message.attach_alternative(html_content, 'text/html')
        message.send()




def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    if cookie_name := getattr(settings, 'JWT_AUTH_COOKIE', None):
        response.delete_cookie(cookie_name)
    refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
        # add refresh token to blacklist
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except KeyError:
            response.data = {"detail": _("Refresh token was not included in request data.")}
            response.status_code = status.HTTP_401_UNAUTHORIZED
        except (TokenError, AttributeError, TypeError) as error:
            if hasattr(error, 'args'):
                if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                    response.data = {"detail": _(error.args[0])}
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                else:
                    response.data = {"detail": _("An error has occurred.")}
                    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = status.HTTP_200_OK
    return response






