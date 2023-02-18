from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from django.contrib.auth import get_user_model

from action.choices import SubscribeStatus
from api.v1.action.services import FollowService
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


class AvatarUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ['avatar']

    def save(self, **kwargs):
        # print(self.instance.avatar)         # avatar/1/a.jpg             #default.jpg
        # print(self.instance.avatar.url)     # /media/avatar/1/a.jpg      #media/default.jpg
        # print(self.instance.avatar.path)    # /usr/src/web/media/default.jpg

        # if not self.instance.avatar.path == '/usr/src/web/media/default.jpg':
        #     self.instance.avatar.delete()
        self.instance.avatar.delete()
        return super().save()


class FillOutViewSerializer(serializers.ModelSerializer):
    following_count = serializers.IntegerField()
    followers_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'birthday', 'avatar', 'following_count', 'followers_count']
        read_only_fields = ['email']


class AllUsersSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True, source='get_absolute_url')

    class Meta:
        model = User
        fields = ['id', 'url', 'full_name', 'first_name', 'last_name', 'email', 'gender', 'birthday', 'avatar']


class UserInfoSerializer(serializers.ModelSerializer):
    subscribe_status = serializers.SerializerMethodField(method_name='get_subscribe_status')
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'gender', 'birthday', 'avatar',
                  'subscribe_status', 'followers_count', 'following_count']

    def get_subscribe_status(self, obj: User) -> int:
        follow_services = FollowService(
            current_user=self.context['request'].user,
            content_maker_id=obj.id)
        return follow_services.get_subscribe_status()






