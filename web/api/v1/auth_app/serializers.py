from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from main.models import UserType
from api.v1.auth_app.services import UserService
from django.conf import settings

User: UserType = get_user_model()

error_messages = {
    'not_verified': _('Email not verified'),
    'not_active': _('Your account is not active. Please contact Your administrator'),
    'wrong_credentials': _('Entered email or password is incorrect'),
    'already_registered': _('User is already registered with this e-mail address'),
    'password_not_match': _('The two password fields did not match'),
}


class UserSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=100)
    last_name = serializers.CharField(min_length=2, max_length=100)
    email = serializers.EmailField()
    password_1 = serializers.CharField(write_only=True, min_length=8)
    password_2 = serializers.CharField(write_only=True, min_length=8)
    gender = serializers.ChoiceField(choices=User.Gender.choices, required=False, default=User.Gender.UNKNOWN)
    birthday = serializers.DateField(required=False)

    def validate_password_1(self, password: str):
        validate_password(password)
        return password

    def validate_email(self, email: str) -> str:
        if UserService.is_user_exist(email):
            raise serializers.ValidationError(_('User is already registered with this e-mail address.'))
        return email

    def validate(self, data: dict):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError({'password_2': error_messages['password_not_match']})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, data: dict):
        email = data.get('email')
        password = data.get('password')
        user = self.authenticate(email=email, password=password)
        if not user:
            user = UserService.get_user(email)
            if not user:
                msg = {'email': error_messages['wrong_credentials']}
                raise serializers.ValidationError(msg)
            if not user.is_active:
                msg = {'email': error_messages['not_active']}
                raise serializers.ValidationError(msg)
            msg = {'email': error_messages['wrong_credentials']}
            raise serializers.ValidationError(msg)
        data['user'] = user
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email: str) -> str:
        if not UserService.is_user_exist(email):
            raise serializers.ValidationError(_('User matching this e-mail address does not exist .'))
        return email


class PasswordResetConfirmSerializer(serializers.Serializer):
    password_1 = serializers.CharField(min_length=8, max_length=64)
    password_2 = serializers.CharField(min_length=8, max_length=64)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate_password_1(self, password: str):
        validate_password(password)
        return password

    def validate(self, data: dict):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError({'password_2': error_messages['password_not_match']})
        return data


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


class GithubCallbackSerializer(serializers.Serializer):
    code = serializers.CharField()
    state = serializers.CharField()

    def validate_state(self, state):
        if state != settings.SOCIALACCOUNT_PROVIDERS['github']['APP']['state']:
            raise serializers.ValidationError({'state': error_messages['state_not_match']})
        return state
























