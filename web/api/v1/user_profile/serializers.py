from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from main.models import UserType
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


User: UserType = get_user_model()

error_messages = {
    'old_password_not_match': _('The password does not  match'),
    'not_verified': _('Email not verified'),
    'not_active': _('Your account is not active. Please contact Your administrator'),
    'wrong_credentials': _('Entered email or password is incorrect'),
    'already_registered': _('User is already registered with this e-mail address'),
    'password_not_match': _('The two password fields did not match'),
}

class ChangePassSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    new_password1 = serializers.CharField(min_length=8, max_length=64, write_only=True)
    new_password2 = serializers.CharField(min_length=8, max_length=64, write_only=True)

    def validate_old_password(self, old_password):
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError( error_messages['old_password_not_match'])
        return old_password

    def validated_password1(self, password: str):
        validate_password(password)
        return password

    def validate(self, data: dict):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': error_messages['password_not_match']})
        return data


    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save(update_fields=['password'])
        return instance

# class AvatarUpdateSerializer(serializers.Serializer):
#     avatar = serializers.ImageField()
#
#     def save(self, **kwargs):
#         print(self.validated_data)
#         user = self.context['request'].user
#         avatar = self.validated_data['avatar']
#         user.avatar = avatar
#         user.save(update_fields=['avatar'])
#         return user


class AvatarUpdateSerializer(serializers.ModelSerializer):
    #avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ['avatar']


    # def save(self, **kwargs):
    #     print(self.validated_data)
    #     user = self.context['request'].user
    #     avatar = self.validated_data['avatar']
    #     print(avatar)
    #     user.avatar = avatar
    #     user.save(update_fields=['avatar'])
    #     print(self.data)
    #     return user.avatar
