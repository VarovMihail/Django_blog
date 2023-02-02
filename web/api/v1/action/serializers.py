from rest_framework import serializers
from django.contrib.auth import get_user_model

from main.models import UserType
from action.models import Vote
from action.choices import LikeModel

User: UserType = get_user_model()


class LikeDislikeSerializer(serializers.Serializer):
    vote = serializers.ChoiceField(choices=Vote.choices)
    object_id = serializers.IntegerField(min_value=1)
    model = serializers.ChoiceField(choices=LikeModel.choices)


class SubscribeButtonSerializer(serializers.Serializer):
    content_maker_id = serializers.IntegerField(min_value=1)
    # followers_count = serializers.IntegerField()
    # following_count = serializers.IntegerField()


class FollowersFollowingButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'gender', 'birthday', 'avatar']

